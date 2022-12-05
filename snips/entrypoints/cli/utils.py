from typing import List, Any, Collection

import typer
from rich.prompt import Prompt

from snips import domain as dm
from snips.domain.service import SnippetService
from snips.infrastructure import IConsoleLogger
from snips.ioc import get_ioc

# import readline
_EMOJI = ":question:"
_TAG_SEPARATOR = ' '


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
    return cli


def parse_tags(tags: str | Collection) -> List[str]:
    print('tags type', type(tags))
    if isinstance(tags, str):
        return [t.strip() for t in tags.split(_TAG_SEPARATOR)]
    elif isinstance(tags, Collection):
        return list(tags)
    raise TypeError


def parse_dict(string: str) -> dict:
    """User-friendly dict parse from string. The string should be prepared in following format:
        key1=value1,key2=value2
    where ',' separates dict items, left side of '=' is key, and right side of '=' is value.
    """

    if not string:
        return

    str_entries = string.split(',')

    di = dict()
    for sentry in str_entries:
        if not sentry:
            continue
        key, value = sentry.split('=')
        di[key.strip()] = value
    return di


def dto_from_prompt(df: dm.Snippet = None, snippet: str = None) -> dm.SnippetDto:
    """
    Function to create SnippetDto object by using Prompt questions to interact with a user
    :param df:
    :param snippet:
    :return:
    """
    alias = Prompt.ask(f"{_EMOJI} Alias", default=df.alias if df else None)
    dm.Validators.alias_cannot_have_white_chars(alias)

    if not snippet:
        snippet = Prompt.ask(f"{_EMOJI} Snippet", default=df.snippet if df else None)
        # snippet = input("Snippet")
        dm.Validators.snippet_cannot_be_empty(snippet)

    description = Prompt.ask(f"{_EMOJI} Description", default=df.desc if df else None)
    input_tags = Prompt.ask(f"{_EMOJI} Tags (space separated) ",
                            default=_TAG_SEPARATOR.join(df.tags) if df else None
                            )
    defaults = Prompt.ask(f"{_EMOJI} Default values for provided arguments", default=df.defaults if df else None)

    return dm.SnippetDto(
        alias=alias,
        snippet=snippet,
        desc=description,
        tags=parse_tags(input_tags),
        defaults=parse_dict(defaults)
    )


def prepare_command_with_args(snp: dm.Snippet) -> str:
    arguments = snp.get_arguments()
    args = dict()
    for arg in arguments:
        args[arg] = Prompt.ask(f"{_EMOJI} {arg}")
    return snp.parse_command(args)


def prepare_command(snp: dm.Snippet, provided_arguments: dict = None) -> str:
    """
    Prepares snippet by checking if all required arguments were provided;
    if not, uses Prompt for each individual argument
    :param snp:
    :param provided_arguments:
    :return:
    """
    if not provided_arguments:
        provided_arguments = dict()

    args = {**provided_arguments}

    missing_args = snp.get_missing_default_arguments(provided_arguments.keys())
    if missing_args:
        print("Provide missing snippet arguments:")
        for arg in missing_args:
            args[arg] = Prompt.ask(f"{_EMOJI} {arg}")
    return snp.parse_command(args)


def read_file(path: str, encoding: str) -> str:
    with open(path, encoding=encoding) as f:
        return f.read()
