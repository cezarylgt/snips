import typer

import snips.domain as dm
from ioc import get_ioc
from snips.infrastructure import IConsoleLogger
from rich.prompt import Prompt
import pyperclip


class Snips(typer.Typer):
    repository: dm.ISnippetRepository
    console_logger: IConsoleLogger


def bootstrap() -> Snips:
    ioc = get_ioc()
    cli = Snips()
    cli.repository = ioc.snippet_repository
    cli.console_logger = ioc.console_logger
    cli.repository.save(dm.Snippet('drop-db', 'DROP DATABASE', 'drops database in sql server engine'))
    return cli


app = bootstrap()


@app.command()
def hello(name: str):
    print(f'Hello {name}')


@app.command()
def inject():
    print(f'Injection of repository is: {app.repository.__class__.__name__}')


@app.command()
def show(path: str):
    result = app.repository.get_by_id(path)
    app.console_logger.log(result)


@app.command()
def show_all():
    result = app.repository.get_all()
    app.console_logger.log_many(result)


@app.command()
def get(path: str):
    result = app.repository.get_by_id(path)
    pyperclip.copy(result.snippet)
    print(f"{result.snippet} copied!")


@app.command()
def add():
    id = Prompt.ask("Set id")
    snippet = Prompt.ask("Set snippet")
    desc = Prompt.ask("Set description")
    e = dm.Snippet(id, snippet, desc)
    e = app.repository.save(e)
    app.console_logger.log(e)


@app.command()
def delete(id: str):
    app.repository.delete_by_id(id)
    print(f"Snippet: {id} deleted")


if __name__ == '__main__':
    app()
