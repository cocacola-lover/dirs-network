import docker
import signal
import sys

import constants as const

client = docker.from_env()

network = client.networks.create(const.DIRS_NETWORK_NAME)

def createContainer(i : int) :
    return client.containers.run(
        const.DIRS_IMAGE_NAME, 
        detach=True, 
        name=f"dirs-test{i}", 
        ports={'3334/tcp': 3333 + i},
        hostname=f"testContainer{i}",
        network=const.DIRS_NETWORK_NAME,
        environment=[f'address=http://testContainer{i}:3333', f'friends=["http://testContainer{i+1}:3333/ask"]']
)
    
containers = [createContainer(i) for i in range(2)]

def extractLogs() :
    for container in containers :
        (_, out) = container.exec_run("cat logs.txt") 
        with open(f"logs/log_{container.name}.txt", "wb") as file:
            file.write(out)

def signal_handler(sig, frame):
    
    extractLogs()
    
    for container in containers : container.remove(force=True)
    
    print('\nContainers have been stopped and removed')
    
    network.remove()
    print('Network has been stopped and removed')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop and remove containers')
signal.pause()