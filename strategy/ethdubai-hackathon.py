import datetime
import logging

import pandas as pd
from pandas_ta.overlap import sma
from tradeexecutor.ethereum.routing_data import get_quickswap_default_routing_parameters
from tradeexecutor.state.state import State
from tradeexecutor.state.trade import TradeExecution
from tradeexecutor.state.visualisation import PlotKind
from tradeexecutor.strategy.alpha_model import AlphaModel
from tradeexecutor.strategy.cycle import CycleDuration
from tradeexecutor.strategy.execution_context import ExecutionContext
from tradeexecutor.strategy.pandas_trader.position_manager import PositionManager
from tradeexecutor.strategy.pricing_model import PricingModel
from tradeexecutor.strategy.strategy_module import (
    ReserveCurrency,
    StrategyType,
    TradeRouting,
)
from tradeexecutor.strategy.trading_strategy_universe import (
    TradingStrategyUniverse,
    load_all_data,
    translate_trading_pair,
)
from tradeexecutor.strategy.universe_model import UniverseOptions
from tradeexecutor.strategy.weighting import weight_by_1_slash_n
from tradingstrategy.chain import ChainId
from tradingstrategy.client import Client
from tradingstrategy.timebucket import TimeBucket
from tradingstrategy.universe import Universe

# NOTE: this setting has currently no effect
TRADING_STRATEGY_ENGINE_VERSION = "0.1"

# NOTE: this setting has currently no effect
TRADING_STRATEGY_TYPE = StrategyType.managed_positions

# How our trades are routed.
trade_routing = TradeRouting.ignore

# Which chain we are trading on
chain_id = ChainId.polygon

# Which exchange we are trading on
exchange_slug = "sushi"

# Which quote tokens we use
quote_tokens = {
    "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",  # USDC
    "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",  # WMATIC
}

# Set cycle to 7 days and look back the momentum of the previous candle
trading_strategy_cycle = CycleDuration.cycle_4d
momentum_lookback_period = datetime.timedelta(days=4)

# Hold N top coins for every cycle
max_assets_in_portfolio = 3

# Leave 50% cash buffer
value_allocated_to_positions = 0.5

#
# Set the take profit/stop loss for our postions.
# Aim for asymmetric opportunities - upside is higher than downside
#

# Set % stop loss over mid price
stop_loss = 0.97

# Set % take profit over mid price
take_profit = 1.33

# The momentum period price must be up % for us to take a long position
minimum_mometum_threshold = 0.03

# The amount of XY liquidity a pair must have on DEX before
# we are happy to take any position.
minimum_liquidity_threshold = 100_000

# Don't bother with trades that would move position
# less than 300 USD
minimum_rebalance_trade_threshold = 300

# decide_trades() operates on 1d candles
candle_data_time_frame = TimeBucket.d1

# Use hourly candles to trigger the stop loss
stop_loss_data_granularity = TimeBucket.h1

# Strategy keeps its cash in USDC
reserve_currency = ReserveCurrency.usdc

# Define the periods when the native asset price is
# above its simple moving average (SMA)
bull_market_moving_average_window = pd.Timedelta(days=15)


logger = logging.getLogger(__name__)


def decide_trades(
    timestamp: pd.Timestamp,
    universe: Universe,
    state: State,
    pricing_model: PricingModel,
    cycle_debug_data: dict,
) -> list[TradeExecution]:
    # Create a position manager helper class that allows us easily to create
    # opening/closing trades for different positions
    position_manager = PositionManager(timestamp, universe, state, pricing_model)

    alpha_model = AlphaModel(timestamp)

    # Watch out for the inclusive range and include and avoid peeking in the future
    adjusted_timestamp = timestamp - pd.Timedelta(seconds=1)
    start = (
        adjusted_timestamp - momentum_lookback_period - datetime.timedelta(seconds=1)
    )
    end = adjusted_timestamp

    candle_universe = universe.candles
    pair_universe = universe.pairs

    # First figure out are we in a bear or a bull market condition.
    # Our rule for a bull market is that the price of the native token of the blockchain
    # is above its simple moving average.
    # Please see the notebook commments why we define this condition like this.
    bullish = False

    # Plot the WMATIC simple moving average.
    matic_usdc = pair_universe.get_pair(chain_id, exchange_slug, "WMATIC", "USDC")

    matic_usdc_candles = candle_universe.get_last_entries_by_pair_and_timestamp(
        matic_usdc.pair_id, timestamp
    )

    if len(matic_usdc_candles) > 0:
        matic_close = matic_usdc_candles["close"]
        matic_price_now = matic_close.iloc[-1]

        # Count how many candles worth of data needed
        matic_sma = sma(
            matic_close,
            length=bull_market_moving_average_window
            / candle_data_time_frame.to_timedelta(),
        )
        if matic_sma is not None:
            # SMA cannot be forward filled at the beginning of the backtest period
            sma_now = matic_sma[-1]
            assert (
                sma_now > 0
            ), f"SMA was zero for {timestamp}, probably issue with the data?"
            state.visualisation.plot_indicator(
                timestamp,
                "Native token SMA",
                PlotKind.technical_indicator_on_price,
                sma_now,
            )

            if matic_price_now > sma_now:
                bullish = True

        # Get candle data for all candles, inclusive time range
    candle_data = candle_universe.iterate_samples_by_pair_range(start, end)

    # Because this is long only strategy, we will honour our momentum signals only in a bull market
    if bullish:
        # Iterate over all candles for all pairs in this timestamp (ts)
        for pair_id, pair_df in candle_data:
            last_candle = pair_df.iloc[-1]

            assert (
                last_candle["timestamp"] < timestamp
            ), "Something wrong with the data - we should not be able to peek the candle of the current timestamp, but always use the previous candle"

            open = last_candle["open"]
            close = last_candle["close"]

            # Get the pair information and translate it to a serialisable strategy object
            dex_pair = pair_universe.get_pair_by_id(pair_id)
            pair = translate_trading_pair(dex_pair)

            available_liquidity = universe.resampled_liquidity.get_liquidity_fast(
                pair_id, adjusted_timestamp
            )
            if available_liquidity < minimum_liquidity_threshold:
                # Too limited liquidity, skip this pair
                continue

            # We define momentum as how many % the trading pair price gained during
            # the momentum window
            momentum = (close - open) / open

            # This pair has not positive momentum,
            # we only buy when stuff goes up
            if momentum <= minimum_mometum_threshold:
                continue

            alpha_model.set_signal(
                pair,
                momentum,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )

    # Select max_assets_in_portfolio assets in which we are going to invest
    # Calculate a weight for ecah asset in the portfolio using 1/N method based on the raw signal
    alpha_model.select_top_signals(max_assets_in_portfolio)
    alpha_model.assign_weights(method=weight_by_1_slash_n)
    alpha_model.normalise_weights()

    # Load in old weight for each trading pair signal,
    # so we can calculate the adjustment trade size
    alpha_model.update_old_weights(state.portfolio)

    # Calculate how much dollar value we want each individual position to be on this strategy cycle,
    # based on our total available equity
    portfolio = position_manager.get_current_portfolio()
    portfolio_target_value = portfolio.get_total_equity() * value_allocated_to_positions
    alpha_model.calculate_target_positions(portfolio_target_value)

    # Shift portfolio from current positions to target positions
    # determined by the alpha signals (momentum)
    trades = alpha_model.generate_rebalance_trades_and_triggers(
        position_manager,
        min_trade_threshold=minimum_rebalance_trade_threshold,  # Don't bother with trades under 300 USD
    )

    # Record alpha model state so we can later visualise our alpha model thinking better
    state.visualisation.add_calculations(timestamp, alpha_model.to_dict())

    return trades


def create_trading_universe(
    ts: datetime.datetime,
    client: Client,
    execution_context: ExecutionContext,
    universe_options: UniverseOptions,
) -> TradingStrategyUniverse:
    assert (
        not execution_context.mode.is_live_trading()
    ), f"Only strategy backtesting supported, got {execution_context.mode}"

    # Load data for our trading pair whitelist
    dataset = load_all_data(
        client,
        time_frame=candle_data_time_frame,
        execution_context=execution_context,
        universe_options=universe_options,
        liquidity_time_frame=TimeBucket.d1,
        stop_loss_time_frame=stop_loss_data_granularity,
    )

    # adapt Sushi routing params from Quickswap
    routing_parameters = get_quickswap_default_routing_parameters(reserve_currency)

    # factory -> (router, init_code_hash)
    # init code hash: https://polygonscan.com/address/0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506#code#L103
    routing_parameters["factory_router_map"] = {
        "0xc35DADB65012eC5796536bD9864eD8773aBc74C4": (
            "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
            "0xe18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303",
        )
    }

    universe = TradingStrategyUniverse.create_multipair_universe(
        dataset,
        [chain_id],
        [exchange_slug],
        quote_tokens=quote_tokens,
        reserve_token=routing_parameters["reserve_token_address"],
        factory_router_map=routing_parameters["factory_router_map"],
        liquidity_resample_frequency="1D",
    )

    return universe
