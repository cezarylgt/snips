import abc
import json
from enum import Enum
from typing import List, Optional, Any
import yaml

from rich import print as rich_print, print_json
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
        print_json(json.dumps(snp.dict(), default=str))


class YamlConsoleLogger(IConsoleLogger):
    def print(self, o: Any):
        rich_print(o)

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print('\n' + yaml.dump(snp.dict(), allow_unicode=True, sort_keys=False))


class PrettyConsoleLogger(IConsoleLogger):

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print(self._convert(snp))

    def print(self, o: Any):
        rich_print(f'[{self._theme.text}]{o}[/{self._theme.text}]')

    def _convert(self, snp: dm.Snippet) -> str:
        return rf"""
    [{self._theme.header}]Alias:[/{self._theme.header}] [{self._theme.alias}]{snp.alias}[/{self._theme.alias}]
    [{self._theme.header}]Snippet:[/{self._theme.header}] [{self._theme.snippet}]{snp.snippet}[/{self._theme.snippet}]
    [{self._theme.header}]Defaults:[/{self._theme.header}] [{self._theme.defaults}]{snp.defaults or ''}[/{self._theme.defaults}]
    [{self._theme.header}]Tags[/{self._theme.header}]: [{self._theme.tags}]{' '.join(snp.tags or [])} [/{self._theme.tags}]
    [{self._theme.header}]Description:[/{self._theme.header}] [{self._theme.desc}]{snp.desc}[/{self._theme.desc}]"""


class TableConsoleLogger(IConsoleLogger):
    _FIELD_ORDER = ['alias', 'snippet', 'defaults', 'tags', 'desc']

    def __init__(self, theme: Theme):
        super(TableConsoleLogger, self).__init__(theme)
        self._console = Console()

    def _log_snippet(self, *snps: dm.Snippet) -> None:
        table = Table(
            *[f"[{self._theme.header}]{f}[/{self._theme.header}]" for f in self._FIELD_ORDER], box=None
        )
        for snp in snps:
            table.add_row(*self._pretty_format(snp, self._theme))
        self._console.print(table)

    @staticmethod
    def _pretty_format(snp: dm.Snippet, theme: Theme) -> List[str]:
        return [rf"[{theme.text}]{snp.alias}[/{theme.text}]",
                rf"[{theme.snippet}]{snp.snippet}[/{theme.snippet}]",
                rf"[{theme.text}]{snp.defaults}[/{theme.text}]",
                rf"[{theme.text}]{' '.join(snp.tags or [])} [/{theme.text}]",
                rf"[{theme.text}]{snp.desc}[/{theme.text}]"]

    def log_snippets(self, *snps: dm.Snippet) -> None:
        self._log_snippet(*snps)


class ConsoleLoggerProviderEnum(str, Enum):
    POOR = 'poor'
    JSON = 'json'
    PRETTY = 'pretty'
    TABLE = 'table'
    YAML = 'yaml'


class ConsoleLoggerFactory:
    _mapping = {
        ConsoleLoggerProviderEnum.POOR: PoorConsoleLoger,
        ConsoleLoggerProviderEnum.JSON: JsonConsoleLogger,
        ConsoleLoggerProviderEnum.PRETTY: PrettyConsoleLogger,
        ConsoleLoggerProviderEnum.TABLE: TableConsoleLogger,
        ConsoleLoggerProviderEnum.YAML: YamlConsoleLogger
    }

    @staticmethod
    def create(logger_provider: ConsoleLoggerProviderEnum, theme: Theme) -> IConsoleLogger:
        return ConsoleLoggerFactory._mapping[logger_provider](theme)
