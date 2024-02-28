import networkx as nx
import docker
import signal
import sys


from dirs_network import DirsNetwork

client = docker.from_env()
DirsNetwork.stop_all_running_containers(client)

G = nx.connected_watts_strogatz_graph(5, 3, 0.1, 10)

network = DirsNetwork(client, G)

def signal_handler(sig, frame):
    network.clean_up()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop and remove containers')
signal.pause()