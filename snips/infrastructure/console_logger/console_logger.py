import abc
from typing import List

import snips.domain as dm
from rich import print as rich_print


class IConsoleLogger:
    output: callable

    @abc.abstractmethod
    def log(self, snp: dm.Snippet) -> None: ...

    @abc.abstractmethod
    def log_many(self, snps: List[dm.Snippet]) -> None: ...


class PoorConsoleLoger(IConsoleLogger):
    output = print

    def log_many(self, snps: List[dm.Snippet]) -> None:
        for snp in snps:
            self.output(snp.dict())

    def log(self, snp: dm.Snippet) -> None:
        self.output(snp.dict())


class JsonConsoleLogger(PoorConsoleLoger):
    output = rich_print

    def log_many(self, snps: List[dm.Snippet]) -> None:
        for snp in snps:
            rich_print(snp.dict())

    def log(self, snp: dm.Snippet) -> None:
        rich_print(snp.dict())


class PrettyConsoleLogger(IConsoleLogger):

    def _convert(self, snp: dm.Snippet) -> str:
        # return f"""[bold blue]{snp.id}[/bold blue] [green]{snp.snippet}[/green] [yellow]{snp.desc}[/yellow]"""
        return f"""[bold blue]Alias:[/bold blue] {snp.alias}\n[yellow]Description:[/yellow] {snp.desc}\n[yellow]tags[/yellow]: {' '.join(snp.tags)}\n[green]Snippet:[/green] {snp.snippet}"""

    def log(self, snp: dm.Snippet) -> None:
        rich_print(self._convert(snp))

    def log_many(self, snps: List[dm.Snippet]) -> None:
        for snp in snps:
            rich_print(self._convert(snp))
