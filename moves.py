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
        moves.append((mrow, col))
        mrow += 1
    if isValidCoord(mrow, col) and areOpponents(b, row, col, mrow, col):
        moves.append((mrow, col))
    
    mrow = row - 1
    while isValidCoord(mrow, col) and isFree(b, mrow, col):
        moves.append((mrow, col))
        mrow -= 1
    if isValidCoord(mrow, col) and areOpponents(b, row, col, mrow, col):
        moves.append((mrow, col))
    
    mcol = col + 1
    while isValidCoord(row, mcol) and isFree(b, row, mcol):
        moves.append((row, mcol))
        mcol += 1
    if isValidCoord(row, mcol) and areOpponents(b, row, col, row, mcol):
        moves.append((row, mcol))
    
    mcol = col - 1
    while isValidCoord(row, mcol) and isFree(b, row, mcol):
        moves.append((row, mcol))
        mcol -= 1
    if isValidCoord(row, mcol) and areOpponents(b, row, col, row, mcol):
        moves.append((row, mcol))
    
    return moves


def bishopMoves(b, row, col):
    moves = []
    
    mrow, mcol = row + 1, col + 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol))
        mrow, mcol =  mrow + 1, mcol + 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol))
    
    mrow, mcol = row + 1, col - 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol))
        mrow, mcol =  mrow + 1, mcol - 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol))
    
    mrow, mcol = row - 1, col + 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol))
        mrow, mcol =  mrow - 1, mcol + 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol))
    
    mrow, mcol = row - 1, col - 1
    while isValidCoord(mrow, mcol) and isFree(b, mrow, mcol):
        moves.append((mrow, mcol))
        mrow, mcol =  mrow - 1, mcol - 1
    if isValidCoord(mrow, mcol) and areOpponents(b, row, col, mrow, mcol):
        moves.append((mrow, mcol))
    
    return moves


def queenMoves(b, row, col):
    return rookMoves(b, row, col) + bishopMoves(b, row, col)


def knightMoves(b, row, col, player):
    candidates = [(row + 2, col + 1), (row + 2, col - 1),
                  (row - 2, col + 1), (row - 2, col - 1),
                  (row + 1, col + 2), (row + 1, col - 2),
                  (row - 1, col + 2), (row - 1, col - 2)]
    return [c for c in candidates if isValidCoord(c[0], c[1])
                                     and not isPlayer(b, c[0], c[1], player)]
