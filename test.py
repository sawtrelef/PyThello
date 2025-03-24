import randyAI
import greedyAI
import pygame
import greedyVariableAI
import plieAI
from time import sleep
import test2

class Gameboard():
    def __init__(self):
        self.gameboard = [[], [], [], [], [], [], [], []]
        for x in range(0, 8):
            self.gameboard[x] = [Space(), Space(), Space(), Space(), Space(), Space(), Space(), Space()]
        for x in range(0, 8):
            for y in range(0, 8):
                self.gameboard[x][y].set_coords(x, y)

        self.gameboard[3][3].set_color('W')
        self.gameboard[3][4].set_color('B')
        self.gameboard[4][4].set_color('W')
        self.gameboard[4][3].set_color('B')

    #find_legal_moves generates a dictionary containing the legal moves on a board for a player
    #Returns:
    # Dictionary using coordinates found to be legal as keys
    #  Keys contain a list of directions they were found in
    #  total count of spaces a player would gain making the move

    def clean_board(self):
        for x in self.gameboard:
            for y in x:
                if y.get_color() == "L":
                    y.set_color("x")

    def find_legal_moves(self, player):
        legalmoves = {}
        for x in self.gameboard:
            for y in x:
                if y.get_color() == player:
                    coords = y.get_coords()
                    if coords[1] > 1:
                        up = self.gameboard[coords[0]][coords[1] - 1].find_legal_up(self.gameboard, y, 0)
                        if up != False:
                            self.add_to_dictionary(legalmoves, up)
                    if coords[1] < 6:
                        down = self.gameboard[coords[0]][coords[1] + 1].find_legal_down(self.gameboard, y, 0)
                        if down != False:
                            self.add_to_dictionary(legalmoves, down)
                    if coords[0] > 1:
                        left = self.gameboard[coords[0] - 1][coords[1]].find_legal_left(self.gameboard, y, 0)
                        if left != False:
                            self.add_to_dictionary(legalmoves, left)
                    if coords[0] < 6:
                        right = self.gameboard[coords[0] + 1][coords[1]].find_legal_right(self.gameboard, y, 0)
                        if right != False:
                            self.add_to_dictionary(legalmoves, right)
                    if coords[1] > 1 and coords[0] > 1:
                        upleft = self.gameboard[coords[0] - 1][coords[1] - 1].find_legal_up_left(self.gameboard, y, 0)
                        if upleft != False:
                            self.add_to_dictionary(legalmoves, upleft)
                    if coords[1] > 1 and coords[0] < 6:
                        upright = self.gameboard[coords[0] + 1][coords[1] - 1].find_legal_up_right(self.gameboard, y, 0)
                        if upright != False:
                            self.add_to_dictionary(legalmoves, upright)
                    if coords[1] < 6 and coords[0] < 6:
                        downright = self.gameboard[coords[0] + 1][coords[1] + 1].find_legal_down_right(self.gameboard, y, 0)
                        if downright != False:
                            self.add_to_dictionary(legalmoves, downright)
                    if coords[1] < 6 and coords[0] > 1:
                        downleft = self.gameboard[coords[0] - 1][coords[1] + 1].find_legal_down_left(self.gameboard, y, 0)
                        if downleft != False:
                            self.add_to_dictionary(legalmoves, downleft)

        return legalmoves

    def add_to_dictionary(self,dictionary,item):
        if item[0] in dictionary:
            dictionary[item[0]][0].append(item[2])
            dictionary[item[0]][1] = dictionary[item[0]][1] + item[1]

        else:
            dictionary[item[0]] = [[item[2]], item[1]+1]

    #takes a legal move and executes it
    #move is ((0,0),["up", "down"])
    def do_move(self,player, move):
        x = move[0][0]
        y = move[0][1]
        directions = move[1]
        self.gameboard[x][y].do_move(directions,player,self.gameboard)
        self.clean_board()

    def space_count(self):
        white = 0
        black = 0
        for x in self.gameboard:
            for y in x:
                if y.get_color() == "W":
                    white = white + 1
                elif y.get_color() == "B":
                    black = black + 1
        return (white, black)

    def get_board(self):
        return self.gameboard
    def set_board(self, gameboard):
        self.gameboard = gameboard

    def get_space(self,x,y):
        return self.gameboard[x][y]


class Space():
    def __init__(self):
        self.y = 0
        self.x = 0
        self.color = 'x'

    def __str__(self):
        return f"{self.color}"

    def set_color(self, newColor):
        self.color = newColor

    def set_coords(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord

    def get_coords(self):
        return (self.x, self.y)

    def get_color(self):
            return self.color

    #Find_legal_whatever returns the following:
    # Coords of the space we found
    # Count of spaces it would gain
    # Direction it was found in
    # False if the direction does not contain a legal move
    def find_legal_up(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "up")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "up")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 0:
            return False
        return board[self.x][self.y - 1].find_legal_up(board, space, count + 1)
    def find_legal_down(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "down")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "down")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 7:
            return False
        return board[self.x][self.y + 1].find_legal_down(board, space, count + 1)
    def find_legal_right(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "right")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "right")
        if self.color == 'x' and count < 1:
            return False
        if self.x == 7:
            return False
        return board[self.x + 1][self.y].find_legal_right(board, space, count + 1)
    def find_legal_left(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "left")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "left")
        if self.color == 'x' and count < 1:
            return False
        if self.x == 0:
            return False
        return board[self.x - 1][self.y].find_legal_left(board, space, count + 1)
    def find_legal_up_left(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "upleft")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "upleft")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 0 or self.x == 0:
            return False
        return board[self.x - 1][self.y - 1].find_legal_up_left(board, space, count + 1)
    def find_legal_up_right(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "upright")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "upright")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 0 or self.x == 7:
            return False
        return board[self.x + 1][self.y - 1].find_legal_up_right(board, space, count + 1)
    def find_legal_down_left(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "downleft")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "downleft")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 7 or self.x == 0:
            return False
        return board[self.x - 1][self.y + 1].find_legal_down_left(board, space, count + 1)
    def find_legal_down_right(self,board,space,count):
        if self.color == space.get_color():
            return False
        if self.color == 'L':
            if count > 0:
                return (self.get_coords(), count, "downright")
            return False
        if self.color == 'x' and count > 0:
            self.set_color('L')
            return (self.get_coords(), count, "downright")
        if self.color == 'x' and count < 1:
            return False
        if self.y == 7 or self.x == 7:
            return False
        return board[self.x + 1][self.y + 1].find_legal_down_right(board, space, count + 1)

    def do_move(self,directions,player,board):
        self.set_color(player)
        for dir in directions:
            if dir == "up":
                board[self.x][self.y + 1].transform_down(player, board)
            elif dir == "down":
                board[self.x][self.y - 1].transform_up(player, board)
            elif dir == "left":
                board[self.x + 1][self.y].transform_right(player, board)
            elif dir == "right":
                board[self.x - 1][self.y].transform_left(player, board)
            elif dir == "upleft":
                board[self.x + 1][self.y + 1].transform_downright(player, board)
            elif dir == "upright":
                board[self.x - 1][self.y + 1].transform_downleft(player, board)
            elif dir == "downleft":
                board[self.x + 1][self.y - 1].transform_upright(player, board)
            elif dir == "downright":
                board[self.x - 1][self.y - 1].transform_upleft(player, board)

    def transform_up(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x][self.y - 1].transform_up(player, board)
    def transform_down(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x][self.y + 1].transform_down(player, board)
    def transform_left(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x - 1][self.y].transform_left(player, board)
    def transform_right(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x + 1][self.y].transform_right(player, board)
    def transform_upleft(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x - 1][self.y - 1].transform_upleft(player, board)
    def transform_upright(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x + 1][self.y - 1].transform_upright(player, board)
    def transform_downleft(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x - 1][self.y + 1].transform_downleft(player, board)
    def transform_downright(self,player, board):
        if self.color != player:
            self.set_color(player)
            board[self.x + 1][self.y + 1].transform_downright(player, board)

class SpaceSprite(pygame.sprite.Sprite):
    def __init__(self, space):
        self.space = space
        super().__init__()
        self.image = pygame.image.load("OthelloSprites/blankspace.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = space.x * 32
        self.rect.y = space.y * 32

    def set_color(self):
        if self.space.get_color() == 'B':
            self.image = pygame.image.load("OthelloSprites/blackspace.png").convert()
        elif self.space.get_color() == 'W':
            self.image = pygame.image.load("OthelloSprites/whitespace.png").convert()
        elif self.space.get_color() == 'L':
            self.image = pygame.image.load("OthelloSprites/legalspace.png").convert()
        elif self.space.get_color() == 'x':
            self.image = pygame.image.load("OthelloSprites/blankspace.png").convert()

    def handle_event(self,event, player=""):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.space.get_color() == "L":
                    return self.space.get_coords()
                return False

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return False

        return True
class GameButt(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, game):
        super().__init__()
        self.image = pygame.image.load(sprite).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = game

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.type
        return False


def find_move(movelist, coord):
    for move in movelist:
        if move[0] == coord:
            return move
    return False

#def display_white_win:

#def display_black_win:

#def display_tie:



# define a main function
def pvp(screen):
    # load and set the logo
    pygame.display.set_caption("Player vs Player")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((380, 256))

    # define a variable to control the main loop
    running = True
    sprite_handler = []
    all_sprites_list = pygame.sprite.Group()
    check_object_events = []

    player1 = "W"
    player2 = "B"
    activeplayer = player1
    inactiveplayer = player2

    passcount = 0

    gameboard = Gameboard()
    for x in range(0,8):
        for y in range(0,8):
            tmp = SpaceSprite(gameboard.get_space(x,y))
            tmp.set_color()
            sprite_handler.append(tmp)
            all_sprites_list.add(tmp)
            check_object_events.append(tmp)
    # main loop
    while running:
        moved = False
        tmp = inactiveplayer
        legalmoves = gameboard.find_legal_moves(activeplayer)
        movelist = []
        print ("NEW TURN")
        print(legalmoves)
        spaces = gameboard.space_count()

        if len(legalmoves) == 0:
            moved = True
            passcount = passcount+1
        else:
            passcount = 0

        for coord, list in legalmoves.items():
            movelist.append((coord, list[0], list[1]))
        print("\n")
        for item in movelist:
            print(item)
        for sprite in sprite_handler:
            sprite.set_color()
        all_sprites_list.draw(screen)
        pygame.display.flip()
        if passcount == 2:
            running = False

        while not moved:
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                for object in check_object_events:
                    check = object.handle_event(event,activeplayer)
                    if check != False:
                        move = find_move(movelist,check)
                        if move != False:
                            gameboard.do_move(activeplayer, move)
                            moved = True

            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                moved = True
        inactiveplayer = activeplayer
        activeplayer = tmp
        tmp = inactiveplayer

    count = gameboard.space_count()
    check = True
    if count[0] > count[1]:
        button = Button(256,0,"OthelloSprites/whitewin.png")
    elif count[1] > count[0]:
        button = Button(256,0,"OthelloSprites/blackwin.png")
    else:
        button = Button(256,0,"OthelloSprites/tie.png")
    all_sprites_list.add(button)

    while check:
        pygame.time.wait(100)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            check = button.handle_event(event)
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                check = False

def pvc(screen):
    pygame.display.set_caption("Player vs AI")
    screen.fill((0,0,0))
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((381, 256))
    sprite_handler = []
    all_sprites_list = pygame.sprite.Group()
    check_object_events = []

    button1 = GameButt(256, 0, "OthelloSprites/random.png", "randy")
    button2 = GameButt(256, 45, "OthelloSprites/greedy.png", "greedy")
    button3 = GameButt(256, 90, "OthelloSprites/greedyvar.png", "greedyvar")
    button4 = GameButt(256, 135, "OthelloSprites/plieplayer.png", "plie")

    all_sprites_list.add(button1)
    all_sprites_list.add(button2)
    all_sprites_list.add(button3)
    all_sprites_list.add(button4)

    check_object_events.append(button1)
    check_object_events.append(button2)
    check_object_events.append(button3)
    check_object_events.append(button4)

    running = True
    game = False
    while game == False:
        screen.fill((0,0,0))
        all_sprites_list.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            for object in check_object_events:
                if game == False:
                    game = object.handle_event(event)

            if event.type == pygame.QUIT:
                game = True
                running = False

    wait = 0
    if game == "randy":
        player2 = randyAI.RandyPlayer()
        wait = 1
    if game == "greedy":
        player2 = greedyAI.GreedyPlayer()
        wait = 1
    if game == "greedyvar":
        player2 = greedyVariableAI.GreedyVariablePlayer()
        wait = 1
    if game == "plie":
        player2 = plieAI.PliePlayer()
        wait = 0

    all_sprites_list = pygame.sprite.Group()
    check_object_events = []

    player1 = "W"
    activeplayer = player1
    inactiveplayer = player2

    passcount = 0
    gameboard = Gameboard()
    for x in range(0, 8):
        for y in range(0, 8):
            tmp = SpaceSprite(gameboard.get_space(x, y))
            tmp.set_color()
            sprite_handler.append(tmp)
            all_sprites_list.add(tmp)
            check_object_events.append(tmp)


    while running:
        moved = False
        tmp = inactiveplayer
        if activeplayer == player1:
            legalmoves = gameboard.find_legal_moves(activeplayer)
        else:
            legalmoves = gameboard.find_legal_moves("B")

        movelist = []
        print ("NEW TURN")
        spaces = gameboard.space_count()

        if len(legalmoves) == 0:
            moved = True
            passcount = passcount+1
        else:
            passcount = 0

        for coord, list in legalmoves.items():
            movelist.append([coord, list[0], list[1]])
        for item in movelist:
            print(item)
        for sprite in sprite_handler:
            sprite.set_color()
        screen.fill((0,0,0))
        all_sprites_list.draw(screen)
        pygame.display.flip()
        if passcount == 2:
            running = False

        while not moved:
            # event handling, gets all event from the eventqueue
            if activeplayer == player1:
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    for object in check_object_events:
                        check = object.handle_event(event,activeplayer)
                        if check != False:
                            move = find_move(movelist,check)
                            if move != False:
                                gameboard.do_move(activeplayer, move)
                                moved = True
            else:
                if len(movelist) > 1:
                    move = player2.calculate(movelist, gameboard)
                    gameboard.do_move("B", move)
                else:
                    move = movelist[0]
                    gameboard.do_move("B", move)
                print ("played ", move)
                moved = True
                sleep(wait)
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                moved = True
        inactiveplayer = activeplayer
        activeplayer = tmp
        tmp = inactiveplayer

    count = gameboard.space_count()
    check = True
    if count[0] > count[1]:
        button = Button(256, 0, "OthelloSprites/whitewin.png")
    elif count[1] > count[0]:
        button = Button(256, 0, "OthelloSprites/blackwin.png")
    else:
        button = Button(256, 0, "OthelloSprites/tie.png")
    all_sprites_list.add(button)

    while check:
        pygame.time.wait(100)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            check = button.handle_event(event)
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                check = False

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    running = True
    pygame.init()
    pygame.display.set_caption("Othello main")
    screen = pygame.display.set_mode((400, 288))
    all_sprite_list = pygame.sprite.Group()
    check_object_events = []

    button1 = GameButt(138, 80, "OthelloSprites/pvp.png", "pvp")
    button2 = GameButt(138, 130, "OthelloSprites/pvc.png", "pvc")
    #button3 = GameButt(138, 80, "OthelloSprites/cvc.png", "cvc")
    all_sprite_list.add(button1)
    all_sprite_list.add(button2)
    #all_sprite_list.add(button3)
    check_object_events.append(button1)
    check_object_events.append(button2)
    #check_object_events.append(button3)


    while running:
        game = False
        all_sprite_list.draw(screen)
        pygame.display.flip()
        while game == False:
            for event in pygame.event.get():
                for object in check_object_events:
                    if game == False:
                        game = object.handle_event(event)

                if event.type == pygame.QUIT:
                    game = True
                    running = False
        if game == "pvp":
            pvp(screen)
        if game == "pvc":
            pvc(screen)
        #if game == "cvc":
            #cvc(screen)
        screen.fill((0,0,0))
