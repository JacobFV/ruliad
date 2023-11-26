import typer

app = typer.Typer()

@app.command()
def main(name: str = typer.Option(..., prompt="Your name")):
    typer.echo(f"Hello {name}")
