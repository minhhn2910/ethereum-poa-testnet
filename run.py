#!/bin/python

import os
import subprocess
import sys
import time

# useage1: python3 start_eth.py start 02 03 04 05

# the commands following should be changed according to the docker swarm configuration
# /data/$user/ethereum-poa-docker
docker_swarm_join_command = os.environ.get('DOCKER_SWARM_JOIN_COMMAND',"docker swarm join --token SWMTKN-1-41aqap3tbx4gf4r1ukgu1nppee6zz0hpkbbexdaqwp4l2itgwz-3tar3u5vc3ukydbxpj59f1epa 10.10.10.13:2377")
# remove_chain_nodes_command = "ssh worker-0{} 'cd /data/minh/ethr-did/ && rm -rf ./poa-docker'"
abs_path = os.path.dirname(os.path.abspath(__file__))
join_docker_swarm_command = "ssh worker-0{} '" + docker_swarm_join_command + "'"

start_docker_swarm_command = "ssh worker-0{} 'cd " + abs_path + " ; DATA_PATH_PREFIX=" + abs_path + " docker stack deploy -c docker-compose.yaml eth'"

stop_docker_swarm_command = "ssh worker-0{} 'cd " + abs_path + " ; DATA_PATH_PREFIX=" + abs_path +  " docker stack rm eth'"

def update_chains(workers):
    ... # dont need to store and remove chain data in the host file system
def remove_chains(workers):
    ... # dont need to store and remove chain data in the host file system

def join_swarm(workers):
    for worker in workers:
        command = join_docker_swarm_command.format(worker, workers[0])
        print(command)
        subprocess.Popen(command, shell=True)

def start_swarm():
    command = start_docker_swarm_command.format(workers[0])
    print(command)
    subprocess.Popen(command, shell=True)

def stop_swarm():
    command = stop_docker_swarm_command.format(workers[0])
    print(command)
    subprocess.Popen(command, shell=True)

if __name__=='__main__':
    error_msg = 'python3 start_eth.py <start/stop>  params\n'\
            + '     start/stop chain1 chain2:     start or kill the network\n'
    if sys.argv[1] == 'update_chains':
        workers = list(sys.argv[2:])
        update_chains(workers)
    elif sys.argv[1] == 'start':
        workers = list(sys.argv[2:])
        update_chains(workers)
        time.sleep(8)
        start_swarm()
    elif sys.argv[1] == 'join_swarm':
        workers = list(sys.argv[2:])
        join_swarm(workers)
    elif sys.argv[1] == 'start_swarm':
        start_swarm()
    elif sys.argv[1] == 'stop_swarm' or sys.argv[1] == 'stop':
        workers = list(sys.argv[2:])
        stop_swarm()
    elif sys.argv[1] == 'remove_chains' or sys.argv[1] == 'remove':
        workers = list(sys.argv[2:])
        remove_chains(workers)
    else:
        print(error_msg)
        sys.exit(1)
