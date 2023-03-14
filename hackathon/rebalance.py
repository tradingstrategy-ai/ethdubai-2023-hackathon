"""In a trade, the fund owner (oracle) swaps the vault denominator asset (USDC) to other asset.

In this test swap we swap using

- Sushi on Polygon

- USDC->WMATIC

To run:

.. code-block:: shell

    poetry run rebalance

"""
import json
import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.contract import Contract
from web3.middleware import construct_sign_and_send_raw_middleware

from eth_defi.abi import get_deployed_contract, encode_function_call
from eth_defi.chain import install_chain_middleware
from web3 import HTTPProvider, Web3

from eth_defi.enzyme.deployment import EnzymeDeployment
from eth_defi.enzyme.generic_adapter import execute_calls_for_generic_adapter
from eth_defi.uniswap_v2.deployment import fetch_deployment, FOREVER_DEADLINE

from hackathon import conf
from hackathon.logs import setup_logging


def rebalance():

    logger = setup_logging()

    json_rpc_url = os.environ["JSON_RPC_POLYGON"]
    web3 = Web3(HTTPProvider(json_rpc_url))

    install_chain_middleware(web3)

    private_key = os.environ.get("PRIVATE_KEY")
    assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

    fund_owner: LocalAccount = Account.from_key(private_key)
    web3.middleware_onion.add(construct_sign_and_send_raw_middleware(fund_owner))

    logger.info("Fund owner address is %s", fund_owner.address)

    usdc = get_deployed_contract(web3, "ERC20Mock.json", conf.USDC_ADDRESS)
    assert usdc.functions.symbol().call() == "USDC"

    # Get Enzyme contracts
    deployment = EnzymeDeployment.fetch(web3)
    assert deployment.contracts.integration_manager.address == "0x92fCdE09790671cf085864182B9670c77da0884B"
    comptroller = deployment.contracts.get_deployed_contract("ComptrollerLib", conf.COMPTROLLER_ADDRESS)
    vault = deployment.contracts.get_deployed_contract("VaultLib", conf.VAULT_ADDRESS)

    # Get Sushi integration contract
    with open("forge/out/SushiAdapter.sol/SushiAdapter.json") as inp:
        contract_data = json.load(inp)
        abi = contract_data["abi"]

    sushi_adapter = web3.eth.contract(address=conf.SUSHI_ADAPTER_ADDRESS, abi=abi)

    usdc_amount = usdc.functions.balanceOf(vault.address).call()
    matic_amount = web3.eth.get_balance(vault.address)
    logger.info("Vault has %f USDC", usdc_amount / 10**6)
    logger.info("Vault has %f MATIC", matic_amount / 10**18)
    logger.info("SushiAdapter is deployed for Enzyme protocol: %s", sushi_adapter.functions.getIntegrationManager().call())

    assert usdc_amount > 0

    sushiswap = fetch_deployment(
        web3,
        factory_address=conf.SUSHI_FACTORY_ADDRESS,
        router_address=conf.SUSHI_ROUTER_ADDRESS,
    )

    wmatic = sushiswap.weth

    logger.info("Preparing to rebalance portfolio. Comptroller: %s, vault: %s", comptroller.address, vault.address)

    # Swap 50% USDC in the vault to WMATIC
    usdc_swap_amount = usdc_amount // 2
    spend_asset_amounts = [usdc_swap_amount]
    spend_assets = [usdc]
    path = [usdc.address, wmatic.address]
    expected_outgoing_amount, expected_incoming_amount = sushiswap.router.functions.getAmountsOut(usdc_swap_amount, path).call()
    
    incoming_assets = [wmatic]
    min_incoming_assets_amounts = [expected_incoming_amount]

    # The vault performs a swap on Uniswap v2
    encoded_approve = encode_function_call(
        usdc.functions.approve,
        [sushiswap.router.address, usdc_swap_amount]
    )

    encoded_swapExactTokensForTokens = encode_function_call(
        sushiswap.router.functions.swapExactTokensForTokens,
        [usdc_swap_amount, 1, path, sushi_adapter.address, FOREVER_DEADLINE]
    )

    bound_call = execute_calls_for_generic_adapter(
        comptroller=comptroller,
        external_calls=(
            (usdc, encoded_approve),
            (sushiswap.router, encoded_swapExactTokensForTokens),
        ),
        generic_adapter=sushi_adapter,
        incoming_assets=incoming_assets,
        integration_manager=deployment.contracts.integration_manager,
        min_incoming_asset_amounts=min_incoming_assets_amounts,
        spend_asset_amounts=spend_asset_amounts,
        spend_assets=spend_assets,
    )

    tx_hash = bound_call.transact({"from": fund_owner.address, "gas": 1_000_000})
    logger.info("Broadcasting rebalance tx: %s", tx_hash.hex())

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    assert receipt.status == 1
    logger.info("Done")
