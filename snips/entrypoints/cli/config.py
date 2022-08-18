import typer
import snips.settings as settings
from dotenv import dotenv_values, set_key


def load_configuration() -> dict:
    return dotenv_values(settings.CONFIG_PATH)


app = typer.Typer()


@app.command()
def show():
    """returns current configuration"""
    cfg = load_configuration()
    print(dict(cfg))


@app.command("set")
def set_variable(var: settings.ConfigEnum, value: str ):
    """Set configuration variable"""
    set_key(settings.CONFIG_PATH, var, value)
