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

import os

from pydevlake.testing import assert_valid_plugin, assert_plugin_run

from nps.main import NPSPlugin
from nps.models import NPSPluginConnection, NPSPluginScopeConfig


def test_valid_plugin():
    assert_valid_plugin(NPSPlugin())


def test_valid_plugin_and_connection(capsys):
    plugin = NPSPlugin()
    connection = NPSPluginConnection(id=1, name='test_connection')
    scope_config = NPSPluginScopeConfig(id=1, name='test_config')

    assert_plugin_run(plugin, connection, scope_config)
