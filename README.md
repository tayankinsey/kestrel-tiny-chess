# Kestrel 30k

A deterministic, 30,000-node-budget chess engine for `tiny-chess-01`.

The self-contained Python source implements legal move generation, castling, en passant, promotion, alpha-beta negamax, iterative deepening, quiescence search, a transposition table, and material/positional evaluation. `main.py` is the LZMA-packed entrypoint; `engine.py` is the readable source used to produce it.

Licensed under GPL-3.0-only.
