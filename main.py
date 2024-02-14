import docker
import signal
import sys

import constants as const

client = docker.from_env()

network = client.networks.create(const.DIRS_NETWORK_NAME)

container1 = client.containers.run(
    "cocacola-lover/dirs:0.1", 
    detach=True, 
    name="dirs-test1", 
    ports={'3334/tcp': 3333},
    hostname="testContainer1",
    network=const.DIRS_NETWORK_NAME,
    environment=['address=http://testContainer1:3333', 'friends=["http://testContainer2:3333/ask"]']
)

container2 = client.containers.run(
    "cocacola-lover/dirs:0.1", 
    detach=True, 
    name="dirs-test2", 
    ports={'3334/tcp': 3334},
    hostname="testContainer2",
    network=const.DIRS_NETWORK_NAME,
)

def signal_handler(sig, frame):
    print(container1.logs()) 
    container1.remove(force=True)
    container2.remove(force=True)
    print('\nContainers have been stopped and removed')
    network.remove()
    print('Network has been stopped and removed')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop and remove containers')
signal.pause()