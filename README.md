# Kestrel — 2.7 KB chess engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/tayankinsey/kestrel-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/tayankinsey/kestrel-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Entry for [make.fun](https://make.fun/bounty/tiny-chess-01)'s “Build the strongest chess engine in 4 KB of Python” bounty.

`main.py` (2,723 bytes) is the LZMA-packed entrypoint. It speaks the trial's HTTP protocol, plays
whatever the env serves, and answers `{"move": "<uci>"}` — no model calls, no clock, no randomness,
so a trial replays byte for byte.

The engine inside: legal move generation (castling, en passant, under-promotion), alpha-beta
negamax with iterative deepening, a transposition table, quiescence search, move ordering, and
material plus piece-square evaluation, on a 75,000-node budget per move (worst case ≈4.7 s locally,
under the 10 s move limit).

Run it the way the env does:

```
MAKEFUN_ENV_URL=<env url> python3 -P -s main.py
```

Licensed under MIT.
