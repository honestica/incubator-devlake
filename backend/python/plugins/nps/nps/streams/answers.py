
from typing import Iterable

from pydevlake import Stream, DomainType

from nps.models import NPSAnswer, NPSDomainModel


class Answer(Stream):
    tool_model = NPSAnswer
    domain_models = [NPSDomainModel]
    domain_types = [DomainType.CROSS]


    def collect(self, state, context) -> Iterable[tuple[object, dict]]:
        # TODO: Add api connection here.
        # Can use the state to store the last yielded item.
        # We should yield a line of data (one line = one answer)
        fake_record = {
            "answer_id": "1",
            "score": 10,
            "responder_team": "team1",
            "team": "team2",
            "date": "2021-01-01"
        }
        yield fake_record, state

    def extract(self, raw_data) -> NPSAnswer:
        # TODO: Convert the raw data (one line) to the NPSAnswer model
        # Can be trivial
        return NPSAnswer(**raw_data)

    def convert(self, answer: NPSAnswer, context) -> Iterable[NPSDomainModel]:
        domain_model = NPSDomainModel(
            answer_id=answer.answer_id,
            score=answer.score,
            responder_team=answer.responder_team,
            team=answer.team,
            date=answer.date
        )
        yield domain_model
