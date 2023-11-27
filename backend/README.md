# Ruliad Backend

This is the backend for the Ruliad project. It is a Python application that uses [FastAPI](https://fastapi.tiangolo.com/) to serve an API for generating and rendering trees based on a given grammar.

## CLI

```bash
$ poetry run python ruliad --help
Usage: ruliad [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  generate  Generate a graph from a grammar.
  serve     Serve the API.
```

### generate

```bash
$ poetry run python ruliad generate --help
Usage: ruliad generate [OPTIONS] GRAMMAR_PATH

  Generate a graph from a grammar.

Arguments:
  GRAMMAR_PATH  Path to the grammar file.  [required]

Options:
  --seed TEXT  The seed symbol to start from.
  --help       Show this message and exit.
```

### serve

```bash
$ poetry run python ruliad serve --help
Usage: ruliad serve [OPTIONS]

  Serve the API.

Options:
  --host TEXT     [default: localhost]
  --port INTEGER  [default: 8000]
  --help          Show this message and exit.
```

## API

```yml
openapi: 3.0.0
info:
  title: Grammar Tree API
  version: 1.0.0
description: API to generate and render trees based on provided grammars.
paths:
  /generate:
    post:
      summary: Generate a tree based on a given grammar and seed.
      operationId: generateTree
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                seed:
                  type: string
                  description: The seed symbol to start generating the tree.
                grammar:
                  type: string
                  description: The grammar string in CFG format.
                iterations:
                  type: integer
                  default: 5
                  description: The number of iterations for tree expansion.
      responses:
        '200':
          description: Successfully generated the tree.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tree'
        '400':
          description: Invalid input.

  /render:
    get:
      summary: Render a tree as a PNG image.
      operationId: renderTree
      parameters:
        - in: query
          name: tree
          required: true
          schema:
            $ref: '#/components/schemas/Tree'
          description: The tree to render.
      responses:
        '200':
          description: Successfully rendered the tree image.
          content:
            image/png:
              schema:
                type: string
                format: binary
        '400':
          description: Invalid input.

components:
  schemas:
    Tree:
      type: object
      oneOf:
        - $ref: '#/components/schemas/Leaf'
        - $ref: '#/components/schemas/Branch'
      description: A tree structure which is either a leaf or a branch.
    Leaf:
      type: string
      description: A leaf node in the tree.
    Branch:
      type: object
      required:
        - symbol
        - children
      properties:
        symbol:
          type: string
        children:
          type: array
          items:
            $ref: '#/components/schemas/Tree'
      description: A branch in the tree with a symbol and children nodes.
```


## Contributing

If you would like to contribute to this project, please feel free to fork the repository, create a feature branch, and then submit a pull request. We appreciate any and all contributions!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Other

If you have any questions or concerns, please open an issue or submit a pull request.

