# Python Chess Engine

## Description

- This is a simple chess engine written in Python. It uses the **minimax algorithm with alpha-beta pruning** to search the game tree.

- The engine uses **iterative deepening** to search the game tree upto the maximal depth possible in a given amount of time.

- The scores for each minimax level are decided by a robust evaluation function that takes into account the piece numbers, piece positions, piece mobility, pawn structure, centralization, castling bonus, king safety, etc.

- The engine is UCI compatible and can be played against another UCI compliant engine using arena.py

## How to run

- Run `python3 arena.py` to play engine 1 with engine 2. (both the engines are configured to Chess_Agent.py intially).

- To use your engine, import the necessary engine in arena.py and replace either white or black with your engine.

## References

- The engine base is inspired from the [Let's create a Chess AI](https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef)

- Additionally, the python-chess library can be looked up here: [python-chess](https://python-chess.readthedocs.io/en/latest/)