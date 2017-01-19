import math
import random
import inspect

class Piece:
    # 0: Flag
    # 1-7: normal 1 movers, piece 1 loses to spy
    # 8: normal mover, kills bombs
    # 9: super mover
    # 10: bombs, no movement, only loses to miner
    # 11: Spy

    def __init__(self, p, v = None, n = None):
        self.player = p
        self.value = v
        self.name = n
        self.visible = False


    # returns how many spaces the piece may move.
    def get_movement(self):
        if self.value > 0 and self.value < 9 or self.value == 11:
            return 1

        elif self.value == 0 or self.value == 10:
            return 0

        elif self.value == 9:
            return math.inf

        else:
            raise Exception('Piece value not found')


    def get_visibility(self):
        return self.visible


    def get_value(self):
        return self.value


    def get_name(self):
        return self.name


    def get_player(self):
        return self.player


    def reveal(self):
        self.visible = True


class GameEngine:
    def __init__(self):
        self.board = [[0 for x in range(0, 10)] for y in range(0, 10)]
        random.seed(0)

    def board_setup(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                self.board[x][y] = 0

        # Rivers
        self.board[2][4] = Piece(None, -1, 'L')
        self.board[2][5] = Piece(None, -1, 'L')
        self.board[3][4] = Piece(None, -1, 'L')
        self.board[3][5] = Piece(None, -1, 'L')

        self.board[6][4] = Piece(None, -1, 'L')
        self.board[6][5] = Piece(None, -1, 'L')
        self.board[7][4] = Piece(None, -1, 'L')
        self.board[7][5] = Piece(None, -1, 'L')

        for i in range(0, 2):
            starting_pieces = [[0, 'Flag', 1], [10, 'Bomb', 6], [11, 'Spy', 1], [9, 'Scout', 8], [9, 'Miner', 5], [7, 'Sergeant', 4], [6, 'Lieutenent', 4], [5, 'Captain', 4], [4, 'Major', 3], [3, 'Colonel', 2], [2, 'General', 1], [1, 'Marshall', 1]]
            starting_locations = []
            for x in range(0, 10):
                for y in range(0 + i*6, 4 + i*6):
                    starting_locations.append((x, y, i))

            while len(starting_pieces) != 0:
                r1 = int(random.random()*(len(starting_pieces)))
                r2 = int(random.random()*(len(starting_locations)))

                p = Piece(starting_locations[r2][2], starting_pieces[r1][0])
                
                self.board[starting_locations[r2][0]][starting_locations[r2][1]] = p



                starting_locations.pop(r2)
                starting_pieces[r1][2] -= 1
                if starting_pieces[r1][2] == 0:
                    starting_pieces.pop(r1)

    def print_board(self):
        print()
        for x in range(0, 10):
            arr_temp = []
            for y in range(0, 10):
                if isinstance(self.board[y][x], Piece):
                    val = self.board[y][x].get_value()
                    if val == 0:
                        name = 'F'
                    elif val == 10:
                        name = 'B'
                    elif val == 11:
                        name = 'S'
                    elif val == -1:
                        name = 'L'
                    else:
                        name = val
                    arr_temp.append(name)
                else:
                    arr_temp.append(self.board[y][x])
            print(' '.join(map(str, arr_temp)))
        print()


    # Takes in coord1 [x1, y1] and coord2 [x2, y2], and player = (0 or 1)
    def check_legal(self, coord1, coord2, player):
        message = None
        if coord1[0] < 0  or coord1[0] > 9:
            message = "coord1 x is out of bounds"
        if coord1[1] < 0  or coord1[1] > 9:
            message = "coord1 y is out of bounds"
        if coord2[0] < 0  or coord2[0] > 9:
            message = "coord2 x is out of bounds"
        if coord2[1] < 0  or coord2[1] > 9:
            message = "coord2 y is out of bounds"


        lakes = [(2,4), (2,5), (3,4), (3,5),
                (6,4), (6,5), (7,4), (7,5)]
        if (coord1[0], coord1[1]) in lakes:
            message = "coord1 is a lake"
        if (coord2[0], coord2[1]) in lakes:
            message = "coord2 is a lake"


        if not isinstance(self.board[coord1[0]][coord1[1]], Piece):
            message = "coord1 is invalid, there is no piece there"
        if not message:
            piece = self.board[coord1[0]][coord1[1]]
            if piece.get_player() != player:
                message = "That is not your piece"

            xdist = abs(coord1[0] - coord2[0])
            ydist = abs(coord1[1] - coord2[1])

            if xdist != 0 and ydist != 0:
                message = "you cannot move diagonally"

            move = piece.get_movement()
            if xdist > move or ydist > move:
                message = "the piece you are moving cannot move like that"

            if isinstance(self.board[coord2[0]][coord2[1]], Piece):
                piece2 = self.board[coord2[0]][coord2[1]]
                if piece.get_player() == piece2.get_player():
                    message = "You cant move into your own piece"
        if message:
            return False, message
        return True, "legal move"


    # Only for the renderer and the AI
    def get_board(self):
        return self.board


    # Takes in 2 players and returns 0 for p1 winning and 1 for p2 winning, 2 for tie.
    # Something about revealing here.
    def battle(self, p1, p2):
        v1 = p1.get_value()
        v2 = p2.get_value()

        p1.reveal()
        p2.reveal()

        if v1 == 0:
            return 'p1 loses'

        if v2 == 0:
            return 'p2 loses'

        if v1 == 10:
            if v2 == 8:
                return 1
            return 0

        if v2 == 10:
            if v1 == 8:
                return 0
            return 1

        if v1 == 11:
            if v2 == 1:
                return 0
            return 1

        if v2 == 11:
            if v1 == 1:
                return 1
            return 0

        if v1 == v2:
            return 2

        if v1 < v2:
            return 0
        if v2 > v1:
            return 0

        raise Exception('A case that was not thought of happened')
        return False


    # Takes in coord1 [x1, y1] and coord2 [x2, y2]
    # This assumes check_legal has been run.
    def move(self, coord1, coord2):
        p1 = self.board[coord1[0]][coord1[1]]
        self.board[coord1[0]][coord1[1]] = 0
        if not isinstance(self.board[coord2[0]][coord2[1]], Piece):
            self.board[coord2[0]][coord2[1]] = p1
            return True

        p2 = self.board[coord2[0]][coord2[1]]
        winner = self.battle(p1, p2)

        if type(winner) == type('this probably isnt how you should code this'):
            # Add player win detection here.
            return 'Game over.'

        if winner == 0:
            self.board[coord2[0]][coord2[1]] = p1
        elif winner == 2:
            self.board[coord2[0]][coord2[1]] = 0

        return True

    def legal_moves_for_piece(self, loc, player):
        moves = [(loc[0]+1, loc[1]), (loc[0]-1, loc[1]), (loc[0], loc[1]+1), (loc[0], loc[1]-1)]
        final = []
        for move in moves:
            if self.check_legal(loc, move, player)[0]:
                final.append((loc, move))
        return final

    def all_legal_moves(self, player):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                moves += self.legal_moves_for_piece([i,j], player)
        return moves


    # Accidently started developing a function that already existed
    # def get_piece_by_coords(coord, player)
    #     msg = 'legal'
    #     if not isinstance(self.board[coord[0]][coord[1]], Piece):
    #         msg = 'No piece there'
    #         return (False, msg)
    #     piece = self.board[coord[0]][coord[1]]
    #     return piece
