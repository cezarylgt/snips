import abc
from enum import Enum
from typing import List, Optional, Any

from rich import print as rich_print
from rich.console import Console
from rich.table import Table

import snips.domain as dm
from snips.settings import CONFIG


class IConsoleLogger:

    def log_snippets(self, *snps: dm.Snippet) -> None:
        for snp in snps:
            self._log_snippet(snp)

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


class Styles:
    header = CONFIG.HEADER_STYLE
    snippet = CONFIG.SNIPPET_STYLE
    text = CONFIG.TEXT_STYLE


class PrettyConsoleLogger(IConsoleLogger):

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print(self._convert(snp))

    def print(self, o: Any):
        rich_print(f'[{Styles.text}]{o}[/{Styles.text}]')

    def _convert(self, snp: dm.Snippet) -> str:
        # return f"""[bold blue]{snp.id}[/bold blue] [green]{snp.snippet}[/green] [yellow]{snp.desc}[/yellow]"""
        return rf"""
[{Styles.header}]Alias:[/{Styles.header}] [{Styles.text}]{snp.alias}[/{Styles.text}]
[{Styles.header}]Snippet:[/{Styles.header}] [{Styles.snippet}]{snp.snippet}[/{Styles.snippet}]
[{Styles.header}]Defaults:[/{Styles.header}] [{Styles.text}]{snp.defaults}[/{Styles.text}]
[{Styles.header}]Tags[/{Styles.header}]: [{Styles.text}]{' '.join(snp.tags or [])} [/{Styles.text}]
[{Styles.header}]Description:[/{Styles.header}] [{Styles.text}]{snp.desc}[/{Styles.text}]"""


class TableConsoleLogger(IConsoleLogger):
    _FIELD_ORDER = ['alias', 'snippet', 'defaults', 'tags', 'desc']

    def __init__(self):
        self._console = Console()

    def _log_snippet(self, *snps: dm.Snippet) -> None:
        table = Table(*[f"[{Styles.header}]{f}[/{Styles.header}]" for f in self._FIELD_ORDER])
        for snp in snps:
            values = [f"[{Styles.text}]{str(snp.dict()[field])}[/{Styles.text}]" for field in self._FIELD_ORDER]
            table.add_row(*values)
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
    def create(logger_provider: ConsoleLoggerProviderEnum) -> IConsoleLogger:
        return ConsoleLoggerFactory._mapping[logger_provider]()
