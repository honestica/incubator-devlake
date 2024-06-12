from typing import Iterable

from pydevlake import RemoteScopeGroup, TestConnectionResult, Plugin, DomainScope

from nps.models import NPSPluginConnection, NPSPluginToolScope, NPSPluginScopeConfig, NPSDomainModel
from nps.streams.answers import Answers
from nps.api import GoogleSheetsAPI

class NPSPlugin(Plugin):

    connection_type = NPSPluginConnection
    tool_scope_type = NPSPluginToolScope
    scope_config_type = NPSPluginScopeConfig
    streams = [
        Answers,
    ]

    def domain_scopes(self, tool_scope: NPSPluginToolScope) -> Iterable[DomainScope]:
        yield DomainScope(
            id=f"{tool_scope.team_name}",
        )

    def remote_scope_groups(self, connection: NPSPluginConnection) -> Iterable[RemoteScopeGroup]:
        yield RemoteScopeGroup(
            id="1",
            name="team1",
        )

    def remote_scopes(self, connection, group_id: str) -> Iterable[NPSPluginToolScope]:
        api = GoogleSheetsAPI(connection)
        result = api.teams()
        for team in result.json["teams"]:
            yield NPSPluginToolScope(
                id=team,
                name=team,
                team_name=team,
            )

    def test_connection(self, connection: NPSPluginConnection) -> TestConnectionResult:
        api = GoogleSheetsAPI(connection)
        result = api.answers()
        return TestConnectionResult.from_api_response(result)


if __name__ == '__main__':
    # plugin = NPSPlugin()
    # plugin.test_connection()
    NPSPlugin.start()
