import datetime

from pydevlake import Field
from pydevlake.model import ToolModel

from pydevlake.migration import migration, MigrationScriptBuilder

@migration(20240610000001, name="initialize schemas for NPS")
def init_schemas(b: MigrationScriptBuilder):
  class NPSAnswer(ToolModel, table=True):
    answer_id: str = Field(primary_key=True)
    score: int
    responder_team: str
    team: str
    date: datetime

  b.create_table(NPSAnswer)
