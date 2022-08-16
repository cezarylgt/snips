from typing import List

from snips.domain import ISnippetRepository, Snippet
import snips.domain.exceptions as ex
from tinydb import TinyDB, Query
import snips.settings as settings


def deserialize(di: dict) -> Snippet:
    if di is None:
        return None
    return Snippet(**di)


class TinyDbSnipperRepository(ISnippetRepository):

    def __init__(self, path: str = settings.DB_URI):
        self.db = TinyDB(path)
        self.table = self.db.table(settings.SNIPPET_TABLE)

        self._query = Query()

    def get_all(self) -> List[Snippet]:
        return [deserialize(x) for x in self.table.all()]

    def save(self, snp: Snippet) -> Snippet:
        doc_id = self.table.upsert(snp.dict(), self._query.id == snp.id)[0]
        print('doc id', doc_id)
        return deserialize(self.table.get(doc_id=doc_id))

    def get_by_id(self, id: str) -> Snippet:
        result = self.table.get(self._query.id == id)
        if result:
            return deserialize(result)
        raise ex.SnippetNotFound.with_message(id)

    def delete_by_id(self, id: str) -> None:
        self.table.remove(self._query.id == id)
