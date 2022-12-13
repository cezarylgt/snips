from typing import List, Any
from datetime import datetime
from snips import settings as settings
from snips.domain import ISnippetRepository, Snippet, TagMatchingMode, IThemeRepository, Theme
import snips.domain.exceptions as ex
from tinydb import TinyDB, Query, JSONStorage
import json
from snips.domain.exceptions import ThemeNotFound
from snips.domain.themes.themes import DEFAULT_THEME
from snips.settings import CONFIG
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer


def deserialize(di: dict) -> Snippet:
    if di is None:
        return
    return Snippet(**di)


def deserialize_many(dis: List[dict]) -> List[Snippet]:
    return [deserialize(di) for di in dis if di is not None]


serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')


class TinyDbSnippetRepository(ISnippetRepository):
    """Implementation of ISnippetRepository for TinyDB lib"""

    def __init__(self, path: str  = CONFIG.DB_URI):
        self.db = TinyDB(path, storage=serialization)
        self.table = self.db.table("Snippets")
        self._query = Query()

    def get_all(self) -> List[Snippet]:
        return deserialize_many(self.table.all())

    def save(self, snp: Snippet) -> Snippet:
        current_time = datetime.now()
        snp.updated_at = current_time
        if not self.exists(snp.alias):
            snp.created_at = current_time

        doc_id = self.table.upsert(snp.dict(), self._query.alias == snp.alias)[0]
        return deserialize(self.table.get(doc_id=doc_id))

    def get_by_id(self, alias: str) -> Snippet:
        result = self.table.get(self._query.alias == alias)
        if result:
            return deserialize(result)
        raise ex.SnippetNotFound.with_message(alias)

    def get_by_tags(self, tags: List[str], mode: TagMatchingMode = TagMatchingMode.any) -> List[Snippet]:
        assert mode in TagMatchingMode.__members__.values()

        if mode == TagMatchingMode.any:
            return deserialize_many(self.table.search(self._query.tags.any(tags)))
        return deserialize_many(self.table.search(self._query.tags.all(tags)))

    def delete_by_id(self, alias: str) -> None:
        self.table.remove(self._query.alias == alias)

    def exists(self, alias: str) -> bool:
        return bool(self.table.get(self._query.alias == alias))

    def remove_all(self) -> None:
        self.db.drop_table('Snippets')


class TinyDbThemeRepository(IThemeRepository):

    def __init__(self, path: str = settings.THEMES_URI):
        self.db = TinyDB(path)
        self.table = self.db.table('themes')

        self._query = Query()

    def get_by_id(self, id: str):
        if id == 'default':
            return DEFAULT_THEME

        result = self.table.get(self._query.name == id)
        if result:
            return Theme(**result)
        raise ThemeNotFound
