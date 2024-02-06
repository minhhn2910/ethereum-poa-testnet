## Config genesis data and prefunded accounts

* Blockchain config `seed_data/blockchain_config.json`
* Accounts: 10,000 accounts with private keys generated in `seed_data/accounts.json`. They can be regenerated with different numbers by using the `generate-accounts.py` script
* Extra code allocation for smart contracts: Some special account such as precompiled smart contracts that need to be included in genesis, the `seed_data/extra_allocation.json` shows how to do it.
In normal settings for experiments, you dont need to modify the accounts or precompiled smart contracts. You only need to change the blockchain config for `block_time` and `gas_limit` etc.

## Install required packages
  * `git clone https://github.com/minhhn2910/ethereum-poa-testnet.git`
  * `cd ethereum-poa-testnet`
  * `pip install -r requirements.txt`


## Run the blockchain nodes

`python poa-deploy.py start [workers param]`

## How to supply workers param:

### Start from a node and counting up with a number of nodes:
`python poa-deploy.py start --start-worker 30 --num-workers 8`

This will deploy 8 nodes starting from worker-030, worker-031, ...., worker-037

### Specify your own list of ip or hostnames:

Create a host file similar to `seed_data/host_list.txt`, each line is one ip or host that you can ssh into.

Then run with this command:

`python poa-deploy.py stop --host-file seed_data/host_list.txt`


Check if it runs sucessfully :
  * `docker services ls``
Check if the nodes are up and running with port `8503`, `8504`, ... opens.

## Stop blockchain nodes

`python poa-deploy.py stop [workers param]`


## Clean the environment (clean docker swarm)
Optional, you dont need to do it because the script will automatically do it every time the start command is triggered.
`python poa-deploy.py remove_swarm [workers param]`


## Acknowledgement
Reconfigured and built from:
  * https://github.com/ibrahim4529/ethereum-poa-docker
  * https://github.com/KunPengRen/ethereum-poa-docker
