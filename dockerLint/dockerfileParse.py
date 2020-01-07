
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
        with open(file=dockerfile) as f:
            r = DockerfileParser(fileobj=f)
            r_dict = {}
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
                    # print("PORT: {0}".format(line['value']))
                    r_ports.append(line['value'])

            r_dict['ports'] = r_ports

            r_json = json.dumps(r_dict)

            return r_json

    # def buildLinterContainer(self):
    #     imageName = 'dft'
    #     cmd = '/bin/bash'

    #     linterContainerObject = self.client.containers.create(
    #         imageName, detach=True, name='redctf-dockerfile-linter', auto_remove=False, privileged=True, volumes={'/': {'bind': '/root/', 'mode': 'rw'}}, command=cmd)
    #     # linterContainerObject.run()
    #     """docker run -it 
    #     --rm --privileged 
    #     -v $PWD:/root/
    #     projectatomic/dockerfile-lint 
    #     dockerfile_lint -p -f dockerfile -r rules.yaml -j"""

    #     return linterContainerObject

#     def lintDockerfile(self, dockerfile, rulesFile, path):
#         """
#         Lint a dockerfile .
#         :from: https://docker-py.readthedocs.io/en/stable/containers.html
#         :param dockerfile: fully qualified path to dockerfile
#         :param rulesFile: fully qualified path to rules.yaml file
#         :return: docker host response
#         """
#         # run the container and return output
#         linter = 'dft'
#         commands = "dockerfile_lint -p -f {0} -r {1} -j".format(dockerfile, rulesFile)
#         # commands = "dockerfile_lint" # -p -f {0} -r {1} -j".format(dockerfile, rulesFile)
#         # print("commands:{0}".format(commands))
#         try:
#             container = self.client.containers.run(image=linter, auto_remove=False, privileged=True, volumes={
# path: {'bind': '/root/', 'mode': 'rw'}},  detach=True,  stderr=True, stdout=True, stream=False, command = commands)

#         except Exception as ex:
#             print(ex)

#         return 

    def lintDockerFile(self, dockerfile, rulesFile): #TODO: write debug flag and pass output if debug - otherwise status code. 
        container = self.getContainerObject('dft-test')
        commands = "dockerfile_lint -p -f {0} -r {1} -j".format('dockerfile', './rules.yaml')
        # TODO: build the stupid container in the docker-compose file. 
        if not container:
            container = self.client.containers.create('dft', name='dft-test',  detach=False, auto_remove=False, command='sleep 1000', volumes={
 '/home/nate/redctf/dockerLint': {'bind': '/dockerLint', 'mode': 'rw'}}, privileged=True)
            # print(type(container))

            # container.start()
            
        containerDict  = {}
        containerDict['status'] = container.status
        if containerDict['status'] == 'created':
            container.start()
        # pwd = container.exec_run('pwd', stream=False, demux=False)
        # for line in pwd:
        #     print(line)
            
        log = container.exec_run(commands, stream=False, demux=False)
        container.kill()
        for line in log: 
            print(line,end='')
        print(container.status)
        container.remove()
        return log

    def getContainerObject(self, containerName):
        """
        Get a container object by its name.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name
        :return: container object
        """
        try:
            containerObject = self.client.containers.get(containerName)
            # print(containerObject)

        except Exception as ex:
            print(ex)
            return False

        return containerObject
