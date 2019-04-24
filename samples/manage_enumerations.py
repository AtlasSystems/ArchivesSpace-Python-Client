import aspace


client = aspace.client.ASpaceClient(
    'http://localhost/institution/api/',
    'admin', 'admin',
    auto_auth=True
)

client.manage_enumerations().update_enumeration(
    aspace.enums.Enumeration.LINKED_AGENT_EVENT_ROLES,
    ['test_value', 'Test value', 'Test value - /', 'RECIPIENT'],
    cleanup_new_values=True, reorder_enumeration=True
)

laer = (client
    .manage_enumerations()
    .get_enumeration(aspace.enums.Enumeration.LINKED_AGENT_EVENT_ROLES)
)

print(laer['values'])

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
