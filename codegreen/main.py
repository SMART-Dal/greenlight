import typer
from rich import print
from rich.markdown import Markdown


app = typer.Typer(rich_markup_mode="rich",help="[green]🍃 CodeGreen: Your Passport to a Greener Code! 🍃[/green]")

@app.callback()
def callback():
    """
    CodeGreen
    """


@app.command()
def setup():
    """
    This command will calculate energy consumption for a single given github project
    """
    print("Shooting portal gun")

@app.command()
def start_measurement():
    """
    This command will start the energy measurement server
    """
    print("Shooting portal gun")


# @app.command()
# def load():
#     """
#     Load the portal gun
#     """
#     print("Loading portal gun")

# only use this by uncommenting for testing purposes
if __name__ == "__main__":
    app()