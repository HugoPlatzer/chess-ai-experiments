#!/usr/bin/python3

import position
import sys

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
counter = 0

def evaluate(pos, depth):
    global counter
    pos.evaluateFully()
    counter += 1
    if depth > 0:
        for newPosition in pos.legalMoves.values():
            evaluate(newPosition, depth - 1)

p = position.Position(fen=fen)
evaluate(p, int(sys.argv[1]))
print(counter)
