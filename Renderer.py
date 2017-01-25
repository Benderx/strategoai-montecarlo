import math
import random
import graphics

class Renderer:

    def __init__(self, engine, l = 40, o = 5):
        self.engine = engine
        self.box_length = l
        self.offset = o
        self.piece_arr = []
        self.win = None
        self.highlighted = []
        self.lines_drawn = False


    # Only for initial draw
    def draw_board(self):
        board = self.engine.get_2D_array(self.engine.board)
        owner = self.engine.get_2D_array(self.engine.owner)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != -1 and self.lines_drawn == False:
                    c = graphics.Rectangle(graphics.Point(self.box_length * i + self.offset, self.box_length * j + self.offset),
                          graphics.Point(self.box_length * (i+1) + self.offset, self.box_length * (j+1) + self.offset))
                    c.draw(self.win)
                    continue

                if self.board[i][j] == -1:
                    continue

                c = graphics.Rectangle(graphics.Point(self.box_length * i + self.offset, self.box_length * j + self.offset),
                          graphics.Point(self.box_length * (i+1) + self.offset, self.box_length * (j+1) + self.offset))
                c.draw(self.win)

                

                piece = graphics.Text(graphics.Point(self.box_length * i + self.offset + (self.box_length / 2),
                                      self.box_length * j + self.offset + (self.box_length / 2)), 'ERROR')

                if self.owner[i][j] == 0:
                    piece.setOutline('white')
                else:
                    piece.setOutline('black')

                if self.board[i][j] == 0:
                    piece.setText('F')
                elif self.board[i][j] == 10:
                    piece.setText('B')
                elif self.board[i][j] == 11:
                    piece.setText('S')
                else:
                    piece.setText(str(self.board[i][j]))


                self.piece_arr.append(piece)
                piece.draw(self.win)
        self.lines_drawn = True


    def get_mouse_square(self):
        p = self.win.getMouse()
        width = int(p.x / self.box_length)
        height = int(p.y / self.box_length)
        return (width, height)


    # takes in array of tuples and highlights those on the board.
    def disp_pos_moves(self, arr):
        for i in arr:
            c = graphics.Rectangle(graphics.Point(self.box_length * i[1][0] + self.offset, self.box_length * i[1][1] + self.offset),
                          graphics.Point(self.box_length * (i[1][0]+1) + self.offset, self.box_length * (i[1][1]+1) + self.offset))
            c.setFill('red')
            c.draw(self.win)
            self.highlighted.append(c)


    # deletes all highlited squares.
    def del_disp_moves(self):
        for i in self.highlighted:
            i.undraw()
        self.highlighted = []
        return


    # Takes in width and height and sets up the Graphical Window.
    def window_setup(self, width, height):
        if __name__ == 'Renderer':
            self.win = graphics.GraphWin("Stratego!", width, height)
            self.win.setBackground("tan2")
        else:
            print("Not the main thread/proccess!")
            return 
