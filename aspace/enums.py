import enum
from collections import namedtuple


AgentTypeInfo = namedtuple('AgentTypeInfo', ['agent_type', 'api_endpoint'])


class AgentType(enum.Enum):
    # pylint: disable=E1101
    @property
    def agent_type(self) -> str:
        return self.value.agent_type

    @property
    def api_endpoint(self) -> str:
        return self.value.api_endpoint
    # pylint: enable=E1101

    PERSON = AgentTypeInfo('agent_person', '/agents/people')
    FAMILY = AgentTypeInfo('agent_family', '/agents/families')
    CORPORATE_ENTITY = AgentTypeInfo('agent_corporate_entity', '/agents/corporate_entities')
    SOFTWARE = AgentTypeInfo('software', '/agents/software')


class AgentNameOrder(enum.Enum):
    INVERTED = 'inverted'
    DIRECT = 'direct'
