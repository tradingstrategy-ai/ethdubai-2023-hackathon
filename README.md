# Preface

You need

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
source env/local.env  # Set up secrets for commands used in this README
cd forge 
forge build              
```

The vault is deployed and configured using `hackathon/deploy.py`

- Currently there is only one inhouse smart contract that is Enzyme-Sushi-Trading Strategy adapter
- We depend on `web3-ethereum-defi` package that contains 600+ precompiled Defi smart contracts
- We deploy Enzyme vault using our deployment script, ABI files from `web3-ethereum-defi`
  and ABI files we compiled using Forge

0x92fcde09790671cf085864182b9670c77da0884b

To deploy the adapter.

```shell
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

After PolygonScan fails to verify contract please try again:


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

# Frontend

# Oracle

- Oracle is the server-side process the market feeds and drives strategy
- We use `trade-executor` Python package for this 
- Oracle is deployed manually using Docker
- Oracle trades once in a week so unfortunately we could not demostrate any live trading in hackathon
- Source code can be found in `strategy` folder
- [Deployment instructions are in the trade-executor documentation](https://tradingstrategy.ai/docs/running/strategy-deployment.html)