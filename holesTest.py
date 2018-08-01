'''
Created on Apr 4, 2018

@author: dexca
'''

import numpy as np
from collections import deque
import turtle
import time as tm

#***********************************************************************
drawM = 1
# which algorithms to draw:
drawShortest = 1
drawAstarShortest = 0

drawDijkstra = 1
drawAstar = 0

drawFollowerR = 0
drawFollowerL = 0

drawRand = 0
drawTremaux = 0

# settings
mazeSize = 80
numHoles = 20
screenSize = 550
pathSpeed = 20
mazeSpeed = 2

#***********************************************************************


#***********************************************************************
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
#***********************************************************************

#***********************************************************************
# create pen class
class Pen(turtle.Turtle):
    def __init__(self,colour):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color(colour)
        self.penup()
        self.speed(0)
        self.hideturtle()
        
# drawing functions
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

def drawPath(x1,x2,y1,y2,mazeSize,screenSize,pen,oset,pathSpeed):
    unitSize = screenSize/mazeSize
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
#***********************************************************************


#***********************************************************************
#generation algorithm
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
#***********************************************************************



#***********************************************************************
# algorithms
def shortestPath(maze,mazeSize,screenSize,drw,pen,pathSpeed):
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
    
    while (1):   
        # ^ if finish is at top of queue - stop
        
        # set x,y to top of queue 
        x = queuex[0]
        y = queuey[0] 
          
        if (queuey[0]==mazeSize-1 and queuex[0]==mazeSize-1):
            break 
        
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
        if drw==1:
            drawPath(x,x1,y,y1,mazeSize,screenSize,pen,.1,pathSpeed)
        x=x1
        y=y1
        numMoves=numMoves+1
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves

def shortestAstar(maze,mazeSize,screenSize,drw,pen,pathSpeed):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
    ### draw speed
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    
    ### initialize
    visited = np.zeros((mazeSize,mazeSize),dtype = np.int)
    aScore = np.full_like(visited,100000,dtype=float)
    dist = np.full_like(visited,100000,dtype=float)
    fromx = np.zeros((mazeSize,mazeSize),dtype = np.int)
    fromy = np.zeros((mazeSize,mazeSize),dtype = np.int)    
    
    dist[0][0]=0
    aScore[0][0]=1000
    queuex = deque()
    queuey = deque()
    queuex.append(0)
    queuey.append(0)
    
    while (1):   
        # ^ if finish is at top of queue - stop
        
        # set x,y to top of queue 
        x = queuex[0]
        y = queuey[0] 
          
        if (queuey[0]==mazeSize-1 and queuex[0]==mazeSize-1):
            break 
        
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
                    aScore[y1][x1]=dist[y1][x1]+2*(np.sqrt(np.power(x1-mazeSize,2)+np.power(y1-mazeSize,2)))
                    j=1
                    while(j<len(queuex)):
                        if aScore[queuey[j]][queuex[j]]>=aScore[y1][x1]:
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
        if drw==1:
            drawPath(x,x1,y,y1,mazeSize,screenSize,pen,.1,pathSpeed)
        x=x1
        y=y1
        numMoves=numMoves+1
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves


def dijkstra(maze,mazeSize,screenSize,drw,pen,pathSpeed):
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
    
    while (1): 
        # ^ if finish is at top of queue - stop
        
        # set x,y to top of queue 
        x = queuex[0]
        y = queuey[0]   
        
        if (queuey[0]==mazeSize-1 and queuex[0]==mazeSize-1):
            break 
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
                    if drw==1:
                        drawPath(x,x1,y,y1,mazeSize,screenSize,pen,-.1,pathSpeed)
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
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves

def aStar(maze,mazeSize,screenSize,drw,pen,pathSpeed):
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
    
    while (1):   
        # ^ if finish is at top of queue - stop
        
        # set x,y to top of queue 
        x = queuex[0]
        y = queuey[0]   
        
        if (queuey[0]==mazeSize-1 and queuex[0]==mazeSize-1):
            break 
        
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
                    if drw==1:
                        drawPath(x,x1,y,y1,mazeSize,screenSize,pen,.2,pathSpeed)
                    #find where to insert to queue
                    aScore[y1][x1]=dist[y1][x1]+2*(np.sqrt(np.power(x1-mazeSize,2)+np.power(y1-mazeSize,2)))
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
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves




def follower(maze,mazeSize,side,screenSize,drw,pen,pathSpeed):
    ### uses getMove, getSide
    ### side--> 1=follow right wall
    ###     --> 0=follow left wall
    
    
    #initialize
    x = 0
    y = 0
    numMoves=0
    curWall = 0
    
    while(1): 
    # ^ if at finish stop  
        xold=x
        yold=y 
        
        if (x==mazeSize-1 and y==mazeSize-1):
            break
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
            curWall=getSide(move,side)
            if move == 0:
                x=x-1
            elif move == 1:
                y=y-1
            elif move == 2:
                x=x+1
            else:
                y=y+1
                
        # increment moves
        if drw==1:
            drawWallPath(xold,x,yold,y,curWall,mazeSize,screenSize,pen,pathSpeed)
        numMoves=numMoves+1
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves

def randMouse(maze,mazeSize,screenSize,drw,pen,pathSpeed):
    x = 0
    y = 0
    numMoves = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    dirGo = 0
    dirFrom = 1
    numChoices = 0
    while(x!=mazeSize-1 or y!=mazeSize-1): 
    # ^ stop when at finish
        
        # find potential moves
        for i in range(4):
            if maze[y][x][i] == 0 and i != dirFrom:
                dirChoices[numChoices]=i  
                numChoices=numChoices+1    
        # if no moves go back  
        if numChoices==0:
            dirGo=dirFrom
            
        # else pick a random move (if only one pick that)
        else:           
            r = np.random.rand()
            if r < (1/numChoices):
                dirGo = dirChoices[0]
            elif r < 2/numChoices:
                dirGo = dirChoices[1]
            elif r < 3/numChoices:
                dirGo = dirChoices[2]
            else:
                dirGo = dirChoices[3]   
                  
        # get new reverse direction
        if dirGo == 0:
            dirFrom = 2
        elif dirGo == 1:
            dirFrom = 3
        elif dirGo == 2:
            dirFrom = 0
        else:
            dirFrom = 1   
          
        oldx = x
        oldy = y
        ## move until hit junction or wall
        # moving horizontally
        if dirGo == 0 or dirGo == 2:
            
            # going left
            if dirGo == 0:
                while(maze[y][x][dirGo]!=1):     
                    x = x - 1   
                    numMoves = numMoves + 1        
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break
            #going right
            else:
                while(maze[y][x][dirGo]!=1):
                    x = x + 1   
                    numMoves = numMoves + 1
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break     
        
        # moving up       
        elif dirGo == 1:
            while(maze[y][x][dirGo]!=1):    
                y = y - 1
                numMoves = numMoves + 1
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break   
                
        #moving down         
        else:
            while(maze[y][x][dirGo]!=1):    
                y = y + 1  
                numMoves = numMoves + 1
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break             
        #reset, draw
        numChoices = 0
        #numMoves = numMoves + 1
        if drw==1:
            drawPath(oldx,x,oldy,y,mazeSize,screenSize,pen,0,pathSpeed)
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves


def tremaux(maze,mazeSize,screenSize,drw,pen,pathSpeed):
    #turtle.tracer(1,1000)
    x = 0
    y = 0
    numMoves = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    dirC=np.asarray([0,0,0,0], dtype=int)
    markPath = np.zeros((mazeSize,mazeSize),dtype = np.int)
    markJunc = np.zeros((mazeSize,mazeSize),dtype = np.int)
    dirGo = 0
    dirFrom = 1
    numChoices = 0
    
    for i in range(4):
        if maze[y][x][i] == 0:
            dirChoices[numChoices]=i  
            numChoices=numChoices+1    
        
    dirGo = dirChoices[0]
    
    x = movex(x,dirGo) 
    y = movey(y,dirGo) 
    if drw==1:
        drawPath(0,x,0,y,mazeSize,screenSize,pen,0,pathSpeed)
    markPath[y][x]=markPath[y][x]+1 
    markJunc[0][0]=1
    if dirGo == 0:
        dirFrom = 2
    elif dirGo == 1:
        dirFrom = 3
    elif dirGo == 2:
        dirFrom = 0
    else:
        dirFrom = 1   

        
    while(x!=mazeSize-1 or y!=mazeSize-1): 
    #for r in range(100):
    # ^ stop when at finish
        numChoices = 0
        # find potential moves
        for i in range(4):
            if maze[y][x][i] == 0:
                dirChoices[numChoices]=i  
                numChoices=numChoices+1    
        # deadend! 
        if numChoices==1:
            dirGo=dirFrom
        
        # at a turn    
        elif numChoices == 2:
            if dirChoices[0]==dirFrom:
                dirGo = dirChoices[1]
            else:
                dirGo = dirChoices[0]
                
        # at a junction
        else:
            # unvisited junc
            if markJunc[y][x]==0: #markPath[movey(y,dirFrom)][movex(x,dirFrom)]
                #pick random
                for i in range(numChoices):
                    if markPath[movey(y,dirChoices[i])][movex(x,dirChoices[i])] == 0:
                        dirGo = dirChoices[i]
                    
            # visited junc
            else:
                #new path
                if markPath[movey(y,dirFrom)][movex(x,dirFrom)] == 1:
                    dirGo=dirFrom
                else:
                    gone =0
                    numC=0
                                        #there is a new path
                    for i in range(numChoices):
                        if markPath[movey(y,dirChoices[i])][movex(x,dirChoices[i])] == 0:                 
                            dirC[numC] = dirChoices[i]
                            numC=numC+1
                            gone=1
                    #take a old path
                    if gone==0:
                        for i in range(numChoices):
                            if markPath[movey(y,dirChoices[i])][movex(x,dirChoices[i])] == 1:
                                dirC[numC] = dirChoices[i]
                                numC=numC+1
                                gone=1
                    
                    if gone==0:
                        for i in range(numChoices):
                            if markJunc[movey(y,dirChoices[i])][movex(x,dirChoices[i])]>= 1:
                                dirC[numC] = dirChoices[i]
                                numC=numC+1
                                
                                gone=1
                    if gone ==0:
                        #print("!!!!!!!")
                        dirGo = dirChoices[np.random.randint(0,numChoices)]
                    else:
                        dirGo = dirC[np.random.randint(0,numC)]
            markJunc[y][x]=markJunc[y][x]+1       
        # get new reverse direction
        if dirGo == 0:
            dirFrom = 2
        elif dirGo == 1:
            dirFrom = 3
        elif dirGo == 2:
            dirFrom = 0
        else:
            dirFrom = 1   
        
        oldx = x
        oldy = y
        
        markPath[y][x]=markPath[y][x]+1  
                
        x = movex(x,dirGo)
        y = movey(y,dirGo)
        
  
                
        #reset, increment, draw
        
        numMoves = numMoves + 1
        if drw==1:
            drawPath(oldx,x,oldy,y,mazeSize,screenSize,pen,0,pathSpeed)
        if numMoves>10000:
            return "error"
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
        
    return numMoves
#***********************************************************************



#***********************************************************************
# run
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("maze")
wn.setup(screenSize+25,screenSize+25)
unitSize = screenSize/mazeSize

blackPen = Pen("black")
redPen = Pen("red")
greenPen = Pen("green")
bluePen = Pen("blue")
orangePen = Pen("orange")
purplePen = Pen("purple")
for i in range(5):
    print("\npath\tA*path\tdijk\tA*\tfollowR\tfollowL\trMouse\ttreaux\t",mazeSize,"x",mazeSize,"\t",numHoles," holes,",sep='')
    
    maze = backtrackerGen(mazeSize,numHoles)
    if drawM == 1:
        drawMaze(maze,mazeSize,screenSize,mazeSpeed,greenPen,redPen,blackPen)
    print(shortestPath(maze,mazeSize,screenSize,drawShortest,redPen,0),"\t",
          shortestAstar(maze,mazeSize,screenSize,drawAstarShortest,redPen,0),"\t",
          dijkstra(maze,mazeSize,screenSize,drawDijkstra,bluePen,pathSpeed),"\t",
          aStar(maze,mazeSize,screenSize,drawAstar,greenPen,pathSpeed),"\t",
          follower(maze,mazeSize,1,screenSize,drawFollowerR,purplePen,pathSpeed),"\t",
          follower(maze,mazeSize,0,screenSize,drawFollowerL,greenPen,pathSpeed),"\t",
          randMouse(maze,mazeSize,screenSize,drawRand,orangePen,pathSpeed),"\t",
          tremaux(maze, mazeSize, screenSize, drawTremaux, bluePen, pathSpeed)
          )
    tm.sleep(5)
    turtle.clearscreen()
wn.exitonclick()    