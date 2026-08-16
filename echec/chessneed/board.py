import pygame

from .pieces import*
from .constant import*

class newboard:
    def __init__(self,width,height,rows,cols,square,win):
        self.width=width
        self.height=height
        self.rows=rows
        self.cols=cols
        self.square=square
        self.win=win
        self.Board=[]
        self.create_Board()

    def create_Board(self):
        for row in range(self.rows):
            self.Board.append([0 for i in range(self.cols)])
            for col in range(self.cols):
                pass