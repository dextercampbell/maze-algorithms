'''
Created on Apr 2, 2018

@author: dexca
'''
'''
Created on Mar 12, 2018

@author: dexca
'''
import numpy as np
import turtle
screen_size = 700
maze_size = 50
unit_size = screen_size/maze_size

#create pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        self.hideturtle()
        


def draw_maze(maze):
    for x in range(maze_size+1):
        screen_x = -(screen_size/2) + (x*unit_size)
        screen_y = -(screen_size/2)           
        pen.goto(screen_x,screen_y)
        pen.pendown()
    pen.penup()

    for y in range(maze_size+1):
        screen_x = (screen_size/2)
        screen_y = (screen_size/2) - (y*unit_size)          
        pen.goto(screen_x,screen_y)
        pen.pendown()
    pen.penup()
    

        
    for y in range(maze_size):
        for x in range(maze_size):
            screen_x = -(screen_size/2) + (x*unit_size)
            screen_y = (screen_size/2) - (y*unit_size)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][1]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()
        if maze[y][maze_size-1][1]==1:
            pen.pendown()
            pen.goto(screen_x+unit_size,screen_y)
            pen.penup()

    for x in range(maze_size):
        for y in range(maze_size):
            screen_x = -(screen_size/2) + (x*unit_size)
            screen_y = (screen_size/2) - (y*unit_size)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][0]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()      
        if maze[maze_size-1][x][0]==1:
            pen.pendown()
            pen.goto(screen_x,screen_y-unit_size)
            pen.penup() 


    pen.penup()
####################################################
def movex(x,dirc):
    if dirc==0:
        return x-1
    elif dirc==2:
        return x+1
    else:
        return x
    
def movey(y,dirc):
    if dirc==1:
        return y-1
    elif dirc==3:
        return y+1
    else:
        return y
def getRev(dirGo):
    if dirGo == 0:
        return 2
    elif dirGo == 1:
        return 3
    elif dirGo == 2:
        return 0
    else:
        return 1      
def recurs(size):
    origGrid = np.full((size,size,4),1,dtype=int)
    visGrid = np.zeros((size+2,size+2),dtype=int)
    for i in range(size+2):
        visGrid[0][i]=1
        visGrid[size+2-1][i]=1
        visGrid[i][0]=1
        visGrid[i][size+2-1]=1
    print(visGrid)
    x=3
    y=3
    dirGo = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    numChoices = 0
    lastx = [0]
    lasty = [0]
    j=0
    while(1): 
        if x==0 and y==0:
            j = j+1
        for i in range(4):
            if visGrid[movey(y+1,i)][movex(x+1,i)]==0:
                dirChoices[numChoices]=i
                numChoices=numChoices+1
                
        if numChoices==0:
            if len(lastx)==0:
                break
            visGrid[y+1][x+1]=1
            x=lastx.pop()
            y=lasty.pop()
            print("pop to",y,x)
        else:       
            if numChoices==1:
                dirGo=dirChoices[0]
            else:  
                lastx.append(x)
                lasty.append(y)         
                r = np.random.rand()
                if r < (1/numChoices):
                    dirGo = dirChoices[0]
                elif r < 2/numChoices:
                    dirGo = dirChoices[1]
                else:
                    dirGo = dirChoices[3]   
            numChoices = 0          
            origGrid[y][x][dirGo]=0
            print("go wall",y,x,dirGo)
            visGrid[y+1][x+1]=1
            x=movex(x,dirGo)
            y=movey(y,dirGo)
            origGrid[y][x][getRev(dirGo)]=0
    print(origGrid)
    return origGrid

maze = recurs(maze_size)
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Small Maze")
wn.setup(screen_size+25,screen_size+25)
pen = Pen()

draw_maze(maze)

wn.exitonclick()
