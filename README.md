# QServer

Quantum computer simulation server for
[Proto-Quipper](https://gitlab.com/frank-peng-fu/dpq-remake) language.

- To set up a virtual environment run
    ```
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

- To start the development server run
    ```
    scripts/dev.sh
    ```

- To run the unit tests (after starting the dev server) run
    ```
    scripts/test.sh
    ```

- Sometimes Python sub-processes can hang on after the main server process
is killed. If this happens, run
    ```
    scripts/kill.sh
    ```
    to kill all processes using port 1901.