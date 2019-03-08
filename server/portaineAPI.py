import json, requests, config



class portainer:
    def __init__(self):
        self.portainerURL = 'http://red-ctf.woodnbottle.com:9000/api'
        self.apiKey = config.apiKey

    """
    this wil receive a request from the API and assign the requesting user a cookie value.
    It will also spin up a new container to replace the one in reserve
    containers will be terminated after x amount of time TBD.
    config.py contains an apiKey for the local Portainer service. Create your own and put the API key in as a string.
    """

    def getApiKey(self, username, password):

        """
        Get Portainer API key to use in future requests
        """
        # set api endpoint
        endpoint = '/auth'

        # create request
        r_url = self.portainerURL + endpoint
        r_data = json.dumps({"Username": username,"Password": password})

        # send request

        r = requests.post(r_url, data=r_data)

        r_dict = json.loads(r.text)
        key = ('apiKey = \'{0}\''.format(r_dict['jwt']))

        # overwrite config file with new key
        f = open('./config.py', 'w')
        f.write(key)
        f.close()
        return r

    def getDockerServices(self):

        """
        Get Docker Services from Portainer API reverse proxy
        """
        # set api endpoint
        endpoint = '/endpoints/1/docker/services'

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}

        # send request
        r = requests.get(r_url, headers=r_headers)

        return r

    def getDockerServicesByID(self, endpointID, serviceID):

        """
        Get Docker Services by their ID from Portainer API reverse proxy
        """
        # set api endpoint
        endpoint = ('/endpoints/{0}/docker/services/{1}').format(endpointID, serviceID)

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}

        # send request
        r = requests.get(r_url, headers=r_headers)

        return r

    def updateDockerServiceByID(self, endpointID, serviceID, replicas):
        """
        Update Docker Services from Portainer API reverse proxy - need ID and current version of service, and number of replicas to set.
        """
        # first need to get the current service to find its version, and then do updates.
        serviceObject = json.loads(self.getDockerServicesByID(endpointID, serviceID).text)
        serviceSpecObject = serviceObject.get('Spec', {})
        version = serviceObject.get('Version', {}).get('Index', {})
        serviceSpecObject['Mode']['Replicated']['Replicas'] = int(replicas)

        # set api endpoint
        endpoint = ('/endpoints/{0}/docker/services/{1}/update').format(endpointID, serviceID)

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}
        r_params = {'version': version}
        r_data = json.dumps(serviceSpecObject)

        # send request
        r = requests.post(r_url, headers=r_headers, params=r_params, data=r_data)

        return r

    def increaseDockerServiceReplicaCountBy1(self, endpointID, serviceID):
        """
        Update a service to have one more replica.
        """
        # get current number of replicas for the service
        serviceSpecObject = self.getDockerServicesByID(endpointID, serviceID).text
        replicas = json.loads(serviceSpecObject).get('Spec', {}).get('Mode', {}).get('Replicated', {}).get('Replicas', {}) # ['Spec']['Mode']['Replicated']['Replicas']

        # call the update and pass n +1 replica count in.
        r = self.updateDockerServiceByID(endpointID, serviceID, replicas + 1)

    def decreaseDockerServiceReplicaCountBy1(self, endpointID, serviceID):
        """
        Update a service to have one more replica.
        """
        # get current number of replicas for the service
        serviceSpecObject = self.getDockerServicesByID(endpointID, serviceID).text
        replicas = json.loads(serviceSpecObject).get('Spec', {}).get('Mode', {}).get('Replicated', {}).get(
            'Replicas', {})  # ['Spec']['Mode']['Replicated']['Replicas']

        # call the update and pass n -1 replica count in.
        r = self.updateDockerServiceByID(endpointID, serviceID, replicas - 1)

        return r

    def getRecentlyCreatedContainers(self, endpointID, limit=None, label=None):
        """
        Get newly created container. Label of swarm service name is exact match. returns container list, can be used to find container objects.
        """
        # set api endpoint
        endpoint = ('/endpoints/{0}/docker/containers/json').format(endpointID)
        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}
        r_params = {}
        if limit is not None:
            r_params['limit'] = {'limit': int(limit)}
        if label is not None:
            r_params["filters"] = json.dumps({"label": [label]})
        else:
            print ('no label or limit specified. gathering all running containers')


        # send request
        r = requests.get(r_url, headers=r_headers, params=r_params)

        return r

    def stopContainerByID(self, endpointID, containerID, scaleDown=None,serviceID=None):
        """
        Stops a container by its ID, will scale down service if scaleDown is True. 15 seconds to scale down - it will recreate container otherwise.
        """
        # set api endpoint
        endpoint = ('/endpoints/{0}/docker/containers/{1}/stop').format(endpointID, containerID)

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}

        # send request
        r = requests.post(r_url, headers=r_headers)

        if scaleDown:
            self.decreaseDockerServiceReplicaCountBy1(endpointID, serviceID)

        return r
