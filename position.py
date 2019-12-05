import moves

class Position:
    def __init__(self, fen):
        fenParts = parseFEN(fen)
        self.board, self.player = fenParts[0], fenParts[1]
    
    
    def __str__(self):
        return "\n".join(self.board) + "\n" + self.player
    
    
    def getMoves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.isCurrentPlayer(row, col):
                    movesFromHere = self.pieceMovesFrom(row, col)
                    for move in movesFromHere:
                        moves.append(((row, col), move))
        return moves
    
    
    def movesAsStr(self):
        return str(list(moveToStr(m) for m in self.getMoves()))
    
    
    def isCurrentPlayer(self, row, col):
        return moves.isPlayer(self.board, row, col, self.player)
    
    
    def pieceMovesFrom(self, row, col):
        piece = self.board[row][col]
        if piece in ("r", "R"):
            return moves.rookMoves(self.board, row, col)
        if piece in ("b", "B"):
            return moves.bishopMoves(self.board, row, col)
        if piece in ("q", "Q"):
            return moves.queenMoves(self.board, row, col)
        if piece in ("n", "N"):
            return moves.knightMoves(self.board, row, col, self.player)
        return []



def parseSquare(s):
    if s == "-":
        return None
    return ("87654321".index(s[1]), "abcdefgh".index(s[0]))


def squareToStr(s):
    return "abcdefgh"[s[1]] + "87654321"[s[0]]


def moveToStr(m):
    return squareToStr(m[0]) + squareToStr(m[1])


def parseCastling(s):
    return "" if s == "-" else s


def parseFENBoard(b):
    def expandRow(r):
        e = ""
        for c in r:
            if c.isdigit():
                e += "-" * int(c)
            else:
                e += c
        return e    
    
    rows = b.split("/")
    return [expandRow(r) for r in rows]


def parseFEN(fen):
    parts = fen.split(" ")
    boardRows = parseFENBoard(parts[0])
    player = parts[1]
    castlingRights = parseCastling(parts[2])
    enpassantSquare = parseSquare(parts[3])
    halfmoveClock = int(parts[4])
    fullmoveNumber = int(parts[5])
    return (boardRows, player, castlingRights,
            enpassantSquare, halfmoveClock, fullmoveNumber)
