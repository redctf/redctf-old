import binascii
import datetime
import hashlib
import logging
import os
import random
import re
import string
import json
from sys import stdout
from logging import *

import docker as d
from docker.utils.socket import demux_adaptor
from dockerfile_parse.parser import DockerfileParser

class dockerAPI:

    def __init__(self):
        # client
        self.client = d.from_env()


    def version(self):
        """
        :return: version of Docker client running (host set by environment variable)
        :from: https://docker-py.readthedocs.io/en/stable/client.html
        """
        r = self.client.version()
        print("this is a print test, file=sys.stderr")
        return r

    def listContainers(self, all=None):
        """
        List running containers on docker host.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param all: bool, set to true to return all containers
        :return: list of container objects
        """
        r = self.client.containers.list(all)

        return r

    # TODO: fix this so its not username dependent - aka add netIsolation switch like below. 
    def createNetwork(self, username):
        """
        Create a network based upon username.
        :from: https://docker-py.readthedocs.io/en/stable/networks.html
        :param username: string, username is used for network name
        :return: network object
        """
        # check if network exists
        net = self.checkIfNetworkExists(username)
        if net is False:
            # create network before creating container
            print("network {0} not found, creating {0} network".format(username))
            try:
                r = self.client.networks.create(name=username, driver="overlay", labels={"user": username}, attachable=True)
            except Exception as ex:
                print("createNetwork() {0}".format(ex))
        else:
            print("network {0} already exists".format(username))
            return net

        return r

    def getNetworkObject(self, networkName):
        """
        Get a network object by its name.
        :from: https://docker-py.readthedocs.io/en/stable/networks.html
        :param networkName: string, name of network to return
        :return: network object
        """
        # check if network exists
        net = self.checkIfNetworkExists(networkName)
        if net is False:
            return net
        else:
            try:
                networkObject = self.client.networks.get(networkName)
            except Exception as ex:
                print("getnetworkobject() {0}".format(ex))

            return networkObject

    def connectNetwork(self, networkName, containerName):

        net = self.getNetworkObject(networkName)
        try:
            net.connect(containerName)
            print("network connected")
        except Exception as ex:
            print("connectNetwork() {0}".format(ex))
            return False
        return True

    def createContainer(self, username, imageName, port, containerName=None, pathPrefix=None, netIsolation=None, containerType=None):
        """
        Create a container for a user.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param username: string, contributes to container name
        :param imageName: string, image name to use for container; imageName:versionNumber
        :param port: dict, port number(s) to use on container
        :param pathPrefix: traefik path prefix: '/hello' is used as a frontend rule
        :param netIsolation: for isolating a container to a specific user network
        :param containerType: string array [http, https, tcp]
        :return: container object
        """

        # check if image exists already
        image = self.checkIfImageExists(imageName)
        if image is False:
            print("no image found")
            # pull image if none exists
            try:
                print("pulling image: {0}".format(imageName))
                self.pullImage(imageName)
                print('image pull successful for: {0}'.format(imageName))
            except Exception as ex:
                print(ex)

        name = re.split(r'/|:', imageName)
        header = self.createRandomHashedHeader()

        
        if "/" in imageName and ":" in imageName:
            r_containerName = ("{0}_{1}".format(name[1], header))
            
        elif "/" in imageName:
            r_containerName = ("{0}_{1}".format(name[1], header))
            
        elif ":" in imageName:
            r_containerName = ("{0}_{1}".format(name[0], header))

        else:
            print("unknown combo provided")
            return("unknown imageName combo")    
            

        # for using network isolation per user basis.
        if netIsolation:

            # check if network exists already
            network = self.checkIfNetworkExists(username)
            if network is False:
                print("no network found")
                # create network if none exists
                try:
                    print("creating network: {0}".format(username))
                    self.createNetwork(username)
                    print('network create successful for: {0}'.format(username))
                except Exception as ex:
                    print(ex)

            # doesn't take commands yet.
            r_containerName = ("{0}_{1}".format(name, username))
            r_ports = {"{0}/tcp".format(port): None}
            r_labels = {"traefik.docker.network": username, "traefik.port": port, "traefik.frontend.rule": "PathPrefix:/{0}; Headers:user, {1};".format(pathPrefix, username), "traefik.backend.loadbalancer.sticky": "True", "traefik.enable": "true"}
            r = self.client.containers.run(imageName, detach=True, name=r_containerName, network=username, ports=r_ports, labels=r_labels)

            return r

        else:
            # check if network exists already
            ctfNet = "redctf_traefik"
            network = self.checkIfNetworkExists(ctfNet)
            if network is False:
                print("no network found")
                # create network if none exists
                try:
                    print("creating network: {0}".format(ctfNet))
                    self.createNetwork(ctfNet)
                    print('network create successful for: {0}'.format(ctfNet))
                except Exception as ex:
                    print(ex)

            r_ports = {"{0}/tcp".format(port): None}       

            # define labels  below - each new label is appended to the labels dict. 
            r_labels = {}
            # default middlewares inserted here as comma delimited string of
            middleware_chain = "errorhandler"
            
            # rules: path prefix and headers
            r_labels["traefik.http.routers.{0}.rule".format(r_containerName)] = "PathPrefix(`/{0}`) &&  HeadersRegexp(`Cookie`, `.*redctf={1};?.*`)".format(pathPrefix, header)
            
            # docker network
            r_labels["traefik.docker.network"] = ctfNet
            
            # LB server port
            r_labels["traefik.http.services.{0}.loadbalancer.server.port".format(r_containerName)] = port
            
            # define middleware chain
            r_labels["traefik.http.routers.{0}.middlewares".format(r_containerName)] = "{0}-chain".format(r_containerName)
            
            for container in containerType:
                # http containers only - will strip path using middleware
                if container == "http":
                    middleware_chain = middleware_chain + ", {0}-stripprefix".format(r_containerName)
                    r_labels["traefik.http.middlewares.{0}-stripprefix.stripprefix.forceslash".format(r_containerName)] = "false"
                    r_labels["traefik.http.middlewares.{0}-stripprefix.stripprefix.prefixes".format(r_containerName)] = "/{0}".format(pathPrefix)
                
                # placeholder https logic
                elif container == "https":
                    print("https container type")
                
                # placeholder tcp logic
                elif container == "tcp":
                    print("tcp container type")
                
                else:
                    print("unknown container type")
                    
            # define middleware chain middleware list - only appends if http above is true
            r_labels["traefik.http.middlewares.{0}-chain.chain.middlewares".format(r_containerName)] = middleware_chain
                
            r = self.client.containers.run(imageName, detach=True, name=r_containerName, network='redctf_traefik', ports=r_ports, labels=r_labels)

            return r

    def startContainer(self, containerName):
        """
        Start a container by name.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name to start
        :return: docker host response
        """
        # start the container in the created state
        try:
            container = self.client.containers.get(containerName)
            r = container.start()
            print(r)

        except Exception as ex:
            print(ex)

        return r

    def getContainerObject(self, containerName):
        """
        Get a container object by its name.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name
        :return: container object
        """
        try:
            containerObject = self.client.containers.get(containerName)
            print(containerObject)

        except Exception as ex:
            print(ex)
            return False

        return containerObject

    def stopContainer(self, containerObject):
        """
        Stop a container.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerObject: container object, used in conjunction with getContainerObject()
        :return: bool with status
        """
        try:
            containerObject.stop()

        except Exception as ex:
            print(ex)
            return False

        return True

    def removeContainer(self, containerName):
        """
        Remove a container by name.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name to remove
        :return: docker host response
        """
        # get the container object
        container = self.getContainerObject(containerName)

        # stop the container
        self.stopContainer(container)

        # remove the container
        try:
            r = container.remove()
            if r is None:
                print("Removed container")
        except Exception as ex:
            print(ex)

        return r

    def pruneContainers(self):
        """
        Prune (remove) all stopped containers.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :return: bool
        """
        try:
            self.client.containers.prune()

        except Exception as ex:
            print(ex)
            return False

        return True

    def pullImage(self, imageName):
        """
        Pull a image to be used in a container.
        :from: https://docker-py.readthedocs.io/en/stable/images.html
        :param imageName: string, image name
        :return: docker host response
        """
        try:
            r = self.client.images.pull("{0}:latest".format(imageName))
            print(r)
        except Exception as ex:
            print(ex)
            raise Exception(ex)

        return r

    def checkIfImageExists(self, imageName):
        """
        check to see if an image already exists or needs to be pulled.
        :from: https://docker-py.readthedocs.io/en/stable/images.html
        :param imageName: string, image name to check
        :return: bool
        """

        try:
            r = self.client.images.get(imageName)
            print(r)
        except Exception as ex:
            print(ex)
            return False

        return True

    def checkIfContainerExists(self, containerName):
        """
        Check to see if a con`tainer already exists.
        :from: https://docker-py.readthedocs.io/en/stable/containers.html
        :param containerName: string, container name to check
        :return: bool
        """
        try:
            self.client.containers.get(containerName)
            return True

        except Exception as ex:
            print(ex)
            return False

    def checkIfNetworkExists(self, networkName):
        """
        Check to see if a container already exists.
        :from: https://docker-py.readthedocs.io/en/stable/networks.html
        :param containerName: string, container name to check
        :return: bool
        """
        try:
            self.client.networks.get(networkName)
            return True
        except Exception as ex:
            print("checkIfNetworkExists() {0}".format(ex))
            return False

    def createRandomHashedHeader(self):
        """
        creates a random hashed character header for use in the container creation for Traefik to use.
         The header will be assigned to a user when they request a challenge, which will assign them a container.
        :return:string, hash for header use
        """
        seed = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(32)])
        salt = os.urandom(16)
        header = hashlib.pbkdf2_hmac('sha256', seed.encode('utf-8'), salt, 100000)
        headerString = binascii.hexlify(header).decode('ascii')
        return headerString
    
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

    def lintDockerFile(self, dockerfile, rulesFile, volume, debug=False, imagePath=None):
        
        commands = "dockerfile_lint -p -f {0} -r {1} -j".format(
            dockerfile, rulesFile)
        
        #TODO: build image for dft. 
        try: 
            image = self.checkIfImageExists('redctf_dockerfile_linter')
        except Exception as ex: 
            print(ex)
            
        if image:
            print("image exists")
        else:
            print("image does NOT exist - need to build it.")
            try: 
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                imagePath = './redctf/server/dockerAPI'
                newImage = self.buildImage(BASE_DIR, 'redctf_dockerfile_linter')
            except Exception as ex: 
                raise ex
            
            
        if debug == False:

            try:
                container = self.client.containers.run('redctf_dockerfile_linter', command = commands, auto_remove = True, volumes = {
                                                   volume: {'bind': '/dockerLint', 'mode': 'rw'}}, privileged=True)
                return container
            except Exception as ex:
                raise ex
        
        elif debug == True:
            
            try:
                container = self.getContainerObject('redctf_dockerfile_linter')
                if not container:
                    container = self.client.containers.create('redctf_dockerfile_linter', name='redctf_dockerfile_linter',  detach=False, auto_remove=False, command='sleep 1000', volumes={
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
            
    def buildImage (self, path, tag, labels=None):
        """
        check to see if an image already exists or needs to be pulled.
        :from: https://docker-py.readthedocs.io/en/stable/images.html
        :param imageName: string, image name to check
        :return: bool
        """
        if labels == None: 
            
            try:
                r = self.client.images.build(path=path, tag=tag, pull=True)
                print(r)
            except Exception as ex:
                print(ex)
                return False
        else: 
            try:
                r = self.client.images.build(path=path, tag=tag, pull=True, labels=labels)
                print(r)
            except Exception as ex:
                print(ex)
                return False

        return True