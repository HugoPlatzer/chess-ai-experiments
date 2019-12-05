from collections import namedtuple
Move = namedtuple("Move", ["move", "score"])

def minmax(pos, evaluator, depth):
    if depth == 1:
        pos.evaluatePartially()
        scores = (Move(move, evaluator(newPos))
                  for move, newPos in pos.allMoves.items())
        default = Move(None, 0)
        if pos.player == "b":
            return min(scores, key=lambda m: m.score, default=default)
        else:
            return max(scores, key=lambda m: m.score, default=default)
    else:
        pos.evaluateFully()
        if len(pos.legalMoves) == 0:
            if pos.status == "checkmate":
                if pos.player == "b":
                    return Move(None, 1000)
                else:
                    return Move(None, -1000)
            else:
                return Move(None, 0)
        else:
            scores = (Move(move, minmax(newPos, evaluator, depth - 1).score)
                      for move, newPos in pos.legalMoves.items())
            if pos.player == "b":
                return min(scores, key=lambda m: m.score)
            else:
                return max(scores, key=lambda m: m.score)
