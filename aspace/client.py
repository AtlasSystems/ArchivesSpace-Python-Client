from requests import Request
from requests.sessions import Session
import urllib.parse
import json

class ASpaceClient(Session):
    """
    Wraps the Session class from the requests Python library, configured specifically
    for interacting with the ArchivesSpace API.
    """
    def __init__(self, api_host='http://localhost:8089', username='admin', password=''):
        super().__init__()
        self.aspace_api_host = api_host
        self.aspace_username = username
        self.aspace_password = password
        self.headers['Accept'] = 'application/json'
        self.authenticate()

    def prepare_request(self, request: Request):
        """
        Overrides and extends the `prepare_request` function from `requests.sessions.Session`.
        """
        request.url = urllib.parse.urljoin(self.aspace_api_host, request.url)
        return super().prepare_request(request)

    def authenticate(self):
        """
        Authenticates the ArchivesSpace API client, setting up the 
        `X-ArchivesSpace-Session` header for future requests. Returns
        the session ID.
        """

        resp = self.post(
            '/users/' + self.aspace_username + '/login', 
            {'password': self.aspace_password}
        )

        if resp.status_code != 200:
            raise 'Error while logging in, error code: ' + resp.status_code

        session = json.loads(resp.text)['session']

        self.headers['X-ArchivesSpace-Session'] = session
        return session
