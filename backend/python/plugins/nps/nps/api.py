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
import json

from pydevlake.api import API, Response
from pydevlake.logger import logger, DEBUG

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from nps.models import NPSPluginConnection

class GoogleSheetsAPI(API):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SPREADSHEET_ID = "1isG8C7ZQz7dBFkGZ8IJaOh_K0OfTpL4J2sl1Fmv4EdE"
    RANGE_NAME = "Sheet1!A:E"

    def __init__(self, connection: NPSPluginConnection):
        super().__init__(connection)
        self.creds = self._get_credentials()

    def _get_credentials(self):
        """Gets valid user credentials from storage or initiates an OAuth2 flow."""
        creds = None
        # TODO: Where to store token.json?
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # TODO: Where to store credentials.json?
                flow = InstalledAppFlow.from_client_secrets_file("nps/credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def _fetch_data_from_sheet(self, range) -> Response:
        """Fetches data from the specified Google Sheet and returns a Response object."""
        try:
            service = build("sheets", "v4", credentials=self.creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.connection.spreadsheet_id,
                range=range,
            ).execute()
            return result
        except HttpError as err:
            logger.error(f"An error occurred: {err}")
            return Response(request=None, status=500, body=str(err).encode('utf-8'))

    def answers(self) -> Response:
        # Get answer range from connection
        range = self.connection.range_name
        result = self._fetch_data_from_sheet(range)
        values = result.get("values", [])
        # Remove the first line
        # TODO: What about the first line? Should we ignore it? Or should we map result based on that ?
        # The mapping could be stored in the connection!
        values.pop(0)
        return Response(request=None, status=200, body=json.dumps({ "answers" : values }).encode('utf-8'))

    def teams(self) -> Response:
        range = "Teams!A:A"
        result = self._fetch_data_from_sheet(range)
        values = result.get("values", []) # This is a list of lists
        teams = [team[0] for team in values]
        return Response(request=None, status=200, body=json.dumps({ "teams" : teams }).encode('utf-8'))
