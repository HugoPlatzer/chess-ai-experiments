import moves

class Position:
    def __init__(self, fen):
        fenParts = parseFEN(fen)
        self.board = fenParts[0]
        self.player = fenParts[1]
        self.castlingRights = fenParts[2]
        self.enpassantSquare = fenParts[3]
    
    
    def __str__(self):
        boardStr = "position:\n" + "\n".join(self.board)
        extraStr = "player = {}, castling = {}, enpassant = {}".format(
                self.player, self.castlingRights, self.enpassantSquare)
        return boardStr + "\n" + extraStr
    
    
    def getMoves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.isCurrentPlayer(row, col):
                    movesFromHere = self.pieceMovesFrom(row, col)
                    for move in movesFromHere:
                        moves.append((row, col, move[0], move[1], move[2]))
        return moves
    
    
    def movesAsStr(self):
        return str(list(moveToStr(m) for m in self.getMoves()))
    
    
    def isCurrentPlayer(self, row, col):
        return moves.isPlayer(self.board, row, col, self.player)
    
    
    def pieceMovesFrom(self, row, col):
        piece = self.board[row][col]
        if piece in ("r", "R"):
            return moves.rookMoves(self.board, row, col)
        elif piece in ("b", "B"):
            return moves.bishopMoves(self.board, row, col)
        elif piece in ("q", "Q"):
            return moves.queenMoves(self.board, row, col)
        elif piece in ("n", "N"):
            return moves.knightMoves(self.board, row, col, self.player)
        elif piece in ("p", "P"):
            return moves.pawnMoves(self.board, row, col,
                                   self.player, self.enpassantSquare)
        elif piece in ("k", "K"):
            return moves.kingMoves(self.board, row, col,
                                   self.player, self.castlingRights)
        else:
            return []



def parseSquare(s):
    if s == "-":
        return None
    return ("87654321".index(s[1]), "abcdefgh".index(s[0]))


def squareToStr(row, col):
    return "abcdefgh"[col] + "87654321"[row]


def moveToStr(m):
    s = squareToStr(m[0], m[1]) + squareToStr(m[2], m[3])
    if m[4] != None:
        s += m[4].upper()
    return s


def parseCastling(s):
    return [] if s == "-" else [c for c in s]


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
