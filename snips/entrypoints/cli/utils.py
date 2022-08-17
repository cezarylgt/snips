import typer
from rich.prompt import Prompt

from snips import domain as dm
from snips.domain.service import SnippetService
from snips.infrastructure import IConsoleLogger
from snips.ioc import get_ioc
import os


class Snips(typer.Typer):
    repository: dm.ISnippetRepository
    console_logger: IConsoleLogger
    service: SnippetService


def bootstrap() -> Snips:
    ioc = get_ioc()
    cli = Snips()
    cli.repository = ioc.repository
    cli.console_logger = ioc.console_logger
    cli.service = ioc.service
    cli.repository.save(dm.Snippet('drop-db', 'DROP DATABASE', 'drops database in sql server engine', tags=['sql']))
    return cli


def dto_from_prompt(df: dm.Snippet = None) -> dm.SnippetDto:
    alias = Prompt.ask("Set alias", default=df.alias if df else None)
    snippet = Prompt.ask("Set snippet", default=df.snippet if df else None)
    desc = Prompt.ask("Set description", default=df.desc if df else None)
    input_tags = Prompt.ask("Set tags (separeted by ',') ",
                            default=', '.join(df.tags) if df else None
                            )
    defaults = Prompt.ask("Set default values for provided arguments", default=df.defaults if df else None)

    if isinstance(input_tags, str):
        input_tags = [t.strip() for t in input_tags.split(',')]

    return dm.SnippetDto(
        alias=alias,
        snippet=snippet,
        desc=desc,
        tags=input_tags,
        defaults=defaults
    )


def prepare_command(snp: dm.Snippet, provided_arguments: dict = None) -> str:
    if not provided_arguments:
        provided_arguments = dict()

    args = {**provided_arguments}

    missing_args = snp.get_missing_default_arguments(provided_arguments.keys())
    if missing_args:
        print("Provide missing snippet arguments:")

        for arg in missing_args:
            args[arg] = Prompt.ask(arg)
    return snp.parse_command(args)



def parse_dict(string: str) -> dict:
    """User-friendly dict parse from string. The string should be prepared in following format:
        key1=value1,key2=value2
    where ',' separates dict items, left side of '=' is key, and right side of '=' is value.
    """
    if string is None:
        return dict()

    str_entries = string.split(',')
    di = dict()
    for sentry in str_entries:
        key, value = sentry.split('=')
        di[key] = value

    return di
