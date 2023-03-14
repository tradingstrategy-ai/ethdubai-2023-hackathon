"""Deploy Enzyme vault with the adapter.

To run:

    poetry run deploy
"""
import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_defi.chain import install_chain_middleware
from web3 import Web3, HTTPProvider
from web3.middleware import construct_sign_and_send_raw_middleware

from eth_defi.abi import get_deployed_contract
from eth_defi.enzyme.deployment import EnzymeDeployment
from hackathon.logs import setup_logging


def deploy():
    """Deploy our vault on Polygon."""

    logger = setup_logging()

    json_rpc_url = os.environ["JSON_RPC_POLYGON"]
    web3 = Web3(HTTPProvider(json_rpc_url))

    install_chain_middleware(web3)

    private_key = os.environ.get("PRIVATE_KEY")
    assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

    deployer: LocalAccount = Account.from_key(private_key)
    web3.middleware_onion.add(construct_sign_and_send_raw_middleware(deployer))

    logger.info(f"Deployer address is {deployer.address}")

    deployment = EnzymeDeployment.fetch(web3, deployer.address)
    assert deployment.contracts.integration_manager.address == "0x92fCdE09790671cf085864182B9670c77da0884B"

    usdc = get_deployed_contract(web3, "ERC20Mock.json", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    assert usdc.functions.symbol().call() == "USDC"

    comptroller, vault = deployment.create_new_vault(
        deployer.address,
        usdc,
        fund_name="Sushidel",
        fund_symbol="SUSHIDEL",
        verbose=True,
    )

    logger.info(f"Comptroller address is: {comptroller.address}")
    logger.info(f"Vault address is: {vault.address}")

    assert comptroller.functions.getDenominationAsset().call() == usdc.address
    assert vault.functions.getTrackedAssets().call() == [usdc.address]
    assert vault.functions.canManageAssets(deployer.address).call() is True
