import aspace


client = aspace.client.ASpaceClient(
    'http://localhost/institution/api/',
    'admin', 'admin',
    auto_auth=True
)

client.enumerations.update_enumeration(
    aspace.enums.Enumeration.LINKED_AGENT_EVENT_ROLES,
    ['test_value', 'Test value', 'Test value - /', 'RECIPIENT'],
    cleanup_new_values=True, reorder_enumeration=True
)

l_a_e_r = client.enumerations.get(
    aspace.enums.Enumeration.LINKED_AGENT_EVENT_ROLES
)

print(l_a_e_r['values'])

#  [
#    "authorizer",
#    "executing_program",
#    "implementer",
#    "recipient",
#    "requester",
#    "test_value",
#    "transmitter",
#    "validator"
#  ]
