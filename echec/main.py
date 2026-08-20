import pygame 

from chessneed.constant import * 
from chessneed.game import Game

pygame.init()

clock=pygame.time.Clock()

win=pygame.display.set_mode((width,height))

def get_position(x,y):
    row=y//square
    col=x//square
    return row ,col

def main():
    run=True
    game_over= False
    turn = black
    run=True
    FPS =60
    game = Game(width,height,rows,cols,square,win)
    while run:
        clock.tick(FPS)

        game.update_windows()
        if game.check_game():
            game_over=True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE and game_over:
                    game.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    row,col = get_position(location[0],location[1])
                    game.select(row,col)
main()