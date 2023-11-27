from fastapi import FastAPI
from pydantic import BaseModel
from typer import Typer
import nltk
import networkx as nx
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from io import BytesIO
import uvicorn
import typer

cli = Typer()
api = FastAPI()

Leaf = str
Branch = tuple[str, list["Tree"]]  # (symbol, children)
Tree = Leaf | Branch


def expand(state: str, grammar: nltk.grammar.CFG, depth=None) -> Tree:
    """Expand a state using a grammar. DFS. Recursive."""
    if depth == 0:
        return
    else:
        productions = grammar.productions(lhs=state)
        for production in productions:
            for symbol in production.rhs():
                if isinstance(symbol, nltk.grammar.Nonterminal):
                    yield from expand(symbol, grammar, depth - 1 if depth else None)
                else:
                    yield symbol


def tree_to_graph(tree: Tree) -> nx.Graph:
    G = nx.Graph()
    if isinstance(tree, str):
        G.add_node(tree)
    else:
        symbol, children = tree
        G.add_node(symbol)
        for child in children:
            G.add_edge(symbol, child)
    return G


@api.post("/generate")
def generate(
    seed: str,
    grammar: str,
    iterations: int = 5,
) -> Tree:
    cfg = nltk.CFG.fromstring(grammar)
    return list(expand(seed, cfg, iterations))


@api.get("/render", response_class=StreamingResponse)
def render_tree(tree: Tree):
    G = tree_to_graph(tree)

    # Create a BytesIO object to save the image
    img = BytesIO()
    nx.draw(G, with_labels=True)
    plt.savefig(img, format="png")
    plt.close()

    # Seek to the start of the stream
    img.seek(0)

    # Create a StreamingResponse returning the image in PNG format
    return StreamingResponse(img, media_type="image/png")


@cli.command()
def generate(
    grammar_path: str = typer.Argument(..., help="Path to the grammar file."),
    seed: str = typer.Option(None, help="The seed symbol to start from."),
):
    """Generate a graph from a grammar."""
    with open(grammar_path) as f:
        grammar = f.read()
    cfg = nltk.CFG.fromstring(grammar)
    if seed is None:
        seed = cfg.start()
    tree = list(expand(seed, cfg))
    G = tree_to_graph(tree)
    nx.draw(G, with_labels=True)
    plt.show()


@cli.command()
def serve(
    host: str = typer.Option("localhost"),
    port: int = typer.Option(8000),
):
    """Serve the API."""
    uvicorn.run(api, host=host, port=port)


if __name__ == "__main__":
    cli()
