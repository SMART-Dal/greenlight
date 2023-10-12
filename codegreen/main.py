import typer
from rich import print
from rich.markdown import Markdown
from codegreen.fecom.measurement import start_measurement
from typing_extensions import Annotated
from pathlib import Path
from typing import List

import subprocess
from codegreen.fecom.patching.patching_config import METHOD_LEVEL_PATCHING_SCRIPT_PATH
# from codegreen.fecom.patching.


app = typer.Typer(rich_markup_mode="rich",help="[green]🍃 CodeGreen: Your Passport to a Greener Code! 🍃[/green]")

@app.command()
def start_energy_profiler(
    project : Annotated[Path,typer.Option(help="Path to the source code of the project to be measured.")],
    scripts : Annotated[List[Path],typer.Option(help="List of paths to the project scripts to be measured.")],
):
    """
    This command will start the energy measurement server
    """
    # Start patching all the files in the argument and store them in the same location as the original file with suffix "_patched"
    result = subprocess.run(['python3', METHOD_LEVEL_PATCHING_SCRIPT_PATH, project], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(files, 'w') as f:
        f.write(result.stdout.decode())
        f.write(result.stderr.decode())

    print("Starting measurement...")
    start_measurement.main()

    # run the patched files in the provided sequence in arguments

    # store the data and log

    # delete the patched file

    # stop measurement process

# only use this by uncommenting for testing purposes
if __name__ == "__main__":
    app()