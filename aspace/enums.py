import enum

class AgentTypeInfo(object):
    def __init__(self, agent_type: str, api_endpoint: str = None):
        self.agent_type = agent_type
        self.api_endpoint = api_endpoint

class AgentType(enum.Enum):
    PERSON = AgentTypeInfo('agent_person', '/agents/people')
    FAMILY = AgentTypeInfo('agent_family', '/agents/families')
    CORPORATE_ENTITY = AgentTypeInfo('agent_family', '/agents/families')
    SOFTWARE = AgentTypeInfo('software', '/agents/software')

class AgentNameOrder(enum.Enum):
    INVERTED = 'inverted'
    DIRECT = 'direct'
