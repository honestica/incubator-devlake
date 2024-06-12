
from typing import Iterable

from pydevlake import Stream, DomainType
from pydevlake.api import APIException

from nps.models import GoogleSheetNPSAnswer, NPSDomainModel
from nps.api import GoogleSheetsAPI


class Answers(Stream):
    tool_model = GoogleSheetNPSAnswer
    domain_types = [DomainType.CROSS]
    domain_models = [NPSDomainModel]


    def collect(self, state, context) -> Iterable[tuple[object, dict]]:
        # Can use the state to store the last yielded item.
        # We should yield a line of data (one line = one answer)
        api = GoogleSheetsAPI(context.connection)
        try:
            response = api.answers()
        except APIException as e:
            # TODO: Do we want to manage specific error here?
            raise e
        for raw_answer in response.json["answers"]:
            yield raw_answer, state

    def extract(self, raw_data) -> GoogleSheetNPSAnswer:
        # TODO : Here we could import the mapping from the connection
        # Sample raw data : ['1', '8', 'INTEGRATION', 'PRODUCT', '4/22/2024 12:11:44']
        print(f"Extracting answer {raw_data}")
        return GoogleSheetNPSAnswer(
            answer_id=raw_data[0],
            score=int(raw_data[1]),
            responder_team=raw_data[2],
            team=raw_data[3],
            created_at=raw_data[4]
        )

    def convert(self, answer: GoogleSheetNPSAnswer, context) -> Iterable[NPSDomainModel]:
        domain_model = NPSDomainModel(
            id=answer.answer_id,
            score=answer.score,
            responder_team=answer.responder_team,
            team=answer.team,
            created_at=answer.created_at,
        )
        yield domain_model
