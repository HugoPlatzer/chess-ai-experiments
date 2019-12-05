def evalMaterialistic(pos):
    mapping = {"R" : 5, "N" : 3, "B" : 3, "Q" : 9, "P" : 1,
               "r" : -5, "n" : -3, "b" : -3, "q" : -9, "p" : -1,
               "K" : 0, "k" : 0, "-" : 0}
    return sum(mapping[p] for row in pos.board for p in row)
