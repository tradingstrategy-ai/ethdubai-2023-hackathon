import os

from eth_defi.chain import install_chain_middleware
from web3 import HTTPProvider, Web3

from hackathon.logs import setup_logging


def make_test_trade():

    logger = setup_logging()

    json_rpc_url = os.environ["JSON_RPC_POLYGON"]
    web3 = Web3(HTTPProvider(json_rpc_url))

    install_chain_middleware(web3)

    private_key = os.environ.get("USER_PRIVATE_KEY")
    assert private_key is not None, "You must set PRIVATE_KEY environment variable"
    assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
