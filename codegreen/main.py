import typer
from rich import print
from rich.markdown import Markdown


app = typer.Typer(rich_markup_mode="rich",help="[green]🍃 CodeGreen: Your Passport to a Greener Code! 🍃[/green]")


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

if __name__ == "__main__":
    app()