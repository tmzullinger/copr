import json
import requests


class FrontendCallback(object):

    """ Object to send data back to fronted """

    def __init__(self, opts):
        super(FrontendCallback, self).__init__()
        self.frontend_url = opts.frontend_url
        self.frontend_auth = opts.frontend_auth
        self.msg = None

    def post_to_frontend(self, data):
        """ Send data to frontend """

        headers = {"content-type": "application/json"}
        url = "{0}/update/".format(self.frontend_url)
        auth = ("user", self.frontend_auth)

        self.msg = None
        try:
            r = requests.post(url, data=json.dumps(data), auth=auth,
                              headers=headers)
            if r.status_code != 200:
                self.msg = "Failed to submit to frontend: {0}: {1}".format(
                    r.status_code, r.text)

        except requests.RequestException, e:
            self.msg = "Post request failed: {0}".format(e)

        if self.msg:
            return False
        else:
            return True


    def build_starting(self, data):
        headers = {"content-type": "application/json"}
        url = "{0}/starting_build/".format(self.frontend_url)
        auth = ("user", self.frontend_auth)

        self.msg = None
        r = None
        try:
            r = requests.post(url, data=json.dumps(data), auth=auth,
                              headers=headers)
            if r.status_code != 200 or "canceled" not in r.json():
                self.msg = "Failed to submit to frontend: {0}: {1}".format(
                    r.status_code, r.text)
                raise requests.RequestException(self.msg)

        except requests.RequestException, e:
            self.msg = "Post request failed: {0}".format(e)
            raise

        return r.json()["canceled"]
            
            


