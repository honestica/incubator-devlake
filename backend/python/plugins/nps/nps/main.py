from typing import Iterable

import pydevlake as dl
from pydevlake.api import Response

from nps.models import NPSPluginConnection, NPSPluginToolScope, NPSPluginScopeConfig, NPSDomainModel
from nps.streams.answers import Answer

class NPSPlugin(dl.Plugin):

    connection_type = NPSPluginConnection
    tool_scope_type = NPSPluginToolScope
    scope_config_type = NPSPluginScopeConfig
    streams = [
        Answer,
    ]

    def domain_scopes(self, tool_scope: NPSPluginToolScope) -> Iterable[NPSDomainModel]:
        """The domain_scopes method should return the list of domain scopes that are related to a given tool scope.
          Usually, this consists of a single domain scope, but it can be more than one for plugins that collect data from multiple domains."""
        yield NPSDomainModel(
            team=tool_scope.team_name,
        )

    def remote_scope_groups(self, connection: NPSPluginConnection) -> Iterable[dl.RemoteScopeGroup]:
        yield dl.RemoteScopeGroup(
            id="1",
            name="team1",
        )

    def remote_scopes(self, connection, group_id: str) -> Iterable[NPSPluginToolScope]:
        # Here we should get the list of teams
        yield NPSPluginToolScope(
            team_name='team1',
        )

    def test_connection(self, connection: NPSPluginConnection) -> dl.TestConnectionResult:
        # Fake test connection - Should be implemented
        print("Tototo")
        response = Response(status=200, json={})
        return dl.TestConnectionResult.from_api_response(response)


if __name__ == '__main__':
    # plugin = NPSPlugin()
    # plugin.test_connection()
    NPSPlugin.start()
