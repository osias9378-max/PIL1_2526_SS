import pygame

from .board import newBoard
from .constant import*
from copy import deepcopy

class Game:
    def __init__(self,width,height,rows,cols,square,win):
        self.win = win
        self.Board= newBoard(width,height,rows,cols,square,win)
        self.square=square
        self.selected= None
        self.turn= black
        self.valid_moves=[]
        self.black_pieces_left=16
        self.white_pieces_left=16

    def update_windows(self):
        self.Board.draw_Board()
        self.Board.draw_pieces()
        self.draw_available_move()
        pygame.display.update()

    def reset(self):
        self.Board=newBoard(width,height,rows,cols,square,win)
        self.square = square

        self.selected=None

    def check_game(self):
        if self.black_pieces_left==0 :
            print("Les blancs ont gagne la partie")
            return True

        if self.white_pieces_left ==0 :
            print("Les noirs ont gagne la partie")
            return True


    def enemies_moves(self,piece,Board):
        enemies_moves=[]

        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c]!=0:
                    if Board[r][c].color != piece.color:
                        moves=Board[r][c].get_available_moves(r,c,Board)
                        for move in moves :
                            enemies_moves.append(move)
        return enemies_moves

    def get_king_pos(self,Board):
        for r in range(len(Board)):
            for c in range (len(Board[r])):
                if Board[r][c]!=0:
                    if Board[r][c].type == "roi" and Board[r][c].color ==self.turn:
                        return (r,c)
                    
    def simulate_move(self,piece,row,col):
        piece_row,piece_col=piece.row,piece.col
        save_piece=self.Board.Board[row][col]

        self.Board.Board[piece_row][piece_col]=0
        self.Board.Board[row][col]=piece

        king_pos=self.get_king_pos(self.Board.Board)
        in_check = king_pos in self.enemies_moves(piece,self.Board.Board)

        self.Board.Board[piece_row][piece_col]=piece
        self.Board.Board[row][col]=save_piece

        return not in_check
    
    def possible_moves(self,Board):
        possible_moves=[]
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color == self.turn and Board[r][c].type != "roi":
                        moves = Board[r][c].get_availables_moves(r,c,Board)
                        for move in moves:
                            possible_moves.append(move)

        return possible_moves

    def checkmate(self,Board):
        king_pos = self.get_king_pos(Board.Board)
        get_king =Board.get_piece(king_pos[0],king_pos[1])
        king_availables_moves = set(get_king.get_available_moves(king_pos[0],king_pos[1],Board.Board))
        enemies_moves_set =set (self.enemies_moves(get_king,Board.Board))
        king_safe = king_availables_moves - enemies_moves_set
        kill_king = king_availables_moves.intersection(self.enemies_moves)
        defense = kill_king.intersection(self.possible_moves(Board.Board))
        if len(king_safe)==0 and len(king_availables_moves) !=0 and self.defense ==0 :
            return True
        return False

  

    def change_turn(self):
        if self.turn == white:
            self.turn = black
        else:
            self.turn = white

    def select(self,row,col):
        if self.selected:
            move = self._move(row,col)
            if not move:
                self.selected= None
                self.select(row,col)

        piece =self.Board.get_piece(row,col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece

            self.valid_moves=piece.get_available_moves(row,col,self.Board.Board)


    def _move(self,row,col):
        piece=self.Board.get_piece(row,col)
        if self.selected and (row,col) in self.valid_moves:
            if piece== 0 or piece.color != self.selected.color:
                if self.simulate_move(self.selected,row,col):
                    self.remove(self.Board.Board,piece,row,col)
                    self.Board.move(self.selected,row,col)
                    self.change_turn()
                    self.valid_moves=[]
                    self.selected = None
                    
                    return True
                
                return False
            
        return False
                    
    def remove(self,board,piece,row,col):
        if piece!=0:
            board[row][col] = 0
            if piece.color == white:
                self.white_pieces_left-=1
            else:
                self.black_pieces_left -= 1

    def draw_available_move(self):
        if len(self.valid_moves)>0:
            for pos in self.valid_moves:
                row,col=pos[0],pos[1]
                pygame.draw.circle(self.win,green,(col*self.square+self.square//2,row*self.square+self.square//2),self.square//8)

    def get_board(self):
        return self.board