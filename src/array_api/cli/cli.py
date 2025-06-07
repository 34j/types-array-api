import typer

from ._main import generate_all

app = typer.Typer()


@app.command()
def main() -> None:
    """Add the arguments and print the result."""
    generate_all()
