import docker
import constants as const

# Stops all containers + removes "dirs-network"

client = docker.from_env()

for container in client.containers.list(all=True):
  container.remove(force=True)
  
for net in client.networks.list(names=const.DIRS_NETWORK_NAME): net.remove();