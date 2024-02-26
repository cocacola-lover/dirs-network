import docker
import signal
import sys


from dirs_network import Dirs_Network

client = docker.from_env()

Dirs_Network.stop_all_running_containers(client)
network = Dirs_Network(client, 2)

def signal_handler(sig, frame):
    network.cleanUp()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop and remove containers')
signal.pause()