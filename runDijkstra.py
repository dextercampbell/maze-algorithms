'''
Created on Apr 2, 2018

@author: dexca
'''

import numpy as np
from collections import deque
import turtle
import time as tm

# settings

mazeSize = 35
screenSize = 550
unitSize = screenSize/mazeSize
pathSpeed = 1
mazeSpeed = 0

#create pen class
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)
        self.hideturtle()
        
def drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen):
    unitSize = screenSize/mazeSize
    turtle.tracer(mazeSpeed,0) # @UndefinedVariable
    
    # draw start and finish
    pen.color("green")
    pen.goto((-screenSize/2)+(.5*unitSize),(screenSize/2)-(.5*unitSize))
    pen.stamp()
    pen.color("red")
    pen.goto((screenSize/2)-(.5*unitSize),(-screenSize/2)+(.5*unitSize))
    pen.stamp()
    pen.color("black")
    
    #draw right side and bottom lines
    for x in range(mazeSize+1):
        screen_x = -(screenSize/2) + (x*unitSize)
        screen_y = -(screenSize/2)           
        pen.goto(screen_x,screen_y)
        pen.pendown()
    pen.penup()

    for y in range(mazeSize+1):
        screen_x = (screenSize/2)
        screen_y = (screenSize/2) - (y*unitSize)          
        pen.goto(screen_x,screen_y)
        pen.pendown()
    pen.penup()
    
    # draw horizontal lines        
    for y in range(mazeSize):
        for x in range(mazeSize):
            screen_x = -(screenSize/2) + (x*unitSize)
            screen_y = (screenSize/2) - (y*unitSize)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][1]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()
        if maze[y][mazeSize-1][1]==1:
            pen.pendown()
            pen.goto(screen_x+unitSize,screen_y)
            pen.penup()
            
    #draw vertical lines
    for x in range(mazeSize):
        for y in range(mazeSize):
            screen_x = -(screenSize/2) + (x*unitSize)
            screen_y = (screenSize/2) - (y*unitSize)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][0]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()      
        if maze[mazeSize-1][x][0]==1:
            pen.pendown()
            pen.goto(screen_x,screen_y-unitSize)
            pen.penup() 
    pen.penup()
    turtle.update() # @UndefinedVariable

def drawPath(x1,x2,y1,y2,mazeSize,screenSize,pen,colour,pathSpeed):
    unitSize = screenSize/mazeSize
    pen.color(colour)
    screen_x = -(screenSize/2) + (x1*unitSize)+(.5*unitSize)
    screen_y = (screenSize/2) - (y1*unitSize)-(.5*unitSize) 
    pen.goto(screen_x,screen_y)
    pen.pendown()
    screen_x = -(screenSize/2) + (x2*unitSize)+(.5*unitSize)
    screen_y = (screenSize/2) - (y2*unitSize)-(.5*unitSize)    
    pen.goto(screen_x,screen_y)
    pen.penup()
    return 0

# movement functions
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

def getSide(m,side):
    if side==1:
        if m==0:
            w=1
        elif m==1:
            w=2
        elif m==2:
            w=3
        else: 
            w=0
    else:
        if m==0:
            w=3
        elif m==1:
            w=0
        elif m==2:
            w=1
        else: 
            w=2
    return w
    
def backtrackerGen(mazeSize,numHoles):
    ### uses movex, movey, getRev
    ### uses numpy
    
    origGrid = np.full((mazeSize,mazeSize,4),1,dtype=int)
    
    # visited matrix (with outside boundary)
    visGrid = np.zeros((mazeSize+2,mazeSize+2),dtype=int)
    for i in range(mazeSize+2):
        visGrid[0][i]=1
        visGrid[mazeSize+2-1][i]=1
        visGrid[i][0]=1
        visGrid[i][mazeSize+2-1]=1
        
    # random starting point
    x=np.random.randint(0,mazeSize-1)
    y=np.random.randint(0,mazeSize-1)
    
    # initialize 
    dirGo = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    numChoices = 0
    lastx = [0]
    lasty = [0]
    holes = 0
    while(1): 
        
        # find potential moves
        for i in range(4):
            if visGrid[movey(y+1,i)][movex(x+1,i)]==0:
                dirChoices[numChoices]=i
                numChoices=numChoices+1
        
        # if no moves, backtrack        
        if numChoices==0:
            if len(lastx)==0:
                break
            visGrid[y+1][x+1]=1
            x=lastx.pop()
            y=lasty.pop()

        else:       
            # if only 1 move
            if numChoices==1:
                dirGo=dirChoices[0]
                
            # if multiple moves - mark as backtracking point - pick a random direction
            else:  
                lastx.append(x)
                lasty.append(y)         
                r = np.random.rand()
                if r < (1/numChoices):
                    dirGo = dirChoices[0]
                elif r < 2/numChoices:
                    dirGo = dirChoices[1]
                else:
                    dirGo = dirChoices[2]   
                    
            # reset counter, mark visited
            numChoices = 0     
            visGrid[y+1][x+1]=1     
            
            # remove wall, move, remove wall on other side
            origGrid[y][x][dirGo]=0
            x=movex(x,dirGo)
            y=movey(y,dirGo)
            origGrid[y][x][getRev(dirGo)]=0

    while(1):
        if holes>=numHoles:
            break
        x=np.random.randint(1,mazeSize-1)
        y=np.random.randint(1,mazeSize-1)
        dirc=np.random.randint(1,4)
        
        if (origGrid[y][x][dirc]==1 and origGrid[movey(y,getSide(dirc,1))][movex(x,getSide(dirc,1))][dirc]==1 
        and origGrid[movey(y,getSide(dirc,0))][movex(x,getSide(dirc,0))][dirc]==1):
            origGrid[y][x][dirc]=0
            origGrid[movey(y,dirc)][movex(x,dirc)][getRev(dirc)]=0
            holes=holes+1
            #drawPath(x,movex(x,dirc),y,movey(y,dirc),mazeSize,screenSize,pen,0,pathSpeed)
    return origGrid
        
def dijkstra(maze,mazeSize,screenSize,pen,pathSpeed):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
    ### draw speed
    turtle.tracer(pathSpeed,.2) # @UndefinedVariable
     
    ### initialize
    visited = np.zeros((mazeSize,mazeSize),dtype = np.int)
    dist = np.full_like(visited,100000,dtype=float)
    fromx = np.zeros((mazeSize,mazeSize),dtype = np.int)
    fromy = np.zeros((mazeSize,mazeSize),dtype = np.int)    
    
    numMoves = 0
    dist[0][0]=0
    
    queuex = deque()
    queuey = deque()
    queuex.append(0)
    queuey.append(0)
    
    while queuey[0]!=mazeSize-1 or queuex[0]!=mazeSize-1:   
        # ^ if finish is at top of queue - stop
        
        # set x,y to top of queue 
        x = queuex[0]
        y = queuey[0]   
        
        # find potential moves   
        for i in range(4):
            if maze[y][x][i]==0:
                y1=movey(y,i)
                x1=movex(x,i)
                
                # if potential move is visited - move to next
                if visited[y1][x1]==1:
                    continue
                
                # otherwise process the move
                else:
                    # calc distance and draw
                    dist[y1][x1]=dist[y][x]+1
                    drawPath(x,x1,y,y1,mazeSize,screenSize,pen,"blue",pathSpeed)
                    #find where to insert to queue
                    j=1
                    while(j<len(queuex)):
                        if dist[queuey[j]][queuex[j]]>=dist[y1][x1]:
                            break
                        j=j+1
                    
                    # insert new location to queue, increment moves
                    queuey.insert(j,y1)
                    queuex.insert(j,x1)
                    numMoves=numMoves+1
                    
                    fromx[y1][x1]=x
                    fromy[y1][x1]=y
        
        # all potential moves processed, remove current location from queue, mark as visited
        queuey.popleft()
        queuex.popleft()
        visited[y][x]=1   
        
    x = mazeSize-1
    y = mazeSize-1
    while (1):
        x1 = fromx[y][x]
        y1 = fromy[y][x]
        if x1==0 and y1==0:
            break
        drawPath(x,x1,y,y1,mazeSize,screenSize,pen,"red",pathSpeed)
        x=x1
        y=y1
    return numMoves


wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Dijkstra Maze")
wn.setup(screenSize+25,screenSize+25)
pen = Pen()
for i in range(10):
    turtle.clearscreen()
    maze = backtrackerGen(mazeSize,15)
    drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)
    print(dijkstra(maze,mazeSize,screenSize,pen,pathSpeed))
    tm.sleep(5)
wn.exitonclick()
