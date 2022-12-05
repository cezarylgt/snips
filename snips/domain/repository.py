import abc
from enum import Enum
from typing import List

from snips.domain.snippet import Snippet


class TagMatchingMode(str, Enum):
    """
    Enum representing possible matching modes
    """
    any = 'any'
    all = 'all'


class ISnippetRepository:

    @abc.abstractmethod
    def get_by_id(self, alias: str) -> Snippet:
        """Returns snippet by alias"""
        ...

    @abc.abstractmethod
    def get_all(self) -> List[Snippet]:
        """
        Returns all Snippets
        :return:
        """
        ...

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
    def save(self, snp: Snippet) -> Snippet:
        """
        Permanent save
        :param snp:
        :return: saved snippet
        """
        ...

    @abc.abstractmethod
    def delete_by_id(self, alias: str) -> None: ...

    @abc.abstractmethod
    def exists(self, alias: str) -> bool:
        """
        Checks if given alias exists
        :param alias:
        :return:
        """

    @abc.abstractmethod
    def remove_all(self) -> None: ...


class IConfigurationRepository:

    @abc.abstractmethod
    def get_all(self): ...

    def get_by_id(self, id: str): ...

    def save(self): ...
