import aspace
import time


client = aspace.client.ASpaceClient(
    'http://localhost/institution/api/',
    'admin',
    'admin',
)

resp = client.get('/repositories/2')

# Simulate 1 month passing by deleting all sessions through mysql.
# `delete from session;`

resp = client.get('/repositories/2')

print('Done')
