from requests import Request
from requests.sessions import Session
import urllib.parse
import json

import aspace._client_extensions as extensions


class ASpaceClient(Session):
    """
    Wraps the Session class from the requests Python library, configured
    specifically for interacting with the ArchivesSpace API.
    """

    def __init__(self, api_host='http://localhost:8089',
                 username='admin', password=''):
        super().__init__()
        self.aspace_api_host = api_host
        self.aspace_username = username
        self.aspace_password = password
        self.headers['Accept'] = 'application/json'
        self.authenticate()

        self.record_stream = extensions.RecordStream(self)  # RecordStream
        self.get_paginaged = extensions.RecordPages(self)  # RecordPages

    def prepare_request(self, request: Request):
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
        if the HTTP status code was not 200.
        """

        resp = self.post(
            '/users/' + self.aspace_username + '/login',
            {'password': self.aspace_password}
        )

        if resp.status_code != 200:
            raise 'Error while logging in, error code: ' + resp.status_code

        session = resp.json()['session']

        self.headers['X-ArchivesSpace-Session'] = session
        return resp
