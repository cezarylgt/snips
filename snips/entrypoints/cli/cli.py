import os
# import readline
from typing import List

import pyperclip
import typer
from rich import print as rich_print

import snips.domain as dm
from .config import app as config_app
from .utils import bootstrap, dto_from_prompt, prepare_command, read_file, parse_dict, prepare_command_with_args, \
    parse_tags

# readline


app = bootstrap()
tags_app = typer.Typer()
app.add_typer(tags_app, name='tags', help="Manage tags")
app.add_typer(config_app, name='config', help="Manage configuration")


class LongArgs:
    alias = '--alias'
    snippet = '--snippet'
    desc = '--desc'
    tags = '--tags'
    defaults = '--defaults'


class ShortArgs:
    alias = '-a'
    snippet = '-s'
    desc = '-d'
    tags = '-t'
    defaults = '-df'


# QUERIES
@app.command()
def show(alias: str):
    """Show snippet data"""
    result = app.repository.get_by_id(alias)
    app.console_logger.log_snippets(result)


@app.command()
def ls(tags: List[str] = typer.Option(None, '--tags', '-t', help="List snippet by tags")):
    """List all available snippets"""
    if tags:
        result = app.repository.get_by_tags(tags)
    else:
        result = app.repository.get_all()
    app.console_logger.log_snippets(*result)


@tags_app.command('get')
def tags_get(tags: List[str], mode: dm.TagMatchingMode = dm.TagMatchingMode.any):
    """Search snippets by tags"""
    result = app.repository.get_by_tags(tags, mode)
    app.console_logger.log_snippets(*result)


@app.command()
def get(alias: str,
        raw: bool = typer.Option(False, '--raw', '-r',
                                 help="Flag whether to use interpolate snippet with defaults or prompt"),
        defaults: bool = typer.Option(True, help="Whether to auo parse command with default arguments")
        ):
    """Copy snippet value into clipboard"""
    snippet = app.repository.get_by_id(alias)

    cmd = snippet.snippet
    if snippet.get_arguments() and not raw:
        if defaults:
            cmd = prepare_command(snippet)
        else:
            cmd = prepare_command_with_args(snippet)

    pyperclip.copy(cmd)
    print('Copied:')
    app.console_logger.print(f"{cmd}")


# /QUERIES

# COMMANDS
@app.command("rm")
def delete(alias: str):
    """Remove snippet """
    app.repository.delete_by_id(alias)
    rich_print(f"[blue]{alias}[/blue] deleted")


@app.command()
def add(
        file: str = typer.Option(None, '--file', '-f', help="Read snippet from file"),
        a: str = typer.Option(None, LongArgs.alias, ShortArgs.alias, help="set alias"),
        s: str = typer.Option(None, LongArgs.snippet, ShortArgs.snippet, help="set snippet"),
        desc: str = typer.Option(None, LongArgs.desc, ShortArgs.desc, help="set description"),
        tags: List[str] = typer.Option([], LongArgs.tags, ShortArgs.tags, help="set tags"),
        defaults: str = typer.Option(None, LongArgs.defaults, ShortArgs.defaults, help="Set default arguments")
):
    """Create new snippet"""
    snippet_content = None
    if file is not None:
        app.console_logger.print('Reading snippet content from file: {} ...'.format(file))
        snippet_content = read_file(file, 'utf-8')
        app.console_logger.print('File content: \n')
        app.console_logger.print(snippet_content)

    if any((a, s, desc, tags, defaults)):
        dto = dm.SnippetDto(
            alias=a,
            snippet=s or snippet_content,
            desc=desc,
            tags=parse_tags(tags) if tags else None,
            defaults=parse_dict(defaults) if defaults else None
        )
    else:
        dto = dto_from_prompt(snippet_content)
    print('created dto', dto)
    e = app.service.create(dto)
    app.console_logger.log_snippets(e)


@app.command()
def edit(alias: str,
         a: str = typer.Option(None, LongArgs.alias, ShortArgs.alias, help="set alias"),
         s: str = typer.Option(None, LongArgs.snippet, ShortArgs.snippet, help="set snippet"),
         desc: str = typer.Option(None, LongArgs.desc, ShortArgs.desc, help="set description"),
         tags: List[str] = typer.Option([], LongArgs.tags, ShortArgs.tags, help="set tags"),
         defaults: str = typer.Option(None, LongArgs.defaults, ShortArgs.defaults, help="Set default arguments")
         ):
    """Update existing snippet"""
    snippet = app.repository.get_by_id(alias)

    if any((a, s, desc, tags, defaults)):
        dto = dm.SnippetDto(
            alias=a or snippet.alias,
            snippet=s or snippet.snippet,
            desc=desc or snippet.desc,
            tags=tags or snippet.tags,
            defaults=parse_dict(defaults) if defaults else snippet.defaults
        )
    else:
        dto = dto_from_prompt(snippet)

    e = app.service.update(dto, alias=snippet.alias)
    app.console_logger.log_snippets(e)


@app.command()
def run(alias: str,
        args: str = typer.Option(None, '--args', '-a',
                                 help="Provide arguments for snippet execution. This will override default arguments"),
        pa: str = typer.Option("", '--post-args', '-pa',
                               help="Additional arguments that will be appended to the end of a snippet")):
    """Execute snippet in your OS"""
    snippet = app.repository.get_by_id(alias)
    cmd = prepare_command(snippet, parse_dict(args))
    os.system(cmd + " " + pa)
