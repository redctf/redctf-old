import json, requests

class traefik:

    """
    get cookie from traefik
    """

    traefikURL = 'http://red-ctf.woodnbottle.com'

    def getTraefikCookie(self, endpoint):
        """
        Get Traefik cookie to give to user
        """
        # set api endpoint
        endpoint = ('/{0}').format(endpoint)

        # create request
        r_url = self.traefikURL + endpoint

        # send request
        r = requests.Session().get(r_url)


        return r