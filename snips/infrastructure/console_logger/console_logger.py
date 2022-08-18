import abc
from enum import Enum
from typing import List, Optional, Any

from rich import print as rich_print
from rich.console import Console
from rich.table import Table

import snips.domain as dm


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


class PrettyConsoleLogger(IConsoleLogger):

    def _log_snippet(self, snp: dm.Snippet) -> None:
        rich_print(self._convert(snp))

    def print(self, o: Any):
        rich_print(o)

    def _convert(self, snp: dm.Snippet) -> str:
        # return f"""[bold blue]{snp.id}[/bold blue] [green]{snp.snippet}[/green] [yellow]{snp.desc}[/yellow]"""
        return rf"""
[bold blue]Alias:[/bold blue] {snp.alias}
[yellow]Description:[/yellow] {snp.desc}
[yellow]Tags[/yellow]: {' '.join(snp.tags or [])}
[green]Snippet:[/green] {snp.snippet}"""


class TableConsoleLogger(IConsoleLogger):
    _FIELD_ORDER = ['alias', 'snippet', 'defaults', 'tags', 'desc']

    def __init__(self):
        self._console = Console()

    def _log_snippet(self, *snps: dm.Snippet) -> None:
        table = Table(*[f"[blue]{f}[/blue]" for f in self._FIELD_ORDER])
        for snp in snps:
            values = [str(snp.dict()[field]) for field in self._FIELD_ORDER]
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
