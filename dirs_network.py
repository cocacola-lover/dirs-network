import docker
import os
import constants as const

class Dirs_Network () :
    def __init__ (self, client : docker.DockerClient, length : int) :
        self.client = client
        self.network = client.networks.create(const.DIRS_NETWORK_NAME)
        self.containers = [self.create_container(i) for i in range(length)]
        
    def extract_logs(self) :
        # Remove old logs
        for root, dirs, files in os.walk('./logs'):
            for f in files:
                os.unlink(os.path.join(root, f))
        # Write new logs      
        for container in self.containers :
            (_, out) = container.exec_run("cat logs.txt") 
            with open(f"logs/log_{container.name}.txt", "wb") as file:
                file.write(out)
        
    def clean_up(self) :
        self.extract_logs()
        
        for container in self.containers : container.remove(force=True)        
        print('\nContainers have been stopped and removed')

        self.network.remove()
        print('Network has been stopped and removed')
        
    def create_container(self, i : int) :
        return self.client.containers.run(
            const.DIRS_IMAGE_NAME, 
            detach=True, 
            name=f"dirs-test{i}", 
            ports={'3334/tcp': 3333 + i},
            hostname=f"testContainer{i}",
            network=const.DIRS_NETWORK_NAME,
            environment=[f'address=testContainer{i}', f'friends=["testContainer{i+1}"]']
        )
        
    @staticmethod
    def stop_all_running_containers(client : docker.DockerClient) :
        for container in client.containers.list(all=True):
            container.remove(force=True)
  
        for net in client.networks.list(names=const.DIRS_NETWORK_NAME): net.remove();
        
    