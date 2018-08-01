'''
Created on Apr 2, 2018

@author: dexca

'''

import numpy as np
from collections import deque
import turtle
import time as tm
# settings

mazeSize = 100
screenSize = 550
unitSize = screenSize/mazeSize
pathSpeed = 300
mazeSpeed = 500

#create pen class
class Pen(turtle.Turtle):
    def __init__(self,colour):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color(colour)
        self.penup()
        self.speed(0)
        self.hideturtle()
        
def drawMaze(maze,mazeSize,screenSize,mazeSpeed,penStart,penEnd,penWall):
    unitSize = screenSize/mazeSize
    turtle.tracer(mazeSpeed,0) # @UndefinedVariable
    
    # draw start and finish
    
    penStart.goto((-screenSize/2)+(.5*unitSize),(screenSize/2)-(.5*unitSize))
    penStart.stamp()
    penEnd.goto((screenSize/2)-(.5*unitSize),(-screenSize/2)+(.5*unitSize))
    penEnd.stamp()
    
    #draw right side and bottom lines
    for x in range(mazeSize+1):
        screen_x = -(screenSize/2) + (x*unitSize)
        screen_y = -(screenSize/2)           
        penWall.goto(screen_x,screen_y)
        penWall.pendown()
    penWall.penup()

    for y in range(mazeSize+1):
        screen_x = (screenSize/2)
        screen_y = (screenSize/2) - (y*unitSize)          
        penWall.goto(screen_x,screen_y)
        penWall.pendown()
    penWall.penup()
    
    # draw horizontal lines        
    for y in range(mazeSize):
        for x in range(mazeSize):
            screen_x = -(screenSize/2) + (x*unitSize)
            screen_y = (screenSize/2) - (y*unitSize)            
            penWall.goto(screen_x,screen_y)
            if maze[y][x][1]==1:
                penWall.pendown()
            else:
                penWall.penup()
        penWall.penup()
        if maze[y][mazeSize-1][1]==1:
            penWall.pendown()
            penWall.goto(screen_x+unitSize,screen_y)
            penWall.penup()
            
    #draw vertical lines
    for x in range(mazeSize):
        for y in range(mazeSize):
            screen_x = -(screenSize/2) + (x*unitSize)
            screen_y = (screenSize/2) - (y*unitSize)            
            penWall.goto(screen_x,screen_y)
            if maze[y][x][0]==1:
                penWall.pendown()
            else:
                penWall.penup()
        penWall.penup()      
        if maze[mazeSize-1][x][0]==1:
            penWall.pendown()
            penWall.goto(screen_x,screen_y-unitSize)
            penWall.penup() 
    penWall.penup()
    turtle.update() # @UndefinedVariable

def drawPath(x1,x2,y1,y2,mazeSize,screenSize,pen,color,oset,pathSpeed):
    unitSize = screenSize/mazeSize
    # pen.color(color)
    screen_x = -(screenSize/2) + (x1*unitSize)+(.5*unitSize)+(oset*unitSize)
    screen_y = (screenSize/2) - (y1*unitSize)-(.5*unitSize)+(oset*unitSize)
    pen.goto(screen_x,screen_y)
    pen.pendown()
    screen_x = -(screenSize/2) + (x2*unitSize)+(.5*unitSize)+(oset*unitSize)
    screen_y = (screenSize/2) - (y2*unitSize)-(.5*unitSize)+(oset*unitSize)
    pen.goto(screen_x,screen_y)
    pen.penup()
    return 0


def drawWallPath(x1,x2,y1,y2,wall,mazeSize,screenSize,pen,pathSpeed):
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    unitSize = screenSize/mazeSize
    #pen.color("blue")
    if wall==0:
        wallx=-.1*unitSize
        wally=0
    elif wall==1:
        wallx=0
        wally=.1*unitSize
    elif wall==2:
        wallx=.1*unitSize
        wally=0
    else:
        wallx=0
        wally=-.1*unitSize
    
    screen_x = -(screenSize/2) + (x1*unitSize)+(.5*unitSize)+wallx
    screen_y = (screenSize/2) - (y1*unitSize)-(.5*unitSize)+wally
    pen.goto(screen_x,screen_y)
    pen.pendown()
    screen_x = -(screenSize/2) + (x2*unitSize)+(.5*unitSize)+wallx
    screen_y = (screenSize/2) - (y2*unitSize)-(.5*unitSize)   +wally 
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

    
def backtrackerGen(mazeSize):
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
    x=np.random.randint(0,mazeSize)
    y=np.random.randint(0,mazeSize)
    
    # initialize 
    dirGo = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    numChoices = 0
    lastx = [0]
    lasty = [0]
    
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

    return origGrid

def shortestPath(maze,mazeSize,screenSize,pen,pathSpeed):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
    ### draw speed
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    
    ### initialize
    visited = np.zeros((mazeSize,mazeSize),dtype = np.int)
    dist = np.full_like(visited,100000,dtype=float)
    fromx = np.zeros((mazeSize,mazeSize),dtype = np.int)
    fromy = np.zeros((mazeSize,mazeSize),dtype = np.int)    
    
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
                    #find where to insert to queue
                    j=1
                    while(j<len(queuex)):
                        if dist[queuey[j]][queuex[j]]>=dist[y1][x1]:
                            break
                        j=j+1
                    
                    # insert new location to queue, increment moves
                    queuey.insert(j,y1)
                    queuex.insert(j,x1)
                    
                    fromx[y1][x1]=x
                    fromy[y1][x1]=y
        
        # all potential moves processed, remove current location from queue, mark as visited
        queuey.popleft()
        queuex.popleft()
        visited[y][x]=1   
    
    numMoves = 0   
    x = mazeSize-1
    y = mazeSize-1
    while (1):
        x1 = fromx[y][x]
        y1 = fromy[y][x]
        if x1==0 and y1==0:
            break
        drawPath(x,x1,y,y1,mazeSize,screenSize,pen,"red",.1,pathSpeed)
        x=x1
        y=y1
        numMoves=numMoves+1
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves


def dijkstra(maze,mazeSize,screenSize,pen,pathSpeed):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
    ### draw speed
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    #pen.color("yellow")
    ### initialize
    visited = np.zeros((mazeSize,mazeSize),dtype = np.int)
    dist = np.full_like(visited,100000,dtype=float)
    
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
                if visited[y1][x1]!=1:
                    #continue
                
                # otherwise process the move
                #else:
                    # calc distance and draw
                    dist[y1][x1]=dist[y][x]+1
                    drawPath(x,x1,y,y1,mazeSize,screenSize,pen,"blue",0,pathSpeed)
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
        
        # all potential moves processed, remove current location from queue, mark as visited
        queuey.popleft()
        queuex.popleft()
        visited[y][x]=1   
    
    return numMoves


        
def aStar(maze,mazeSize,screenSize,pen,pathSpeed):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
    ### draw speed
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    #pen.color("blue")
    ### initialize
    visited = np.zeros((mazeSize,mazeSize),dtype = np.int)
    dist = np.full_like(visited,100000,dtype=float)
    aScore = np.full_like(visited,100000,dtype=float)
    
    numMoves = 0
    dist[0][0]=0
    aScore[0][0]=1000
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
                    drawPath(x,x1,y,y1,mazeSize,screenSize,pen,"red",-.05,pathSpeed)
                    #find where to insert to queue
                    aScore[y1][x1]=dist[y1][x1]+5*(np.sqrt(np.power(x1-mazeSize,2)+np.power(y1-mazeSize,2)))
                    j=1
                    while(j<len(queuex)):
                        if aScore[queuey[j]][queuex[j]]>=aScore[y1][x1]:
                            break
                        j=j+1
                    
                    # insert new location to queue, increment moves
                    queuey.insert(j,y1)
                    queuex.insert(j,x1)
                    numMoves=numMoves+1
        
        # all potential moves processed, remove current location from queue, mark as visited
        queuey.popleft()
        queuex.popleft()
        visited[y][x]=1   
    
    return numMoves


def getMove(w,side):
    if side==1:
        if w==0:
            m=3
        elif w==1:
            m=0
        elif w==2:
            m=1
        else:
            m=2
    else:
        if w==0:
            m=1
        elif w==1:
            m=2
        elif w==2:
            m=3
        else:
            m=0
    return m

def getWall(m,side):
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



def follower(maze,mazeSize,side,screenSize,pen,pathSpeed):
    ### uses getMove, getWall
    ### side--> 1=follow right wall
    ###     --> 0=follow left wall
    #initialize
    x = 0
    y = 0
    numMoves=0
    curWall = 0
    
    while(x!=mazeSize-1 or y!=mazeSize-1): 
    # ^ if at finish stop  
        xold=x
        yold=y 
        if maze[y][x][curWall]==1:

        # if next to wall 
            while(1):
            #turn until move available
                if maze[y][x][getMove(curWall,side)]==0:
                    break
                else:
                    curWall = getMove(curWall,side)
            
                   
            #move along wall
            move = getMove(curWall,side)
            if move == 0:
                x=x-1
            elif move == 1:
                y=y-1
            elif move == 2:
                x=x+1
            else:
                y=y+1
                
        # if next to path
        else:
            #move towards wall
            move=curWall
            curWall=getWall(move,side)
            if move == 0:
                x=x-1
            elif move == 1:
                y=y-1
            elif move == 2:
                x=x+1
            else:
                y=y+1
                
        # increment moves
        #drawWallPath(xold,x,yold,y,curWall,mazeSize,screenSize,pen,pathSpeed)
        numMoves=numMoves+1
    return numMoves





wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Dijkstra ")
wn.setup(screenSize+25,screenSize+25)
blackPen = Pen("black")
redPen = Pen("red")
greenPen = Pen("green")
bluePen = Pen("blue")
orangePen = Pen("orange")
purplePen = Pen("purple")

for i in range(6):

    tm.sleep(5)

    turtle.clearscreen()
    maze = backtrackerGen(mazeSize) 
    drawMaze(maze,mazeSize,screenSize,mazeSpeed,greenPen,redPen,blackPen)
    #===========================================================================
    # maze = np.zeros((mazeSize,mazeSize,4),dtype=int)
    # for i in range(mazeSize):
    #     maze[0][i][1]=1
    #     maze[mazeSize-1][i][3]=1
    #     maze[i][0][0]=1
    #     maze[i][mazeSize-1][2]=1
    # drawMaze(maze,mazeSize,screenSize,mazeSpeed,greenPen,redPen,blackPen)
    # 
    #===========================================================================
   # print("number of moves in shortest path:",shortestPath(maze,mazeSize,screenSize,redPen,0),"red")
    print("number of moves for dijkstra:",dijkstra(maze,mazeSize,screenSize,bluePen,pathSpeed),"blue")
    print("number of moves for A*:",aStar(maze,mazeSize,screenSize,greenPen,pathSpeed),"green")
  #  print("number of moves for wall follower(right)",follower(maze,mazeSize,1,screenSize,orangePen,pathSpeed))
  #  print("number of moves for wall follower(left)",follower(maze,mazeSize,0,screenSize,purplePen,pathSpeed))
    turtle.update()
    tm.sleep(5)

wn.exitonclick()