import docker
import signal
import sys

client = docker.from_env()
container = client.containers.run(
    "cocacola-lover/dirs:0.1", 
    detach=True, 
    name="dirs-test", 
    ports={'3334/tcp': 3333}
)
print(container)

def signal_handler(sig, frame):
    container.remove(force=True)
    print('\nContainers have been stopped and removed')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop and remove containers')
signal.pause()