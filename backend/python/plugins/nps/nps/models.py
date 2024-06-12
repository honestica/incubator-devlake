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

from datetime import datetime

from pydevlake import ScopeConfig, Field
from pydevlake.model import ToolModel, DomainModel, Connection, ToolScope


class GoogleSheetNPSAnswer(ToolModel, table=True):
    # Here we could add a url or any other field that can identify the answer
    answer_id: str = Field(primary_key=True)
    score: int
    responder_team: str
    team: str
    created_at: datetime


class NPSDomainModel(DomainModel):
    __tablename__ = "nps_answers"
    score: int
    responder_team: str #TODO: Rename as "stakeholder"
    team: str
    created_at: datetime


class NPSPluginConnection(Connection):
    # TODO : Configure spreadsheet_id and range_name
    spreadsheet_id: str = "1isG8C7ZQz7dBFkGZ8IJaOh_K0OfTpL4J2sl1Fmv4EdE"
    range_name: str = "Sheet1!A:E"


class NPSPluginToolScope(ToolScope):
    # TODO: We should move the spreadsheet_it and the range_name here
    team_name: str


class NPSPluginScopeConfig(ScopeConfig):
    """A scope config contains the list of domain entities to collect and optionally some parameters
    used to customize the conversion of data from the tool layer to the domain layer.
    For example, you can define a regex to match issue type from issue name.
    https://github.com/apache/incubator-devlake/blob/main/backend/python/README.md#scope-config
    """
    # Here we could filter by project
    pass
