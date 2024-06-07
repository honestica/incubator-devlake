from typing import Iterable

import pydevlake as dl
from pydevlake.pydevlake.domain_layer.crossdomain import Team
from pydevlake.pydevlake.api import Response

class NPSPluginConnection(dl.Connection):
    """The parameters of your plugin split between those that are required to connect to the datasource
    that are grouped in your connection class and those that are used to customize conversion to domain
    models that are grouped in your scope config class.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#connection-parameters
    """
    # TODO : Add a token
    url: str


class NPSPluginScopeConfig(dl.ScopeConfig):
    """A scope config contains the list of domain entities to collect and optionally some parameters
    used to customize the conversion of data from the tool layer to the domain layer.
    For example, you can define a regex to match issue type from issue name.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#scope-config
    """
    # Here we could filter by project
    pass


class NPSPluginToolScope(dl.ToolScope):
    """The tool scope type is the top-level entity type of your plugin.
    For example, a board, a repository, a project, etc.
    A scope is connected to a connection, and all other collected entities are related to a scope.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#tool-scope-type
    """
    team_name = str


class NPSPlugin(dl.Plugin):
    connection_type = NPSPluginConnection
    tool_scope_type = NPSPluginToolScope
    scope_config_type = NPSPluginScopeConfig
    streams = []

    def domain_scopes(self, tool_scope: NPSPluginToolScope) -> Iterable[dl.DomainScope]:
        """The domain_scopes method should return the list of domain scopes that are related to a given tool scope.
          Usually, this consists of a single domain scope, but it can be more than one for plugins that collect data from multiple domains."""
        yield Team(
            name=tool_scope.team_name,
        )

    def remote_scope_groups(self, connection: NPSPluginConnection) -> Iterable[dl.RemoteScopeGroup]:
        yield dl.RemoteScopeGroup(
            id="1",
            name="team1",
            )

    def remote_scopes(self, connection, group_id: str) -> Iterable[NPSPluginToolScope]:
        # Here we should get the list of teams
        yield NPSPluginToolScope(team_name='team1'),

    def test_connection(self, connection: NPSPluginConnection) -> dl.TestConnectionResult:
        # Fake test connection - Should be implemented
        response = Response(status=200, json={})
        return dl.TestConnectionResult.from_api_response(response)


if __name__ == '__main__':
    NPSPlugin.start()
