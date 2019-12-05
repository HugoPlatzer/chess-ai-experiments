import moves

squares = [(row, col) for row in range(8) for col in range(8)]

class Position:
    def __init__(self, *args, **kwargs):
        if "fen" in kwargs:
            fenParts = parseFEN(kwargs["fen"])
            self.board = fenParts[0]
            self.player = fenParts[1]
            self.castlingRights = fenParts[2]
            self.enpassantSquare = fenParts[3]
        elif "copyOf" in kwargs:
            copyOf = kwargs["copyOf"]
            self.board = [[piece for piece in row] for row in copyOf.board]
            self.player = copyOf.player
            self.castlingRights = copyOf.castlingRights[:]
            self.enpassantSquare = copyOf.enpassantSquare
        else:
            raise Exception
        
        self.allMoves = None
        self.legalMoves = None
        self.kings = None
        self.status = None
    
    
    def __str__(self):
        boardStr = "position:\n" + boardToStr(self.board)
        extraStr = ("player = {}, castling = {}, enpassant = {}"
                    " valid = {} status = {}").format(
                self.player,
                castlingToStr(self.castlingRights),
                squareToStr(self.enpassantSquare),
                self.isValid(),
                self.status)
        return boardStr + "\n" + extraStr
    
    
    def executeMove(self, fromRow, fromCol, toRow, toCol, promotion):
        piece = self.board[fromRow][fromCol]
        
        self.board[fromRow][fromCol] = "-"
        if promotion == None:
            self.board[toRow][toCol] = piece
        elif self.player == "w":
            self.board[toRow][toCol] = promotion.upper()
        else:
            self.board[toRow][toCol] = promotion.lower()
         
        if piece in ("p", "P") and (toRow, toCol) == self.enpassantSquare:
            direction = 1 if piece == "p" else -1
            captureRow = toRow - direction
            self.board[captureRow][toCol] = "-"
        
        if piece in ("k", "K") and (fromCol - toCol) in (-2, 2):
            if toRow == 0 and toCol == 2:
                self.board[0][0] = "-"
                self.board[0][3] = "r"
            elif toRow == 0 and toCol == 6:
                self.board[0][7] = "-"
                self.board[0][5] = "r"
            elif toRow == 7 and toCol == 2:
                self.board[7][0] = "-"
                self.board[7][3] = "R"
            elif toRow == 7 and toCol == 6:
                self.board[7][7] = "-"
                self.board[7][5] = "R"
        
        if (fromRow, fromCol) == (0, 4) or (toRow, fromCol) == (0, 4):
            self.removeCastling(("k", "q"))
        elif (fromRow, fromCol) == (7, 4) or (toRow, fromCol) == (7, 4):
            self.removeCastling(("K", "Q"))
        elif (fromRow, fromCol) == (0, 0) or (toRow, fromCol) == (0, 0):
            self.removeCastling(("k",))
        elif (fromRow, fromCol) == (0, 7) or (toRow, fromCol) == (0, 7):
            self.removeCastling(("q",))
        elif (fromRow, fromCol) == (7, 0) or (toRow, fromCol) == (7, 0):
            self.removeCastling(("K",))
        elif (fromRow, fromCol) == (7, 7) or (toRow, fromCol) == (7, 7):
            self.removeCastling(("Q",))
        
        if piece == "p" and toRow == fromRow + 2:
            self.enpassantSquare = (fromRow + 1, fromCol)
        elif piece == "P" and toRow == fromRow - 2:
            self.enpassantSquare = (fromRow - 1, fromCol)
        else:
            self.enpassantSquare = None
        
        self.player = moves.opponentOf(self.player)
        self.allMoves = None
        self.legalMoves = None
        self.kings = None
        self.status = None
    
    
    def findKings(self):
        if self.kings != None:
            return
        self.kings = moves.findKings(self.board)
    
    
    def removeCastling(self, options):
        for option in options:
            try:
                self.castlingRights.remove(option)
            except ValueError:
                pass
    
    
    def evaluatePartially(self):
        if self.allMoves != None:
            return
        self.findKings()
        self.allMoves = {}
        for row, col in squares:
            if self.isCurrentPlayer(row, col):
                movesFromHere = self.pieceMovesFrom(row, col)
                for toMove in movesFromHere:
                    move = (row, col, toMove[0], toMove[1], toMove[2])
                    newPosition = Position(copyOf=self)
                    newPosition.executeMove(*move)
                    self.allMoves[move] = newPosition
    
    
    def evaluateFully(self):
        if self.legalMoves != None:
            return
        self.evaluatePartially()
        self.legalMoves = {}
        for move, newPosition in self.allMoves.items():
            newPosition.evaluatePartially()
            importantSquares = [newPosition.kings[self.player]]
            fromRow, fromCol, toRow, toCol = move[0:4]
            piece = self.board[fromRow][fromCol]
            if piece == "K" and toRow == fromRow - 2:
                importantSquares.append((7, 4))
                importantSquares.append((7, 3))
            elif piece == "K" and toRow == fromRow + 2:
                importantSquares.append((7, 4))
                importantSquares.append((7, 5))
            elif piece == "k" and toRow == fromRow - 2:
                importantSquares.append((0, 4))
                importantSquares.append((0, 3))
            elif piece == "k" and toRow == fromRow + 2:
                importantSquares.append((0, 4))
                importantSquares.append((0, 5))
            if all(not newPosition.isSquareAttacked(*s)
                   for s in importantSquares):
                self.legalMoves[move] = newPosition
        self.findStatus()
    
    
    def isSquareAttacked(self, row, col):
        self.evaluatePartially()
        return any(m[2] == row and m[3] == col for m in self.allMoves)
   
    
    def movesAsStr(self):
        self.evaluateFully()
        return str(list(moveToStr(m) for m in self.legalMoves))
    
    
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
    
    
    def isValid(self):
        pieces = ["K", "k", "Q", "q", "B", "b", "N", "n", "R", "r", "P", "p", "-"]
        if len(self.board) != 8:
            return False
        if any(len(row) != 8 for row in self.board):
            return False
        if any(p not in pieces for row in self.board for p in row):
            return False
        if any(p in ("P", "p") for p in self.board[0]):
            return False
        if any(p in ("P", "p") for p in self.board[7]):
            return False
        blackKings = sum(1 for row in self.board for p in row if p == "k")
        if blackKings != 1:
            return False
        whiteKings = sum(1 for row in self.board for p in row if p == "K")
        if whiteKings != 1:
            return False
        self.evaluatePartially()
        kingSquare = moves.findKings(self.board)[moves.opponentOf(self.player)]
        if self.isSquareAttacked(*kingSquare):
            return False
        return True
    
    
    def findStatus(self):
        if self.status != None:
            return
        self.evaluateFully()
        testBoard = Position(copyOf=self)
        testBoard.player = moves.opponentOf(self.player)
        testBoard.evaluatePartially()
        if testBoard.isSquareAttacked(*self.kings[self.player]):
            if len(self.legalMoves) > 0:
                self.status = "check"
            else:
                self.status = "checkmate"
        elif len(self.legalMoves) == 0:
            self.status = "stalemate"
        else:
            self.status = "normal"


def parseSquare(s):
    if s == "-":
        return None
    return ("87654321".index(s[1]), "abcdefgh".index(s[0]))


def squareToStr(q):
    if q == None:
        return "-"
    return "abcdefgh"[q[1]] + "87654321"[q[0]]


def parseMove(s):
    fromSquare = parseSquare(s[0:2])
    toSquare = parseSquare(s[2:4])
    promotion = s[4] if len(s) == 5 else None
    return (fromSquare[0], fromSquare[1], toSquare[0], toSquare[1],
            promotion)


def moveToStr(m):
    s = squareToStr((m[0], m[1])) + squareToStr((m[2], m[3]))
    if m[4] != None:
        s += m[4].upper()
    return s


def boardToStr(b):
    return "\n".join("".join(p for p in row) for row in b)


def parseCastling(s):
    return [] if s == "-" else [c for c in s]


def castlingToStr(c):
    if c == []:
        return "-"
    return "".join(c)


def parseFENBoard(s):
    def expandRow(r):
        e = []
        for c in r:
            if c.isdigit():
                for i in range(int(c)):
                    e.append("-")
            else:
                e.append(c)
        return e    
    
    rows = s.split("/")
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
