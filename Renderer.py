import math
import random
import graphics

class Renderer:

    def __init__(self, b, l = 40, o = 5):
        self.board = b
        self.box_length = l
        self.offset = o
        self.piece_arr = []
        self.win = None


    # Only for initial draw
    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                piece = graphics.Text(graphics.Point(self.box_length * i + self.offset + (self.box_length / 2),
                                      self.box_length * j + self.offset + (self.box_length / 2)), "NO")
                self.piece_arr.append(piece)
                piece.draw(self.win)


    # Used for refreshing to save space and time.
    def refresh_board(self):
        pass


    # Takes in width and height and sets up the Graphical Window.
    def window_setup(self, width, height):
        if __name__ == 'Renderer':
            print('ya')
            self.win = graphics.GraphWin("Stratego!", width, height)
            self.win.setBackground("tan2")
        else:
            print("Not the main thread/proccess!")
            return 