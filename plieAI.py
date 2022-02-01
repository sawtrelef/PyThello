from random import sample
from copy import deepcopy
from test import Gameboard, Space
class  PliePlayer():
    def __init__(self):
        return
    def calculate(self,movelist,gameboard):
        maxi = 0
        move = []

        for moves in movelist:
            result = self.dig_move(gameboard, 1, moves)
            if result > maxi:
                maxi = result
                moves[2] = maxi

        for moves in movelist:
            if moves[2] == maxi:
                move.append(moves)

        if len(move) > 0:
            return sample(move,1)[0]

    #returns number of highest scoring move
    def calculate_greedy(self, movelist):
        maxi = 0
        for moves in movelist:
            if moves[2] > maxi:
                maxi = moves[2]
        return maxi


    #def do_move(self,player, move):
    #def find_legal_moves(self, player):
    def dig_move(self, gameboard, count, move):
        movelist = []
        if count == 0:
            legalmoves = gameboard.find_legal_moves("B")
            for coord, list in legalmoves.items():
                movelist.append((coord, list[0], list[1]))
            highestMoves = self.calculate_greedy(movelist)
            squaresOwned = gameboard.space_count()[1]
            return squaresOwned+highestMoves

        movelist = []
        resultlist = []
        gameboard2 = deepcopy(gameboard)
        gameboard2.do_move("B", move)
        legalmoves = gameboard2.find_legal_moves("W")
        for coord, list in legalmoves.items():
            movelist.append((coord, list[0], list[1]))
        for move in movelist:
            resultlist.append(self.dig_opponent_move(gameboard2, count, move))
        return self.biggest(resultlist)

    def dig_opponent_move(self, gameboard, count, move):
        movelist = []
        resultlist = []
        gameboard2 = deepcopy(gameboard)
        gameboard2.do_move("W", move)
        legalmoves = gameboard2.find_legal_moves("B")
        for coord, list in legalmoves.items():
                movelist.append((coord, list[0], list[1]))
        for move in movelist:
            resultlist.append(self.dig_move(gameboard2, count - 1, move))
        return self.biggest(resultlist)

    def biggest(self,results):
        most = 0
        for result in results:
            if result > most:
                most = result

        return most
