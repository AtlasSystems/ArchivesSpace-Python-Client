import requests.sessions
import urllib.parse
import json

class ASpaceClient(requests.sessions.Session):
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

	def prepare_request(self, request: requests.Request):
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

		self.headers['X-ArchivesSpace-Session'] = json.loads(resp.text)['session']
		return self.headers['X-ArchivesSpace-Session']

	def get_paged(self, endpoint, page_size=10, page=1):
		"""
		Arbitrary ASpace endpoints that implement paging.
		"""
		raise 'Not Yet Implemented'

	def stream_records(self, endpoint):
		"""
		Stream records from arbitrary aspace endpoints.
		"""
		raise 'Not Yet Implemented'

