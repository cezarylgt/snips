import abc
from enum import Enum
from typing import List, Optional, Any

from rich import print as rich_print
from rich.console import Console
from rich.table import Table

import snips.domain as dm
from snips.domain.themes.themes import Theme


class IConsoleLogger:

    def __init__(self, theme: Theme):
        self._theme = theme

    def log_snippets(self, *snps: dm.Snippet) -> None:
        for snp in snps:
            self._log_snippet(snp)
        print('')

    def print(self, o: Any):
        print(o)

    @abc.abstractmethod
    def _log_snippet(self, snp: dm.Snippet) -> None: ...


def format_tags(tags: Optional[List[str]]):
    if not tags:
        return []


class PoorConsoleLoger(IConsoleLogger):
    def _log_snippet(self, snp: dm.Snippet) -> None:
        print(snp.dict())


class JsonConsoleLogger(IConsoleLogger):

    def print(self, o: Any):
        rich_print(o)

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print(snp.dict())


def pretty_format(snp: dm.Snippet, theme: Theme) -> List[str]:
    return [rf"[{theme.text}]{snp.alias}[/{theme.text}]",
            rf"[{theme.snippet}]{snp.snippet}[/{theme.snippet}]",
            rf"[{theme.text}]{snp.defaults}[/{theme.text}]",
            rf"[{theme.text}]{' '.join(snp.tags or [])} [/{theme.text}]",
            rf"[{theme.text}]{snp.desc}[/{theme.text}]"]


class PrettyConsoleLogger(IConsoleLogger):

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print(self._convert(snp))

    def print(self, o: Any):
        rich_print(f'[{self._theme.text}]{o}[/{self._theme.text}]')

    def _convert(self, snp: dm.Snippet) -> str:
        # horizontal
        # return rf"""[{Styles.header}]Alias:[/{Styles.header}] [{Styles.text}]{snp.alias}[/{Styles.text}] [{Styles.header}]Snippet:[/{Styles.header}] [{Styles.snippet}]{snp.snippet}[/{Styles.snippet}] [{Styles.header}]Defaults:[/{Styles.header}] [{Styles.text}]{snp.defaults}[/{Styles.text}] [{Styles.header}]Tags[/{Styles.header}]: [{Styles.text}]{' '.join(snp.tags or [])} [/{Styles.text}] [{Styles.header}]Description:[/{Styles.header}] [{Styles.text}]{snp.desc}[/{Styles.text}]"""
        #
        # veritical
        return rf"""
    [{self._theme.header}]Alias:[/{self._theme.header}] [{self._theme.alias}]{snp.alias}[/{self._theme.alias}]
    [{self._theme.header}]Snippet:[/{self._theme.header}] [{self._theme.snippet}]{snp.snippet}[/{self._theme.snippet}]
    [{self._theme.header}]Defaults:[/{self._theme.header}] [{self._theme.defaults}]{snp.defaults or ''}[/{self._theme.defaults}]
    [{self._theme.header}]Tags[/{self._theme.header}]: [{self._theme.tags}]{' '.join(snp.tags or [])} [/{self._theme.tags}]
    [{self._theme.header}]Description:[/{self._theme.header}] [{self._theme.desc}]{snp.desc}[/{self._theme.desc}]"""

    # fields only
    # return rf""" [{Styles.text}]{snp.alias}[/{Styles.text}] [{Styles.snippet}]{snp.snippet}[/{Styles.snippet}]  [{Styles.text}]{snp.defaults}[/{Styles.text}] [{Styles.text}]{' '.join(snp.tags or [])} [/{Styles.text}] [{Styles.text}]{snp.desc}[/{Styles.text}]"""


class TableConsoleLogger(IConsoleLogger):
    _FIELD_ORDER = ['alias', 'snippet', 'defaults', 'tags', 'desc']

    def __init__(self, theme: Theme):
        super(TableConsoleLogger, self).__init__(theme)
        self._console = Console()

    def _log_snippet(self, *snps: dm.Snippet) -> None:
        table = Table(*[f"[{self._theme.header}]{f}[/{self._theme.header}]" for f in self._FIELD_ORDER],
                      box=None
                      )
        for snp in snps:
            table.add_row(*pretty_format(snp, self._theme))
        self._console.print(table)

    def log_snippets(self, *snps: dm.Snippet) -> None:
        self._log_snippet(*snps)


class ConsoleLoggerProviderEnum(str, Enum):
    POOR = 'poor'
    JSON = 'json'
    PRETTY = 'pretty'
    TABLE = 'table'


class ConsoleLoggerFactory:
    _mapping = {
        ConsoleLoggerProviderEnum.POOR: PrettyConsoleLogger,
        ConsoleLoggerProviderEnum.JSON: JsonConsoleLogger,
        ConsoleLoggerProviderEnum.PRETTY: PrettyConsoleLogger,
        ConsoleLoggerProviderEnum.TABLE: TableConsoleLogger
    }

    @staticmethod
    def create(logger_provider: ConsoleLoggerProviderEnum, theme: Theme) -> IConsoleLogger:
        return ConsoleLoggerFactory._mapping[logger_provider](theme)
