import pygame

from .pieces import*
from .constant import*

class newBoard:
    def __init__(self,width,height,rows,cols,square,win):
        self.width=width
        self.height=height
        self.rows=rows
        self.cols=cols
        self.gameBoard = self.width//2
        self.square=square
        self.win=win
        self.Board=[]
        self.create_Board()

    def create_Board(self):
        for row in range(self.rows):
            self.Board.append([0 for i in range(self.cols)])
            for col in range(self.cols):
                if row == 6 :
                    self.Board[row][col]=Pion(self.square,pion_noir,black,"Pion",row,col)

                if row == 1 :
                    self.Board[row][col]=Pion(self.square,pion_blanc,white,"Pion",row,col)

                if row==0:
                    if col==0 or col==7:
                        self.Board[row][col]=Tour(self.square,tour_blanche,white,"Tour",row,col)

                    if col==1 or col==6:
                        self.Board[row][col]=Cavalier(self.square,chevalier_blanc,white,"Cavalier",row,col)

                    if col==2 or col==5:
                        self.Board[row][col]=Fou(self.square,fou_blanc,white,"Fou",row,col)

                    if col==3 :
                        self.Board[row][col]=Reine(self.square,reine_blanche,white,"Reine",row,col)

                    if col==4:
                        self.Board[row][col]=Roi(self.square,roi_blanc,white,"Roi",row,col)        

                if row==7:
                    if col==0 or col==7:
                        self.Board[row][col]=Tour(self.square,tour_noir,black,"Tour",row,col)

                    if col==1 or col==6:
                        self.Board[row][col]=Cavalier(self.square,chevalier_noir,black,"Cavalier",row,col)

                    if col==2 or col==5:
                        self.Board[row][col]=Fou(self.square,fou_noir,black,"Fou",row,col)

                    if col==3 :
                        self.Board[row][col]=Reine(self.square,reine_noir,black,"Reine",row,col)

                    if col==4:
                        self.Board[row][col]=Roi(self.square,roi_noir,black,"Roi",row,col)            

    def get_piece(self,row,col):
        return self.Board[row][col]

    def move(self,piece,row,col):             
        self.Board[piece.row][piece.col],self.Board[row][col] = self.Board[row][col] ,self.Board[piece.row][piece.col]

        piece.piece_moves(row,col)

        if piece.type == "Pion":
            if piece.first_move:
                piece.first_move= False

    def draw_Board(self):
        self.win.fill(brown)
        for row in range(self.rows):
            for col in range(row%2,cols,2):
                pygame.draw.rect(self.win,white,(square*(col),square*(row),square,square))

    def draw_piece(self,piece,win):
        win.blit(piece.image,(piece.x,piece.y))

    def draw_pieces(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.Board[row][col] !=0:
                    self.draw_piece(self.Board[row][col],self.win)