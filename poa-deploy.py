#!/bin/python

import os
import subprocess
import sys
import time

# useage1: python3 start_eth.py start 02 03 04 05

# the commands following should be changed according to the docker swarm configuration
# /data/$user/ethereum-poa-docker


# remove_chain_nodes_command = "ssh worker-0{} 'cd /data/minh/ethr-did/ && rm -rf ./poa-docker'"
abs_path = os.path.dirname(os.path.abspath(__file__))
init_node_script = abs_path+"/init-nodes.sh"


# start_docker_swarm_command = "ssh {} 'cd " + abs_path + " ; DATA_PATH_PREFIX=" + abs_path + " docker stack deploy -c docker-compose.yaml eth'"
# stop_docker_swarm_command = "ssh {} 'cd " + abs_path + " ; DATA_PATH_PREFIX=" + abs_path +  " docker stack rm eth'"
leave_docker_swarm_command = "docker swarm leave --force"
leave_docker_swarm_command_remote = "ssh {} 'cd " + abs_path + " ; " + leave_docker_swarm_command + "'"
init_docker_swarm_command = leave_docker_swarm_command + " ; docker swarm init"
join_docker_swarm_command = "ssh {} ' cd " + abs_path + " ; "  + leave_docker_swarm_command  + " ; {}'"
start_docker_swarm_command =  "DATA_PATH_PREFIX=" + abs_path + " docker stack deploy -c docker-compose.yaml eth"
stop_docker_swarm_command = "DATA_PATH_PREFIX=" + abs_path +  " docker stack rm eth"

def update_chains(workers):
    ... # dont need to store and remove chain data in the host file system
def remove_chains(workers):
    ... # dont need to store and remove chain data in the host file system
def init_node(num_nodes=4):
    return subprocess.Popen(init_node_script + " " +str(num_nodes), shell=True).wait()
def init_swarm(workers):
    # leave and init new swarm
    subprocess.Popen(init_docker_swarm_command, shell=True).wait()
    # get join command
    process_output = subprocess.Popen("docker swarm join-token worker", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
    for line in process_output.splitlines():
        if "docker" in line:
            join_command = line
            break
    for worker in workers[1:]:
        command = join_docker_swarm_command.format(worker, join_command)
        print(command)
        time.sleep(0.1)
        subprocess.Popen(command, shell=True).wait()

def start_swarm(workers):
    command = start_docker_swarm_command.format(workers[0])
    print(command)
    return subprocess.Popen(command, shell=True).wait()

def stop_swarm(workers):
    command = stop_docker_swarm_command.format(workers[0])
    print(command)
    return subprocess.Popen(command, shell=True).wait()

def remove_swarm(workers):
    for worker in workers:
        command = leave_docker_swarm_command_remote.format(worker)
        print(command)
        subprocess.Popen(command, shell=True).wait()
def get_workers(args):
    if args.host_file != "":
        with open(args.host_file, 'r') as file:
            workers = file.read().splitlines()
            return workers
    else:
        workers = [f"worker-{int(args.start_worker) + i:03}" for i in range(args.num_workers)]
        return workers
import argparse
if __name__=='__main__':
    # python3 start_eth.py start --start-worker 01 --num-workers 4 --host-file ./hostfile --skip-swarm-setup
    parser = argparse.ArgumentParser(description='Start Ethereum PoA network')
    parser.add_argument('action', type=str, help='Action to perform')
    parser.add_argument('--start-worker', type=int, default=30, help='Start worker')
    parser.add_argument('--num-workers', type=int, default=4, help='Number of workers')
    parser.add_argument('--host-file', type=str, default="", help='Host file')
    parser.add_argument('--skip-swarm-setup', action='store_true', help='Skip swarm setup')

    args = parser.parse_args()
    if args.action == 'start':
        workers = get_workers(args)
        print (workers)
        init_node(len(workers))
        if not args.skip_swarm_setup:
            init_swarm(workers)
        start_swarm(workers)
    elif args.action == 'stop':
        workers = get_workers(args)
        stop_swarm(workers)
    elif args.action == 'init_swarm':
        workers = get_workers(args)
        init_swarm(workers)
    elif args.action == 'remove_swarm':
        workers = get_workers(args)
        remove_swarm(workers)
    else:
        print("Invalid action")
        sys.exit(1)

