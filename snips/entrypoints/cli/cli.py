import os
from typing import List, Optional

import pyperclip
import typer
from rich import print as rich_print

import snips.domain as dm
from .utils import bootstrap, dto_from_prompt, prepare_command, parse_dict
from .config import app as config_app

app = bootstrap()
tags_app = typer.Typer()
app.add_typer(tags_app, name='tags')
app.add_typer(config_app, name='config')


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


@app.command()
def get(alias: str,
        raw: bool = typer.Option(False, help="Flag whether to use interpolate snippet with defaults or prompt")):
    """Copy snippet value into clipboard"""
    snippet = app.repository.get_by_id(alias)

    if not raw:
        cmd = prepare_command(snippet)
    else:
        cmd = snippet.snippet

    pyperclip.copy(cmd)
    rich_print(f"[green]'{cmd}'[/green] copied!")


@tags_app.command('get')
def tags_get(tags: List[str], mode: dm.TagMatchingMode = dm.TagMatchingMode.any):
    """Search snippets by tags"""
    result = app.repository.get_by_tags(tags, mode)
    app.console_logger.log_snippets(*result)


# /QUERIES

# COMMANDS
@app.command("rm")
def delete(alias: str):
    """Remove snippet """
    app.repository.delete_by_id(alias)
    rich_print(f"Snippet: [blue]{alias}[/blue] deleted")


@app.command()
def add():
    """Create new snippet"""
    dto = dto_from_prompt()
    e = app.service.create(dto)
    app.console_logger.log_snippets(e)


@app.command()
def edit(alias: str,
         a: str = typer.Option(None, help="set alias"),
         s: str = typer.Option(None, help="set snippet"),
         desc: str = typer.Option(None, help="set description"),
         tags: List[str] = typer.Option([], help="set tags"),
         defaults: str = typer.Option(None, help="Set default arguments")
         ):
    """Update existing snippet"""
    snippet = app.repository.get_by_id(alias)
    app.console_logger.log_snippets(snippet)

    if any((a, s, desc, tags, defaults)):
        dto = dm.SnippetDto(
            alias=a or snippet.alias,
            snippet=s or snippet.snippet,
            desc=desc or snippet.desc,
            tags=tags or snippet.tags,
            defauts=defaults or snippet.defaults
        )
    else:
        dto = dto_from_prompt(snippet)

    e = app.service.update(dto)
    app.console_logger.log_snippets(e)


@app.command()
def run(alias: str,
        args: str = typer.Option(None,
                                 help="Provide arguments for snippet execution. This will override default arguments"),
        pa: str = typer.Option("", help="Additional arguments that will be appended to the end of a snippet")):
    """Execute snippet in your os"""
    snippet = app.repository.get_by_id(alias)
    cmd = prepare_command(snippet, parse_dict(args))
    os.system(cmd + " " + pa)
