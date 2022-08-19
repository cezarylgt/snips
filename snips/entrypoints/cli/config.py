import typer
from dotenv import dotenv_values, set_key
from rich import print

import snips.settings as settings
from snips.infrastructure.console_logger import ConsoleLoggerProviderEnum


def load_configuration() -> dict:
    return dotenv_values(settings.CONFIG_PATH)


app = typer.Typer()
set_app = typer.Typer(name='set', help="Manage configuration variables")
app.add_typer(set_app)


@app.command()
def show():
    """returns current configuration"""
    cfg = load_configuration()
    print(dict(cfg))


@set_app.command("env")
def set_variable(var: settings.ConfigEnum, value: str):
    """Set configuration variable py providing name and value"""
    set_key(settings.CONFIG_PATH, var, value)


@set_app.command()
def db_uri(uri: str):
    """Change your db uri.
    If DB_PROVIDER is set to 'json', this must be path to .json file
    """
    set_key(settings.CONFIG_PATH, settings.ConfigEnum.DB_URI, uri)


@set_app.command()
def format(format: ConsoleLoggerProviderEnum):
    """
    Change your display format
    """
    set_key(settings.CONFIG_PATH, settings.ConfigEnum.FORMAT, format)


@app.command()
def path():
    """returns path to your configuration"""
    print(settings.CONFIG_PATH)
