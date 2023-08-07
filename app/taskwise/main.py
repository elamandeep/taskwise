import typer
import rich
from rich.progress import track
import time
from questionary import select
from importlib import import_module
from models import Model


def greet():
    """
    Greets users
    """
    time.sleep(0.1)
    typer.echo(rich.print("[red]Welcome to TaskWise!"))

    for _ in track(range(10), description="Loading..."):
        time.sleep(0.02)


def select_theme():
    """
    Lists all themes and add new theme
    """

    """
        Loader module import and use
    """
    loader_mod = import_module("loader")
    loader_obj = loader_mod.ThemeLoader()

    """
        Model Class imported
    """
    model_obj = Model()
    stored_theme = model_obj.get_current_themes()
    if stored_theme is not None:
        mod = loader_obj.load_specific_theme(stored_theme[0])
        mod.theme()
    else:
        typer.echo(rich.print("[red]List of themes"))
        theme = select("select theme", choices=loader_obj.themes).ask()
        print(theme)
        # model_obj.update_current_theme(theme)
        mod = loader_obj.load_specific_theme(theme)
        mod.theme()


def main():
    """
    Main function
    """
    greet()
    print("\x1b[2J\x1b[H")
    select_theme()


if __name__ == "__main__":
    typer.run(main)
