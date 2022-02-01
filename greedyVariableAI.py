from random import sample

class  GreedyVariablePlayer():
    def __init__(self):
        return
    def calculate(self,movelist,gameboard):
        maxi = 0
        move = []
        for moves in movelist:
            if moves[2] > maxi:
                maxi = moves[2]

        for moves in movelist:
            if moves[2] == maxi:
                move.append(moves)

        if len(move) > 0:
            return sample(move,1)[0]

        return move
