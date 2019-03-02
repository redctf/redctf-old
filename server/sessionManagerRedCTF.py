import json, requests, docker, config



class portainerAPI:



    """
    this wil receive a request from the API and assign the requesting user a cookie value.
    It will also spin up a new container to replace the one in reserve
    containers will be terminated after x amount of time TBD.
    """
    portainerURL = 'http://red-ctf.woodnbottle.com:9000/api'
    apiKey = config.apiKey

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

    def updateDockerService(self):
        """
        Update Docker Services from Portainer API reverse proxy - need ID and previous version of service to increment version number
        """
        # set api endpoint
        endpoint = '/endpoints/1/docker/services'
        id = 're2dm45lloj605wfarj0wp99g'

        # create request
        r_url = self.portainerURL + endpoint
        r_headers = {'Authorization': self.apiKey}
        r_params = {'filters': docker.convert_filters('name', 'id', 'label', 'mode')}

        # send request
        r = requests.get(r_url, headers=r_headers, params=r_params)

        return r

class traefik:

    """
    get cookie from traefik
    """
    traefikURL = 'http://red-ctf.woodnbottle.com'

    def getTraefikCookie(self):
        """
        Get Traefik cookie to give to user
        """
        # set api endpoint
        endpoint = '/hello'

        # create request
        r_url = self.traefikURL + endpoint

        # send request
        r = requests.Session().get(r_url)


        return r