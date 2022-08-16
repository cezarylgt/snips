import abc
from typing import List

from snips.domain.snippet import Snippet


class ISnippetRepository:

    @abc.abstractmethod
    def get_by_id(self, id: str) -> Snippet: ...

    @abc.abstractmethod
    def get_all(self) -> List[Snippet]: ...

    @abc.abstractmethod
    def get_by_tags(self, tags: List[str], mode='any') -> List[Snippet]:
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
