class  GreedyPlayer():
    def __init__(self):
        return
    def calculate(self,movelist,gameboard):
        max = 0
        move = False
        for moves in movelist:
            if moves[2] > max:
                max = moves[2]
                move = moves
        return move
