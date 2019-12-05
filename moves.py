squares = [(row, col) for row in range(8) for col in range(8)]


def opponentOf(player):
    return "b" if player == "w" else "w"


def areOpponents(b, row1, col1, row2, col2):
    if b[row1][col1].isupper() and b[row2][col2].islower():
        return True
    if b[row1][col1].islower() and b[row2][col2].isupper():
        return True
    return False


def isValidCoord(row, col):
    return (row >= 0 and col >= 0 and row < 8 and col < 8)


def isFree(b, row, col):
    return (b[row][col] == "-")


def isPlayer(b, row, col, player):
    if player == "w" and b[row][col].isupper():
        return True
    if player == "b" and b[row][col].islower():
        return True
    return False


def rookMoves(b, row, col):
    moves = []
    
    mrow = row + 1
    while isValidCoord(mrow, col) and isFree(b, mrow, col):
        moves.append((mrow, col, None))
        mrow += 1
    if isValidCoord(mrow, col) and areOpponents(b, row, col, mrow, col):
        moves.append((mrow, col, None))
    
    mrow = row - 1
    while isValidCoord(mrow, col) and isFree(b, mrow, col):
        moves.append((mrow, col, None))
        mrow -= 1
    if isValidCoord(mrow, col) and areOpponents(b, row, col, mrow, col):
        moves.append((mrow, col, None))
    
    mcol = col + 1
    while isValidCoord(row, mcol) and isFree(b, row, mcol):
        moves.append((row, mcol, None))
        mcol += 1
    if isValidCoord(row, mcol) and areOpponents(b, row, col, row, mcol):
        moves.append((row, mcol, None))
    
    mcol = col - 1
    while isValidCoord(row, mcol) and isFree(b, row, mcol):
        moves.append((row, mcol, None))
        mcol -= 1
    if isValidCoord(row, mcol) and areOpponents(b, row, col, row, mcol):
        moves.append((row, mcol, None))
    
    return moves


def bishopMoves(b, row, col):
    moves = []
    
    mrow, mcol = row + 1, col + 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol, None))
        mrow, mcol =  mrow + 1, mcol + 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol, None))
    
    mrow, mcol = row + 1, col - 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol, None))
        mrow, mcol =  mrow + 1, mcol - 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol, None))
    
    mrow, mcol = row - 1, col + 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol, None))
        mrow, mcol =  mrow - 1, mcol + 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol, None))
    
    mrow, mcol = row - 1, col - 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol, None))
        mrow, mcol =  mrow - 1, mcol - 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol, None))
    
    return moves


def queenMoves(b, row, col):
    return rookMoves(b, row, col) + bishopMoves(b, row, col)


def knightMoves(b, row, col, player):
    candidates = [(row + 2, col + 1, None), (row + 2, col - 1, None),
                  (row - 2, col + 1, None), (row - 2, col - 1, None),
                  (row + 1, col + 2, None), (row + 1, col - 2, None),
                  (row - 1, col + 2, None), (row - 1, col - 2, None)]
    return [c for c in candidates if isValidCoord(c[0], c[1])
                                     and not isPlayer(b, c[0], c[1], player)]


def pawnMoves(b, row, col, player, enpSquare):
    moves = []
    direction = 1 if player == "b" else -1
    
    if isFree(b, row + direction, col):
        moves.append((row + direction, col))
        if (((player == "w" and row == 6) or (player == "b" and row == 1))
                 and isFree(b, row + 2 * direction, col)):
            moves.append((row + 2 * direction, col))
    
    if (        isValidCoord(row + direction, col + 1)
            and areOpponents(b, row, col, row + direction, col + 1)):
        moves.append((row + direction, col + 1))
    if (        isValidCoord(row + direction, col - 1)
            and areOpponents(b, row, col, row + direction, col - 1)):
        moves.append((row + direction, col - 1))
    
    if (       enpSquare == (row + direction, col - 1)
            or enpSquare == (row + direction, col + 1)):
        moves.append(enpSquare)
    
    promoMoves = []
    for m in moves:
        if m[0] == 0 or m[0] == 7:
            promoMoves.append((m[0], m[1], "Q"))
            promoMoves.append((m[0], m[1], "N"))
            promoMoves.append((m[0], m[1], "R"))
            promoMoves.append((m[0], m[1], "B"))
        else:
            promoMoves.append((m[0], m[1], None))
    
    return promoMoves


def kingMoves(b, row, col, player, castling):
    candidates = [(row + 1, col + 1, None), (row + 1, col, None),
                  (row + 1, col - 1, None), (row, col + 1, None),
                  (row, col - 1, None), (row - 1, col + 1, None),
                  (row - 1, col, None), (row - 1, col - 1, None)]
    moves = [c for c in candidates if isValidCoord(c[0], c[1])
                              and not isPlayer(b, c[0], c[1], player)]
    if player == "w":
        if "K" in castling and isFree(b, 7, 5) and isFree(b, 7, 6):
            moves.append((7, 6, None))
        if ("Q" in castling and isFree(b, 7, 3)
                and isFree(b, 7, 2) and isFree(b, 7, 1)):
            moves.append((7, 2, None))
    elif player == "b":
        if "k" in castling and isFree(b, 0, 5) and isFree(b, 0, 6):
            moves.append((0, 6, None))
        if ("q" in castling and isFree(b, 0, 3)
                and isFree(b, 0, 2) and isFree(b, 0, 1)):
            moves.append((0, 2, None))
    return moves


def findKings(b):
    kings = {}
    for row, col in squares:
        if b[row][col] == "K":
            kings["w"] = (row, col)
        elif b[row][col] == "k":
            kings["b"] = (row, col)
    return kings
