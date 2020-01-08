
import json
from sys import stdout

import docker as d
from docker.utils.socket import demux_adaptor
from dockerfile_parse.parser import DockerfileParser


class dockerAPI:

    def __init__(self):
        # client
        self.client = d.from_env()

    def parseDockerfile(self, dockerfile):
        try:
            with open(file=dockerfile) as f:
                r = DockerfileParser(fileobj=f)
                r_dict = {}
                # uncomment below to add additional fields from parser object to dictionary. 
                # r_dict['baseimage'] = r.baseimage
                # r_dict['cache_content'] = r.cache_content
                # r_dict['cached_content'] = r.cached_content
                # r_dict['cmd'] = r.cmd
                # r_dict['content'] = r.content
                r_dict['labels'] = r.labels

                r_ports = []
                count = 0
                for line in r.structure:
                    if line['instruction'] == 'EXPOSE':
                        r_ports.append(line['value'])

                r_dict['ports'] = r_ports

                r_json = json.dumps(r_dict)

                return r_json
            
        except Exception as ex:
            raise ex

    def lintDockerFile(self, dockerfile, rulesFile, volume, debug=False):
        
        commands = "dockerfile_lint -p -f {0} -r {1} -j".format(
            dockerfile, rulesFile)

        if debug == False:

            try:
                container = self.client.containers.run('dft', command = commands, auto_remove = True, volumes = {
                                                   volume: {'bind': '/dockerLint', 'mode': 'rw'}}, privileged=True)
                return container
            except Exception as ex:
                raise ex
        
        elif debug == True:
            
            try:
                container = self.getContainerObject('dft-test')
                if not container:
                    container = self.client.containers.create('dft', name='dft-test',  detach=False, auto_remove=False, command='sleep 1000', volumes={
                                                            volume: {'bind': '/dockerLint', 'mode': 'rw'}}, privileged=True)

                containerDict = {}
                containerDict['status'] = container.status
                if containerDict['status'] == 'created':
                    container.start()

                log = container.exec_run(commands, stream=False, demux=False)
                container.kill()
                for line in log:
                    print(line, end='')
                print(container.status)
                container.remove()
                return log
            except Exception as ex:
                raise ex

        else:
            raise("Unknown debug flag")
            

    def getContainerObject(self, containerName):
        """
        Get a container object by its name.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name
        :return: container object
        """
        try:
            containerObject = self.client.containers.get(containerName)

        except Exception as ex:
            print(ex)
            return False

        return containerObject
