import typer
from rich import print
from rich.markdown import Markdown


app = typer.Typer(rich_markup_mode="markdown" ,help = Markdown("[green]🍃 Awesome CLI user manager. 🍃[/green]"))


@app.callback()
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