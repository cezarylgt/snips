from typing import Protocol

import typer

from snips.domain import IThemeRepository
from snips.entrypoints.cli.utils import bootstrap
from snips.ioc import get_ioc


class ThemeApp(Protocol):
    repository: IThemeRepository


app = typer.Typer()
app.repository = get_ioc().theme_repository


@app.command()
def ls():
    """List all themes"""
    pass


@app.command()
def show(name: str):
    """Show one theme"""
    result = app.repository.get_by_id(name)



@app.command("rm")
def delete():
    """Remove theme"""


@app.command()
def add():
    """Add theme"""


@app.command()
def edit():
    """Edit theme"""
