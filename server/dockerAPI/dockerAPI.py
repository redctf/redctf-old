import docker as d
import json


class dockerAPI:

    def __init__(self):
        # client
        self.client = d.from_env()

    def version(self):
        r = self.client.version()

        return r

    def listContainers(self, all=None):
        r = self.client.containers.list(all)

        return r

    def initializeUser(self, username):
        """
        individual traefik contianer per user
        """
        # netParams = ("check_duplicate=True, driver='overlay', labels={'user': {0} scope='local'".format(username))
        containerName = ("traefik")

        try:
            net = self.createNetwork(username)
            print(net)
        except Exception as ex:
            print(ex)

        try:
            cont = self.createTraefikContainer(username)
            print(cont)
        except Exception as ex:
            print(ex)

        return net

    def createNetwork(self, username):

        # check if network exists
        net = self.checkIfNetworkExists(username)
        if net is False:
            # create network before creating container
            try:
                r = self.client.networks.create(name=username, driver="overlay", labels={"user": username}, attachable=True)
            except Exception as ex:
                print(ex)
        else:
            print("network {0} already exists".format(username))
            return net

        return r

    def getNetworkObject(self, networkName):

        networkObject = self.client.networks.get(networkName)

        return networkObject

    def connectNetwork(self, networkName, containerName):

        net = self.getNetworkObject(networkName)
        try:
            r = net.connect(containerName)
        except Exception as ex:
            print(ex)
            return False
        return True

    def createTraefikContainer(self, username=None):
        """
        must create a traefik.toml on the server you are creating this on to expose the API/dashboard.
        """
        # r =self.client.containers.create("traefik:latest", "docker.watch", name="traefik_{0}".format(username), network='traefik', ports={"80/tcp": "80", "9090/tcp": "9090"}, volumes={"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}})

        # check if network exists
        net = self.checkIfNetworkExists('traefik')
        if net is False:
            # create network before creating container
            try:
                self.createNetwork('traefik')
            except Exception as ex:
                print(ex)
        else:
            print("network already exists")

        traefik = self.checkIfContainerExists('traefik')
        if traefik is False:
            print("no traefik container found")

            # create container & run if none exists
            try:
                print("creating traefik container")
                r = self.client.containers.create("traefik:latest", name="traefik",network="traefik", ports={"80/tcp": "80", "9090/tcp": "9090"}, volumes={"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}, "/home/nate/traefik.toml": {"bind": "/etc/traefik/traefik.toml", "mode": "rw"}})
                print('created traefik container: {0}'.format(r))
                self.startContainer('traefik')
                status = self.getContainerObject('traefik').status
                print('traefik container status: {0}'.format(status))
            except Exception as ex:
                print(ex)
                return False
        else:
            print("traefik container already exists")
            return traefik

        return r

    def createContainer(self, username, imageName, port, pathPrefix=None):

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

        name = imageName.split("/")

        # doesn't take commands yet.
        r_containerName = ("{0}_{1}".format(name[1], username))
        r_ports = {"{0}/tcp".format(port): None}
        r_labels = {"traefik.docker.network": username, "traefik.port": port, "traefik.frontend.rule": "PathPrefix:/{0};".format(pathPrefix), "traefik.backend.loadbalancer.sticky": "True", "traefik.enable": "true"}
        r = self.client.containers.run(imageName, detach=True, name=r_containerName, network=username, ports=r_ports, labels=r_labels)

        return r

    def startContainer(self, containerName):

        # start the container in the created state
        try:
            container = self.client.containers.get(containerName)
            r = container.start()
            print(r)

        except Exception as ex:
            print(ex)

        return r

    def getContainerObject(self, containerName):

        try:
            containerObject = self.client.containers.get(containerName)
            print(containerObject)

        except Exception as ex:
            print(ex)
            return False

        return containerObject

    def stopContainer(self, containerObject):

        try:
            containerObject.stop()

        except Exception as ex:
            print(ex)
            return False

        return True

    def removeContainer(self, containerName):
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

        try:
            self.client.containers.prune()

        except Exception as ex:
            print(ex)
            return False

        return True

    def pullImage(self, containerName):
        # repo = self.client.images.list(all=True)
        # print(repo)
        try:
            r = self.client.images.pull("{0}:latest".format(containerName))
            print(r)
        except Exception as ex:
            print(ex)

        return r

    def checkIfImageExists(self, imageName):
        # check to see if an image already exists or needs to be pulled.
        try:
            r = self.client.images.get(imageName)
            print(r)
        except Exception as ex:
            print(ex)
            return False

        return True

    def checkIfContainerExists(self, containerName):
        # check to see if an image already exists or needs to be pulled.
        try:
            r = self.client.containers.get(containerName)
            print(r)
        except Exception as ex:
            print(ex)
            return False

        return True

    def checkIfNetworkExists(self, networkName):
        # check to see if an image already exists or needs to be pulled.
        try:
            r = self.client.networks.get(networkName)
            print(r)
        except Exception as ex:
            print(ex)
            return False

        return True
