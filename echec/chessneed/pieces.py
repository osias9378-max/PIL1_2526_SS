import pygame
from .constant import *

class piece :
    def __init__(self,square,image,color,type,row,col):
        self.square= square
        self.image=image
        self.color= color
        self.row=row
        self.col=col
        self.x=0
        self.y=0
        self.availables_moves=[]

    def pieces_moves(self,row,col):
         self.type=row
         self.col=col
         self.cal_pos()

    def cal_pos(self):
        self.x=self.col*self.square
        self.y=self.row*self.square

    def clear_available_moves(self):
        if len(self.availables_moves) >0:
            self.availables_moves=[]

class Pion(piece):
    def __init__(self,square,image,color,type,row,col):
         super().__init__ (self,square,image,color,type,row,col)
         self.first_move = True

    def get_available_moves(self,row,col,Board):
        self.clear_available_moves 

        if self.color == white:
            if row-1>=0 :
                if Board[row-1][col]==0:
                    self.availables_moves.append(((row-1,col)))

                if self.first_move:
                    if Board[row-1][col]==0 and Board[row-2][col]:
                        self.availables_moves.append((row-2,col))

                if col-1:
                    if Board[row-1][col-1]:
                        piece = Board[row-1][col-1]
                        if piece.color != self.color:
                            self.availables_moves.append((row-1,col-1))

                if col+1<len(Board[0]):
                    if Board[row-1][col-1] !=0:
                        piece=Board[row-1][col+1]
                        if piece.color != self.color:
                            self.availables_moves.append((row-1,col+1))

        if self.color == black:
            if row+1<8:
                if Board[row+1][col]==0:
                    self.availables_moves.append((row+1,col))

                if self.first_move:
                    if Board[row+2][col]==0 and Board[row+1][col]:
                        self.availables_moves.append((row+2,col))

                if col-1:
                    if Board[row+1][col-1]:
                        piece=Board[row+1][col-1]
                        if piece.color!= self.color:
                            self.availables_moves.append((row+1,col-1))

                if  col+1<len(Board[0]):
                    if Board[row+1][col+1] !=0 :
                        piece=Board[row+1][col+1]
                        if piece.color != self.color :
                            self.availables_moves.append((row+1,col+1))

        return self.availables_moves


class Tour(piece):
    def __init__(self, square, image, color, type, row, col):
        super().__init__(square, image, color, type, row, col) 

    def get_avaivalble_moves(self,row,col,Board):
        self.clear_available_moves()
        for i in range(row+ 1,8):
            if Board[i][col]==0:
                self.availables_moves.append((i,col))
            elif Board[i][col].color!= self.color:
                self.availables_moves.append((i,col))
                break
        for j in range(row-1,-1,-1):
                if Board[j][col]==0:
                    self.availables_moves.append((j,col))
                elif Board[j][col].color!= self.color:
                    self.availables_moves.append((j,col))
                    break
        for t in range(col-1,-1,-1):
                if Board[t][col]==0:
                    self.availables_moves.append((row,t))
                elif Board[row][t].color!= self.color:
                    self.availables_moves.append((row,t))
                    break
        for k in range(col+1,8):
                if Board[row][k]==0:
                    self.availables_moves.append((row,k))
                elif Board[row][k].color!= self.color:
                    self.availables_moves.append((row,k))
                    break
            

            

                        


          
