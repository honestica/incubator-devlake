
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

    def convert(self, answer: GoogleSheetNPSAnswer, context) -> Iterable[NPSDomainModel]:
        domain_model = NPSDomainModel(
            id=answer.answer_id,
            score=answer.score,
            responder_team=answer.responder_team,
            team=answer.team,
            created_at=answer.created_at,
        )
        yield domain_model
