#!/usr/bin/python3

import position, tree_minmax, evaluators
import sys

#fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen = "8/p5p1/1b5k/1R5p/PP6/2P4P/4rrPK/1R6 b - - 3 30"

p = position.Position(fen=fen)
ev = evaluators.evalMaterialistic
bestMove = tree_minmax.minmax(p, ev, depth=5)
print(bestMove.score, position.moveToStr(bestMove.move))
