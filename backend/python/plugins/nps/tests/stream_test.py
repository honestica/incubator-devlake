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

import pytest

from nps.main import NPSPlugin
from nps.models import NPSDomainModel
from pydevlake.testing import assert_stream_convert, ContextBuilder


@pytest.fixture
def context():
    return (
        ContextBuilder(NPSPlugin())
        .with_connection() #TODO: Add connection when available
        .with_scope_config()
        .with_scope(name="NPS_Scope1", team_name="NPS_Team1")
        .build()
    )

def test_answers_stream(context, capsys):
    raw = {
        "answer_id": "1",
        "score": 10,
        "responder_team": "team1",
        "team": "product",
        "created_at": "2021-01-01T00:00:00",
    }
    expected = NPSDomainModel(
        id="1",
        score=10,
        responder_team="team1",
        team="product",
        created_at="2021-01-01T00:00:00",
    )
    with capsys.disabled():
        assert_stream_convert(NPSPlugin, "answers", raw, expected, context)