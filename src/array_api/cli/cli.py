import typer

from ._main import generate

app = typer.Typer()


@app.command()
def main() -> None:
    """Add the arguments and print the result."""
    generate()
