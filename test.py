#!/usr/bin/python3

import position

#fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen = "3rk3/ppp1b1pp/8/5r2/3Pp3/4P1nP/PPPKN2R/RN6 b - - 1 19"
#fen = "r2qkb1r/ppp2ppp/2n2n2/6B1/3Pp1b1/4P1P1/PPP3BP/RN1QK1NR w KQkq - 1 8"

p = position.Position(fen)
print(p)
print(p.movesAsStr())
