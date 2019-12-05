#!/usr/bin/python3

import position

#fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#fen = "3rk3/ppp1b1pp/8/5r2/3Pp3/4P1nP/PPPKN2R/RN6 b - - 1 19"
#fen = "r2qkb1r/ppp2ppp/2n2n2/6B1/3Pp1b1/4P1P1/PPP3BP/RN1QK1NR w KQkq - 1 8"
fen = "3rk2r/ppp1b1pp/4B3/4np2/3Pp3/4P1P1/PPP4P/RN1K2NR b k - 5 13"
#fen = "8/3KPk2/8/8/8/8/8/8 w - - 0 1"

p = position.Position(fen)
print(p)
print(p.movesAsStr())
