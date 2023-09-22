import typer
from rich import print
from rich.markdown import Markdown


app = typer.Typer(rich_markup_mode="markdown")


@app.callback(help = Markdown("[green]🍃 Awesome CLI user manager. 🍃[/green]"))
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    print("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    print("Loading portal gun")