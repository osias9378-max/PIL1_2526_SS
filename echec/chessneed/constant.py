import pygame 
import os

width,height=760,760
rows,cols=8,8
square=width//rows 


brown=(87,16,16)
white=(255,255,255) 
black=(0,0,0)
green=(0,1,0)
path="chessneed/chess_images"

chevalier_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bN.png")),(square,square))
fou_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bB.png")),(square,square))
roi_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bK.png")),(square,square))
reine_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bQ.png")),(square,square))
pion_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bP.png")),(square,square))
tour_noir=pygame.transform.scale(pygame.image.load(os.path.join(path,"bR.png")),(square,square))

chevalier_blanc=pygame.transform.scale(pygame.image.load(os.path.join(path,"wN.png")),(square,square))
roi_blanc=pygame.transform.scale(pygame.image.load(os.path.join(path,"wK.png")),(square,square))
reine_blanche=pygame.transform.scale(pygame.image.load(os.path.join(path,"wQ.png")),(square,square))
fou_blanc=pygame.transform.scale(pygame.image.load(os.path.join(path,"wB.png")),(square,square))
tour_blanche=pygame.transform.scale(pygame.image.load(os.path.join(path,"wR.png")),(square,square))
pion_blanc=pygame.transform.scale(pygame.image.load(os.path.join(path,"wP.png")),(square,square))