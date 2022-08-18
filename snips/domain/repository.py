import abc
from enum import Enum
from typing import List

from snips.domain.snippet import Snippet


class TagMatchingMode(str, Enum):
    any = 'any'
    all = 'all'


class ISnippetRepository:

    @abc.abstractmethod
    def get_by_id(self, id: str) -> Snippet: ...

    @abc.abstractmethod
    def get_all(self) -> List[Snippet]: ...

    @abc.abstractmethod
    def get_by_tags(self, tags: List[str], mode: TagMatchingMode = TagMatchingMode.any) -> List[Snippet]:
        """

        :param tags:
        :param mode:
             'any' - search by any tag matching with snippet
             'all' - search by all tags matching with snippet
        :return:
        """
        ...

    @abc.abstractmethod
    def save(self, snp: Snippet) -> Snippet: ...

    @abc.abstractmethod
    def delete_by_id(self, id: str) -> None: ...

    def exists(self, alias: str): ...

class IConfigurationRepository:

    @abc.abstractmethod
    def get_all(self): ...

    def get_by_id(self, id: str): ...

    def save(self): ...