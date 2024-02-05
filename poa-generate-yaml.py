import json
import yaml
import sys
import os
from collections import OrderedDict
# python poa-generate-yaml.py number_node config_file local_path
number_node =  int(sys.argv[1])
config_file = sys.argv[2]
if len(sys.argv) > 3:
    local_path = sys.argv[3]
else:
    local_path = os.path.dirname(os.path.abspath(__file__)) + '/seed_data'

with open(config_file, "r") as f:
    config = json.load(f)
    chain_id = config.get("chain_id", 42)
    block_time = config.get("block_time", 12)
    gas_limit = hex(config.get("gas_limit", 30000000))

yaml_file = {'version':'3'}
nodes = {}
for i in range(1,number_node+1):
    node={}
    http_port=str(30312+i)
    port=str(8502+i)
    ws_port = str(33444+i)
    node['hostname']='node_'+str(i)
    node['image']='ethereum/client-go:release-1.10'

    command = (
    "cp -r /root/data /root/data2 ; "
    "geth account import --datadir /root/data2 --password /root/files/password /root/files/priv.key ; "
    "geth --datadir /root/data2 init /root/files/genesis.json ; "
    "geth --datadir /root/data2 --nodiscover --syncmode full --nodekey /root/files/priv.key --port " + str(http_port) + " "
    "--http --http.addr \"0.0.0.0\" --http.vhosts=\"*\" --http.corsdomain=\"*\" --http.port " + str(port) + " "
    "--http.api db,eth,net,web3,admin,personal,miner,signer:insecure_unlock_protect --networkid " + str(chain_id) + " "
    "--unlock 0 --password /root/files/password --mine --allow-insecure-unlock --ws --ws.port " + str(ws_port) + " "
    "--ws.addr \"0.0.0.0\" --ws.origins=\"*\" --ws.api eth,net,web3"
    )
    node['command']= [command]
    node['entrypoint'] = '/bin/sh -c'
    volumes=[]
    volumes.append("${DATA_PATH_PREFIX}/seed_data/node_" + str(i)+'/keys/password:/root/files/password:ro')
    volumes.append("${DATA_PATH_PREFIX}/seed_data/node_" + str(i)+'/keys/priv.key:/root/files/priv.key:ro')
    volumes.append("${DATA_PATH_PREFIX}/seed_data/genesis.json:/root/files/genesis.json:ro")
    volumes.append("${DATA_PATH_PREFIX}/seed_data/node_" + str(i)+'/data:/root/data:ro')

    ports=[]
    ports.append(http_port+':'+http_port)
    ports.append(port+':'+port)
    ports.append(ws_port+':'+ws_port)
    node['volumes']=volumes
    node['ports']=ports
    nodes.update({ 'node'+str(i) : node })
yaml_file['services']= nodes
stream = open('docker-compose.yaml', 'w')
yaml.dump(yaml_file, stream)

    # node['command']= ("/bin/sh -c '"
    #                     "cp -r /root/data /root/data2;
    #                     'geth account import  --datadir /root/data2 --password /root/files/password /root/files/priv.key; '
    #                     'geth --datadir  /root/data2 init /root/files/genesis.json; ' +
    #                     'geth --datadir /root/data2 --nodiscover --syncmode full --nodekey /root/files/priv.key --port '+ str(http_port)+
    #                     ' --http --http.addr "0.0.0.0" --http.vhosts="*" --http.corsdomain="*" --http.port '+str(port)+
    #                     ' --http.api db,eth,net,web3,admin,personal,miner,signer:insecure_unlock_protect  --networkid '+str(chain_id)+
    #                     ' --unlock 0 --password /root/files/password --mine --allow-insecure-unlock  --ws --ws.port '+str(ws_port)+
    #                     ' --ws.addr "0.0.0.0" --ws.origins="*" --ws.api eth,net,web3')