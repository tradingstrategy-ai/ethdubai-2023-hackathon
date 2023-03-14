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

Contracts are managed by Forge

- Depends on Enzyme and OpenZeppelin
- Enzyme protocol is used for the investment vault
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
- We depend on `web3-ethereum-defi` package that contains 600+ precompiled Defi smart contracts
- We deploy Enzyme vault using our deployment script, ABI files from `web3-ethereum-defi`
  and ABI files we compiled using Forge

To deploy 

```shell

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