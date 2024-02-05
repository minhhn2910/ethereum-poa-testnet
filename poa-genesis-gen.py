import json
import codecs
from Crypto.Hash import keccak
import sys
import os

# python poa-genesis-gen nodes_path number_node chain_id account_file block_time
if len(sys.argv) < 4:
    print("Usage: python poa-genesis-gen.py nodes_path config_file account_file extra_allocation_file")
    sys.exit(1)
nodes_path = sys.argv[1]
number_node = int(sys.argv[2])
config_file = sys.argv[3]
account_file = sys.argv[4] if len(sys.argv) > 4 else "seed_data/accounts.json"
extra_allocation_file = sys.argv[5] if len(sys.argv) > 5 else "seed_data/extra_allocation.json"

with open(config_file, "r") as f:
    config = json.load(f)
    chain_id = config.get("chain_id", 42)
    block_time = config.get("block_time", 12)
    gas_limit = hex(config.get("gas_limit", 30000000))

def exportGenesis(consortium, chainId):
    pubKeyList = readPubKeys()
    addressList = getAdresses(pubKeyList)
    res = {}
    if consortium == "poa":
        res = cliqueGenesis(addressList, chainId)
    with open(nodes_path+"/genesis.json", "w") as outfile:
        json.dump(res, outfile, indent=2)
    outfile.close()
    return


def cliqueGenesis(addresses, chainId):
    res = baseGenesis()
    res["alloc"] = {
        addresses[0][2:]: {
            "balance": "0x2000000000000000000000000000000000000000000000"
        }
    }
    with open(account_file, "r") as f:
        accounts = json.load(f)
        for account in accounts:
            res['alloc'][account['address']] = {'balance': '10000000000000000000000000'}
    with open(extra_allocation_file, "r") as f:
        extra_allocations = json.load(f)
        for address, alloc_item in extra_allocations.items():
            res['alloc'][address] = alloc_item
    concataddress = "0x0000000000000000000000000000000000000000000000000000000000000000"
    for address in addresses:
        concataddress += address[2:]
    concataddress += "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    res["extraData"] = concataddress
    res["config"] = {
        "chainId": chainId,
        "homesteadBlock": 0,
        "eip150Block": 0,
        "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "eip155Block": 0,
        "eip158Block": 0,
        "byzantiumBlock": 0,
        "constantinopleBlock": 0,
        "petersburgBlock": 0,
        "istanbulBlock": 0,
        "clique": {
            "period": block_time,
            "epoch": 30000
        }
    }
    res["nonce"] = "0x0"
    res["difficulty"] = "0x1"
    res["timestamp"] = "0x5f5e100"
    return res


def baseGenesis():
    return {
        "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "coinbase": "0x0000000000000000000000000000000000000000",
        "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "gasLimit": gas_limit,
    }


def getAdresses(pubKeyList):
    res = []
    for pubKey in pubKeyList:
        res.append(public_to_address(pubKey.strip()))
    return res


def readPubKeys():
    res = []
    for i in range(1, int(number_node)+1):
        filename = nodes_path+"/node_"+str(i)+"/keys/pub.key"
        fileReader = open(filename, "r")
        currentLine = fileReader.readline()
        while currentLine != "":
            res.append(currentLine.strip())
            currentLine = fileReader.readline()
        fileReader.close()
    return res


def public_to_address(public_key):
    public_key_bytes = codecs.decode(public_key, "hex")
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take last 20 bytes
    wallet_len = 40
    wallet = "0x" + keccak_digest[-wallet_len:]
    return wallet


if __name__ == "__main__":
    exportGenesis("poa", chain_id)