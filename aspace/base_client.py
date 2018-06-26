r"""
Contains the BaseASpaceClient class.
"""

import requests
import urllib


class BaseASpaceClient(requests.Session):
    """
    Extends the Session class from the requests Python library, adding
    methods that relate to 
    """

    def __init__(self, api_host='http://localhost:8089',
                 username='admin', password=''):
        super().__init__()
        self.aspace_api_host = api_host
        self.aspace_username = username
        self.aspace_password = password
        self.headers['Accept'] = 'application/json'

    def prepare_request(self, request: requests.Request):
        """
        Overrides and extends the `prepare_request` function from
        `requests.sessions.Session`.
        """

        request.url = urllib.parse.urljoin(self.aspace_api_host, request.url)
        return super().prepare_request(request)

    def authenticate(self):
        """
        Authenticates the ArchivesSpace API client and sets up the
        X-ArchivesSpace-Session header for future requests. Returns
        the JSON response if the login was valid. Raises an error
        if the HTTP status code was not in the 200 series.
        """

        resp = self.post(
            '/users/' + self.aspace_username + '/login',
            {'password': self.aspace_password}
        )

        if resp.status_code != 200:
            raise ValueError(
                'Received %d while attempting to authenticate: %s' %
                (resp.status_code, resp.text)
            )

        session = resp.json()['session']
        self.headers['X-ArchivesSpace-Session'] = session
        return resp
