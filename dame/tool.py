import pygame
import math


pygame.init()

window=pygame.display.set_mode((1000,800))

pygame.display.set_caption("Dame")

Board=[]
fonce=(100,100,100)
clair=(220,220,220)
p_white=(255,248,220)
p_black= (70,40,20)
depla=(26,26,23)



for row in range(8):
    for col in range(8):
        if (col+row)%2 == 0:
            color =clair
        else:
            color= fonce
        pygame.draw.rect(window,color,(140+(col*90),50+(row*90),90,90)) 
        if row in [0,1,2] :
            if color== fonce:
                pygame.draw.circle(window,p_white,((185+(col*90)),(95+(row*90))),30)
                Board.append((row,col,1))
            else:
                Board.append((row,col,0))
        elif row in [5,6,7]:
            if color==fonce:
                pygame.draw.circle(window,p_black,((185+(col*90)),(95+(row*90))),30)
                Board.append((row,col,2))
            else:
                Board.append((row,col,0))
        else:
            Board.append((row,col,0))

def ind(col,row):
    co=(col-140)//90
    ro=(row-50)//90

    return(co,ro)
    

def inde(col,row):
    index=row*8+col
    return index


def change_turn(turn):
    if turn == 2:
        return  1
    elif  turn==1:
        return  2

def nbpion(Board):
    nbp_white=0
    nbp_black=0
    for pion in Board:
        if pion[2] == 1:
            nbp_white+=1

        elif pion[2] == 2 :
            nbp_black+=1
    return (nbp_white,nbp_black)

def game_check(nbp_white,nbp_black):
    if nbp_black==0 or nbp_white==0:
        return False


possible_moves=[]

turn=2
def move():
    if pygame.mouse.get_pressed()[0]:
        location= pygame.mouse.get_pos()
        print(location[0],location[1])
        col=ind(location[0],location[1])[0]
        row=ind(location[0],location[1])[1]
        index=inde(col,row)
        print(col,row)
        global nbp_white
        global nbp_black
        global turn
        global col_i
        global row_i
        print(turn)

        if Board[index][2] != 0 and turn==Board[index][2]:
            possible_moves.clear()
        
            if col-1>=0  and row+1<8:
                index_1=inde(col-1,row+1)
                if Board[index][2]==1 and index_1: 
                    if ((Board[index_1][2]==0 or Board[index_1][2] != Board[index][2]))  :
                        possible_moves.append((row+1,col-1,Board[index][2]))

            if col-1 >= 0 and row-1 >=0:

                index_2=inde(col-1,row-1)
                if Board[index][2]==2 and index_2: 
                    if (Board[index_2][2]==0 or Board[index_2][2] != Board[index][2]):   
                        possible_moves.append((row-1,col-1,Board[index][2]))

            if col+1<8 and row-1 >=0:

                index_3=inde(col+1,row-1)
                if Board[index][2]==2 and index_3: 
                    if (Board[index_3][2]==0 or Board[index_3][2] != Board[index][2])  :
                        possible_moves.append((row-1,col+1,Board[index][2]))

            if col+1<8 and row+1<8:

                index_4=inde(col+1,row+1)
                if Board[index][2]==1 and index_4: 
                    if (Board[index_4][2]==0 or Board[index_4][2] != Board[index][2])  :
                        possible_moves.append((row+1,col+1,Board[index][2]))

            print(Board)
            print(possible_moves)

            col_i=col
            row_i=row
            
            for row in range(8):
                for col in range(8):
                    if (col+row)%2 == 0:
                        color =clair
                        pygame.draw.rect(window,color,(140+(col*90),50+(row*90),90,90)) 
                    else:
                        color= fonce
                        pygame.draw.rect(window,color,(140+(col*90),50+(row*90),90,90)) 
    
            for i in Board:
                        if i[2]==1:
                            color=p_white
                            pygame.draw.circle(window,color,((185+((i[1])*90)),(95+((i[0])*90))),30)
    
                        elif i[2] == 2 :
                            color=p_black 
                            pygame.draw.circle(window,color,((185+((i[1])*90)),(95+((i[0])*90))),30)

                        if i[2]==3:
                            color=p_black
                            pygame.draw.circle(window,color,((185+((i[1])*90)),(95+((i[0])*90))),40)

                        if i[2]==4:
                            color=p_white
                            pygame.draw.circle(window,color,((185+((i[1])*90)),(95+((i[0])*90))),40)
            for i in possible_moves :
                pygame.draw.circle(window,depla,((185+((i[1])*90)),(95+((i[0])*90))),10)


            print(col_i,row_i)
            print(turn)
  
            pygame.display.update()

        elif Board[index][2] == 3:

            for i in range(8):
                if col-i >= 0 and row-i >= 0:
                    if Board[inde(col-i, row-i)][2] == 0:
                        possible_moves.append((col-i, row-i,3))
                    elif Board[inde(col-i, row-i)][2] == 1:
                        possible_moves.append((col-i, row-i,3))
                        break
                    else:
                        break

            for i in range(8):
                if col+i < 8 and row+i < 8:
                    if Board[inde(col+i, row+i)][2] == 0:
                        possible_moves.append((col+i,row+i,3))
                    elif Board[inde(col+i, row+i)][2] == 1:
                        possible_moves.append((col+i, row+i,3))
                        break
                    else:
                        break

            for i in range(8):
                if col+i < 8 and row-i >= 0:
                    if Board[inde(col+i, row-i)][2] == 0:
                        possible_moves.append((col+i, row-i,3))
                    elif Board[inde(col+i, row-i)][2] == 1:
                        possible_moves.append((col+i, row-i,3))
                        break
                    else:
                        break

            for i in range(8):
                if col-i >= 0 and row+i < 8:
                    if Board[inde(col-i, row+i)][2] == 0:
                        possible_moves.append((col-i, row+i,3))
                    elif Board[inde(col-i, row+i)][2] == 1:
                        possible_moves.append((col-i, row+i,3))
                        break
                    else:
                        break
            print(f"possible_move: {possible_moves}")

            for i in possible_moves :
                pygame.draw.circle(window,depla,((185+((i[1])*90)),(95+((i[0])*90))),10)
            pygame.display.update()
            

        elif Board[index][2] == 4:

            for i in range(8):
                if col-i >= 0 and row-i >= 0:
                    if Board[inde(col-i, row-i)][2] == 0:
                        possible_moves.append((col-i, row-i,4))
                    elif Board[inde(col-i, row-i)][2] == 2:
                        possible_moves.append((col-i, row-i,4))
                        break
                    else:
                        break

            for i in range(8):
                if col+i < 8 and row+i < 8:
                    if Board[inde(col+i, row+i)][2] == 0:
                        possible_moves.append((col+i, row+i,4))
                    elif Board[inde(col+i, row+i)][2] == 2:
                        possible_moves.append((col+i, row+i,4))
                        break
                    else:
                        break

            for i in range(8):
                if col+i < 8 and row-i >= 0:
                    if Board[inde(col+i, row-i)][2] == 0:
                        possible_moves.append((col+i, row-i,4))
                    elif Board[inde(col+i, row-i)][2] == 2:
                        possible_moves.append((col+i, row-i,4))
                        break
                    else:
                        break

            for i in range(8):
                if col-i >= 0 and row+i < 8:
                    if Board[inde(col-i, row+i)][2] == 0:
                        possible_moves.append((col-i, row+i,4))
                    elif Board[inde(col-i, row+i)][2] == 2:
                        possible_moves.append((col-i, row+i,4))
                        break
                    else:
                        break


            print(f"possible_move: {possible_moves}")
            for i in possible_moves :
                pygame.draw.circle(window,depla,((185+((i[1])*90)),(95+((i[0])*90))),10)
            col_i=col
            row_i=row

            pygame.display.update()

        elif Board[index][2] == 0 or Board[index][2] != Board[inde(col_i,row_i)][2]  :            


            if (7,col,1) in possible_moves :
                pygame.draw.circle(window,p_white,((185+((col)*90)),(95+((7)*90))),40)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,4)
                possible_moves.remove((row,col,1))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] !=0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()

            if (0,col,2) in possible_moves :
                pygame.draw.circle(window,p_black,((185+((col)*90)),(95+((0)*90))),40)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,3)
                possible_moves.remove((row,col,2))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] !=0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()

            if(row,col,2) in possible_moves:
                pygame.draw.circle(window,p_black,((185+((col)*90)),(95+((row)*90))),30)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,2)
                print("ok")
                possible_moves.remove((row,col,2))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] ==0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90)) 
                pygame.display.update()

            if(row,col,1) in possible_moves:
                pygame.draw.circle(window,p_white,((185+((col)*90)),(95+((row)*90))),30)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,1)
                possible_moves.remove((row,col,1))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] == 0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()
                print(possible_moves)

            if(row,col,1) in possible_moves:
                pygame.draw.circle(window,p_white,((185+((col)*90)),(95+((row)*90))),30)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,1)
                possible_moves.remove((row,col,1))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] == 0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()

            if (row,col,3) in possible_moves :
                pygame.draw.circle(window,p_black,((185+((col)*90)),(95+((row)*90))),40)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,3)
                possible_moves.remove((row,col,3))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] !=0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()

            if (row,col,4) in possible_moves :
                pygame.draw.circle(window,p_white,((185+((col)*90)),(95+((row)*90))),40)
                pygame.draw.rect(window,fonce,(140+(col_i*90),50+(row_i*90),90,90)) 
                Board[inde(col_i,row_i)]=(row_i,col_i,0)
                Board[index]=(row,col,4)
                possible_moves.remove((row,col,4))
                print(possible_moves)
                turn=change_turn(turn)
                for i in possible_moves :
                    if Board[inde(i[1],i[0])][2] !=0 :
                        pygame.draw.rect(window,fonce,(140+(i[1]*90),50+(i[0]*90),90,90))
                pygame.display.update()
                print(possible_moves)






        print(Board)
        print(turn)

    nbpion(Board)
    game_over=game_check(nbpion(Board)[0],nbpion(Board)[1])
    if  game_over:
         pygame.quit()
    print(nbpion(Board)[0],nbpion(Board)[1])




pygame.display.update()


window.fill((0,0,0))
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False
        if event.type == pygame.MOUSEBUTTONDOWN:
            move()
pygame.display.update()



pygame.quit()
    
