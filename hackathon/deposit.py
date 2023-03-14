"""User deposits USDC into the vault."""

import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware

from eth_defi.abi import get_deployed_contract
from eth_defi.chain import install_chain_middleware
from web3 import HTTPProvider, Web3

from eth_defi.enzyme.deployment import EnzymeDeployment
from hackathon.logs import setup_logging
from hackathon import conf


def deposit():

    logger = setup_logging()

    json_rpc_url = os.environ["JSON_RPC_POLYGON"]
    web3 = Web3(HTTPProvider(json_rpc_url))

    install_chain_middleware(web3)

    private_key = os.environ.get("USER_PRIVATE_KEY")
    assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

    user: LocalAccount = Account.from_key(private_key)
    web3.middleware_onion.add(construct_sign_and_send_raw_middleware(user))

    logger.info("User address is %s", user.address)

    usdc = get_deployed_contract(web3, "ERC20Mock.json", conf.USDC_ADDRESS)
    assert usdc.functions.symbol().call() == "USDC"

    usdc_amount = usdc.functions.balanceOf(user.address).call()
    matic_amount = web3.eth.get_balance(user.address)
    logger.info("User has %f USDC", usdc_amount / 10**6)
    logger.info("User has %f MATIC", matic_amount / 10**18)

    assert usdc_amount > 0
    assert matic_amount > 0

    deployment = EnzymeDeployment.fetch(web3)
    assert deployment.contracts.integration_manager.address == "0x92fCdE09790671cf085864182B9670c77da0884B"

    comptroller = deployment.contracts.get_deployed_contract("ComptrollerLib", conf.COMPTROLLER_ADDRESS)
    vault = deployment.contracts.get_deployed_contract("VaultLib", conf.VAULT_ADDRESS)

    logger.info("Preparing shares buy. Comptroller: %s, vault: %s", comptroller.address, vault.address)

    # Buy vault shares for 3 USDC
    amount = 3
    usdc.functions.approve(comptroller.address, amount*10**6).transact({"from": user.address})
    tx_hash = comptroller.functions.buyShares(amount*10**6, 1).transact({"from": user.address})
    logger.info("Performing deposit: %s", tx_hash.hex())
    web3.eth.wait_for_transaction_receipt(tx_hash)
    logger.info("Deposit done")
