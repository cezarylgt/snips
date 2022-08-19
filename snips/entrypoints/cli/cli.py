import os
from typing import List, Optional

import pyperclip
import typer
from rich import print as rich_print

import snips.domain as dm
from .utils import bootstrap, dto_from_prompt, prepare_command, read_file, parse_dict, prepare_command_with_args
from .config import app as config_app

app = bootstrap()
tags_app = typer.Typer()
app.add_typer(tags_app, name='tags', help="Manage tags")
app.add_typer(config_app, name='config', help="Manage configuration")


# QUERIES
@app.command()
def show(alias: str):
    """Show snippet data"""
    result = app.repository.get_by_id(alias)
    app.console_logger.log_snippets(result)


@app.command()
def ls():
    """List all available snippets"""
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
    rich_print(f"Snippet: [blue]{alias}[/blue] deleted")


@app.command()
def add(file: str = typer.Option(None, '--file', '-f', help="Read snippet from file")):
    """Create new snippet"""
    snippet = None
    if file is not None:
        app.console_logger.print('Reading snippet content from file: {} ...'.format(file))
        snippet = read_file(file, 'utf-8')
        app.console_logger.print('File content: \n')
        app.console_logger.print(snippet)

    dto = dto_from_prompt(snippet=snippet)
    e = app.service.create(dto)
    app.console_logger.log_snippets(e)


@app.command()
def edit(alias: str,
         a: str = typer.Option(None, '--alias', '-a', help="set alias"),
         s: str = typer.Option(None, '--snippet', '-s', help="set snippet"),
         desc: str = typer.Option(None, '--desc', '-d', help="set description"),
         tags: List[str] = typer.Option([], '--tags', '-t', help="set tags"),
         defaults: str = typer.Option(None, '--defaults', '-df', help="Set default arguments")
         ):
    """Update existing snippet"""
    snippet = app.repository.get_by_id(alias)

    print(defaults)

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
    print(dto)

    e = app.service.update(dto)
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
