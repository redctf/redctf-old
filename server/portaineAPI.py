import json, requests, docker, config



class portainer:
    def __init__(self):
        self.portainerURL = 'http://red-ctf.woodnbottle.com:9000/api'
        self.apiKey = config.apiKey
        self.util = docker.client.api.service.utils

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

    def updateDockerServiceByID(self, endpointID, serviceID):
        """
        Update Docker Services from Portainer API reverse proxy - need ID and previous version of service to increment version number
        """
        # first need to get the current service to find its version, and then do updates.
        serviceSpecObject = self.getDockerServicesByID(endpointID, serviceID).text
        version = json.loads(serviceSpecObject)['Version']['Index']
        nextVersion = int(version + 1)

        # TODO: only pass parameters that we need to update.
        serviceSpecObject = self.getDockerServicesByID(endpointID, serviceID).text


        # set api endpoint
        endpoint = ('/endpoints/{0}/docker/services/{1}/update').format(endpointID, serviceID)

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}
        r_params = json.dumps({'version': version})
        r_data = serviceSpecObject
        # send request
        r = requests.post(r_url, headers=r_headers, params=r_params, data=r_data)

        return r
