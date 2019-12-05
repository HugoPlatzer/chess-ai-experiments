#!/usr/bin/python3

import position
import random, sys

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

random.seed(int(sys.argv[1]))
p = position.Position(fen=fen)
counter = 0
while True:
    p.evaluateFully()
    print(p)
    if not p.isValid():
        raise Exception
    print(p.movesAsStr())
    print()
    if len(p.legalMoves) == 0:
        break
    move = random.choice(list(p.legalMoves.keys()))
    print("doing move {}/{}: {}".format(counter // 2 +  1, p.player,
                                        position.moveToStr(move)))
    p = p.legalMoves[move]
    counter += 1
    
    
