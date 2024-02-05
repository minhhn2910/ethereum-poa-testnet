

## Set up nodes data
```
./init-nodes.sh [number of node]
```
e.g. `./init-node.sh 8`


## Run the blockchain nodes

`python poa-deploy.py start [worker lists]`

Check if it runs sucessfully :
  * `docker services ls``
Check if the nodes are up and running with port `8503`, `8504`, ... opens.

## Stop blockchain nodes

`python poa-deploy.py stop [worker lists]`

Check if it runs sucessfully :
  * `docker services ls``
Check if the nodes are up and running with port `8503`, `8504`, ... opens.


## Acknowledgement
Reconfigured and built from:
  * https://github.com/ibrahim4529/ethereum-poa-docker
  * https://github.com/KunPengRen/ethereum-poa-docker
