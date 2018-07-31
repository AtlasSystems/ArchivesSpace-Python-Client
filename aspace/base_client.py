r"""
Contains the BaseASpaceClient class.
"""

import configparser
import requests
import time
import urllib

import aspace


class BaseASpaceClient(requests.Session):
    """
    Extends the Session class from the requests Python library, adding
    methods that relate to 
    """

    def __init__(self, api_host: str = aspace.constants.DEFAULT_API_HOST,
                 username: str = aspace.constants.DEFAULT_USERNAME,
                 password: str = aspace.constants.DEFAULT_PASSWORD,
                 auto_auth=True):
        """
        Initializes a new ArchivesSpace client.

        :api_host: Url used to connect to the API of the ArchivesSpace 
        instance. Trailing slashes are not required.

        :username: Username of an ASpace user account that has access
        to the API.

        :password: Password of the ASpace user account.

        :auto_auth: Specifies whether the client automatically logs
        sends an authentication request to ArchivesSpace on initialization.
        This should be turned off in cases where the implementing program
        needs to wait for the ArchivesSpace instance to spin up.
        """
        
        super().__init__()
        self.aspace_api_host = api_host
        self.aspace_username = username
        self.aspace_password = password
        self.headers['Accept'] = 'application/json'
        
        if auto_auth:
            self.authenticate()

    @classmethod
    def init_from_config(cls, config: configparser.ConfigParser, 
                         section='aspace_credentials', auto_auth=False):
        """
        Initializes an instance of any subclass of BaseASpaceClient from an
        instance of the `configparser.ConfigParser` builtin Python config
        parser. The following keys must be set under the specified `section`
        of the specified `config`. If any are not set, the initializer will
        use defaults from the `aspace.constants` module.

        `"api_host"`: Url used to connect to the API of the ArchivesSpace 
        instance. Trailing slashes are not required.

        `"username"`: Username of an ASpace user account that has access
        to the API.

        `"password"`: Password of the ASpace user account.
        """

        def aspace_credential(term, default=None):
            return config.get(section, term, fallback=default)

        _self = cls(
            api_host=aspace_credential(
                'api_host', aspace.constants.DEFAULT_API_HOST),
            
            username=aspace_credential(
                'username', aspace.constants.DEFAULT_USERNAME),
            
            password=aspace_credential(
                'password', aspace.constants.DEFAULT_PASSWORD),

            auto_auth=auto_auth,
        )

        return _self

    def prepare_request(self, request: requests.Request):
        """
        Overrides and extends the `prepare_request` function from
        `requests.sessions.Session`.
        """

        request.url = urllib.parse.urljoin(self.aspace_api_host, request.url)
        return super().prepare_request(request)

    def wait_until_ready(self, check_interval=5.0, max_wait_time=None,
                         on_fail=None, authenticate_on_success=False):
        """
        Periodically checks the `/` endpoint of the base api host until the
        API becomes ready, or until the max_wait_time is reached.

        :check_interval: Specifies the number of seconds in between each 
        check. Can be a non-integer interval of seconds. Defaults to 5.

        :max_wait_time: Specifies the maximum number of seconds that the
        function will wait until raising a ValueError. Optional, if `None`,
        then the function will wait indefinitely.

        :on_fail: If callable, will execute after every attempt, before 
        initiating the wait. Intended to be used for writing to the 
        program's logs.

        :authenticate_on_success: If True, the client will attempt to
        authenticate after a successful connection. Please see the docs
        for the `authenticate` method.
        """

        counter = 0

        while not self.get('/').ok:
            if callable(on_fail): 
                on_fail()
                
            if max_wait_time is not None and counter > max_wait_time:
                raise ValueError(
                    "The API could not be reached within the maximum allowed "
                    "time."
                )

            time.sleep(check_interval)
            counter += check_interval

        if authenticate_on_success:
            self.authenticate()

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
