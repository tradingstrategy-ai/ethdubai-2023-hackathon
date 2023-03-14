
This is the Github repository for **Citade-Sashimi** EthDubai hackathon project.
The project implements non-custodial user investable automated trading strategies on the top of Sushi DEX.

The hackathon comes with one example trading strategy, but it's easy to custome the approach for the multiple professional-grade quant finance strategies. The strategies can be easily written in Python, using on-chain data sources and 150+ technical indicators out of the box. 

# Goal

**Citade-Sashimi** benefits decentralised investors and Sushi

- For **DeFi users** the project offer professional grade investable trading strategies with features like portfolio rebalancing, stop loss,
  alpha signals, position risk sizing and liquidity awarness
- For **Sushi** and its **liquidity provides** offers market taker volume 
- For strategy developers, offer a way to write automated trading strategies in high-level Python scripting  
  and on-chain fund management for accepting external capital with profit sharing 

The trading strategies are based on real yield that comes for trading profits.
Typical active trading strategies may include strategies like mean reversion, momentum and trend following. 
Active trading provides more sustainable yield than liquidity mining, as it is based on true profits. 

# Deliverables

In this hackathon we created

- Sushi adapter smart contract for Enzyme Vaults, so that trading strategies can perform rebalances using Sushi liquidity (see source, see Polygon smart contract)
- Trading Strategy backtesting and strategy development notebook for creating algorithmic trading strategies on the top of Sushi trading pairs and market data feeds
- SvelteKit frontend that allows you to connect the wallet and invest the Enzyme Finance vault smart contract that is controlled by Trading Strategy oracles

# Architecture

![Architecture overview](./architecture.png)

- **Polygon** blockchain for the underlying chain 
- **Sushi** DEX for the trading venue
- **Enzyme Finance** vaults smart contracts for managing strategy portfolio, investor shares and profit sharing
- **Trading Strategy** oracle for market data feeds, strategy development and backtesting
- **SvelteKit** frontend for the website

# Development

For building yhe project you need

- Forge
- Python
- Poetry

This repository contains Git submodules.

Include them:

```shell
git submodule update --init --recursive     
```

# Contracts

We have one in-house adapter contract and then a complex suite of contracts from other protocols.

- Contract compilation and deployment is managed by Forge
- Depends on Enzyme and OpenZeppelin
- Enzyme protocol is used for the investment vault
- [Enzyme protocol is already deployed on Polygon](https://docs.enzyme.finance/developers/contracts/polygon)
- We deploy a special Enzyme vault that is using custom SushiAdapter for connecting
  trade instructions to the investment vault and then to Sushi protocol
- Enzyme protocol is already deployed on Polygon, so we do not deploy it
- The Trading Strategy oracle is set up as a fund manager for the vault

To compile:

```shell
cd forge 
forge build              
```

The vault is deployed and configured using `hackathon/deploy.py`

- Currently there is only one inhouse smart contract that is Enzyme-Sushi-Trading Strategy adapter
- We depend on [web3-ethereum-defi](https://github.com/tradingstrategy-ai/web3-ethereum-defi) package that contains 600+ precompiled Defi smart contracts
- We deploy Enzyme vault using our deployment script, ABI files from `web3-ethereum-defi`
  and ABI files we compiled using Forge

0x92fcde09790671cf085864182b9670c77da0884b

To deploy the adapter.

```shell
# Set up secrets for commands used in this README
source env/local.env  

# 0x92fcde09790671cf085864182b9670c77da0884b is Enzyme IntegrationManager on Polygon
# https://docs.enzyme.finance/developers/contracts/polygon
 forge create \
  --constructor-args 0x92fcde09790671cf085864182b9670c77da0884b \
  --rpc-url $JSON_RPC_POLYGON \
  --private-key $PRIVATE_KEY \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --verify \
  src/SushiAdapter.sol:SushiAdapter
```

If/when PolygonScan contract verify fails please try again:

Deployer: 0x454E9F5219CD92BCAa8c5C0406c16fdA6116b342
Deployment address: 0x8b326FC39d222a7f8A6a210FBe3CDCDb2C2b62Ed

```shell
forge verify-contract \
    --chain-id 137 \
    --watch \
    --constructor-args $(cast abi-encode "constructor(address)" "0x92fcde09790671cf085864182b9670c77da0884b") \
    --compiler-version 0.6.12+commit.27d51765 \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    0x8b326FC39d222a7f8A6a210FBe3CDCDb2C2b62Ed \
    src/SushiAdapter.sol:SushiAdapter     
```

# Strategy code

Strategy code is available as Python. Python dependencies are managed by `poetry`.

- Backtesting 
- Live strategy Python module

To install

``shell
poetry install
``

To open the backtesting Jupyter notebook for the strategy development

```shell
poetry shell
jupyter notebook
```

# Frontend

# Oracle

- Oracle is the server-side process the market feeds and drives strategy
- We use `trade-executor` Python package for this 
- Oracle is deployed manually using Docker
- Oracle trades once in a week so unfortunately we could not demostrate any live trading in hackathon
- Source code can be found in `strategy` folder
- [Deployment instructions are in the trade-executor documentation](https://tradingstrategy.ai/docs/running/strategy-deployment.html)