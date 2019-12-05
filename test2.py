#!/usr/bin/python3

import position
import random, sys

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

games = 0
while games < int(sys.argv[1]):
    counter = 0
    p = position.Position(fen=fen)
    while counter < int(sys.argv[2]):
        p.evaluateFully()
        if len(p.legalMoves) == 0:
            break
        move = random.choice(list(p.legalMoves.keys()))
        p = p.legalMoves[move]
        counter += 1
    games += 1
