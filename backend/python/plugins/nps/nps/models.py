# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import datetime

from pydevlake import ScopeConfig, Field
from pydevlake.model import ToolModel, DomainModel, Connection, ToolScope


class NPSAnswer(ToolModel, table=True):
    answer_id: str = Field(primary_key=True)
    score: int
    responder_team: str
    team: str
    # date: datetime


class NPSDomainModel(DomainModel):
    answer_id: str
    score: int
    responder_team: str
    team: str
    # date: datetime


class NPSPluginConnection(Connection):
    """The parameters of your plugin split between those that are required to connect to the datasource
    that are grouped in your connection class and those that are used to customize conversion to domain
    models that are grouped in your scope config class.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#connection-parameters
    """
    # TODO : Add a token
    url: str


class NPSPluginToolScope(ToolScope):
    """The tool scope type is the top-level entity type of your plugin.
    For example, a board, a repository, a project, etc.
    A scope is connected to a connection, and all other collected entities are related to a scope.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#tool-scope-type
    """
    team_name: str


class NPSPluginScopeConfig(ScopeConfig):
    """A scope config contains the list of domain entities to collect and optionally some parameters
    used to customize the conversion of data from the tool layer to the domain layer.
    For example, you can define a regex to match issue type from issue name.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#scope-config
    """
    # Here we could filter by project
    pass
