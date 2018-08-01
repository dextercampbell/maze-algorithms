'''
Created on Apr 2, 2018

@author: dexca
'''
import numpy as np
import turtle

# settings
mazeSize=40
screenSize = 500
unitSize = screenSize/mazeSize
pathSpeed = 50
mazeSpeed = 0
side=0

whichSide = {0: "left Side Wall Follower Maze", 1: "Right Side Wall Follower Maze"}

########################## drawing ##################3
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
    unitSize = screenSize/mazeSize # @UndefinedVariable
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


def drawWallPath(x1,x2,y1,y2,wall,mazeSize,screenSize,pen,pathSpeed):
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    unitSize = screenSize/mazeSize
    pen.color("blue")
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

########################### solving ###################

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
                    dirGo = dirChoices[3]   
                    
            # reset counter, mark visited
            numChoices = 0     
            visGrid[y+1][x+1]=1     
            
            # remove wall, move, remove wall on other side
            origGrid[y][x][dirGo]=0
            x=movex(x,dirGo)
            y=movey(y,dirGo)
            origGrid[y][x][getRev(dirGo)]=0

    return origGrid



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
        
def follower(maze,mazeSize,side):
    ### uses getMove, getWall, drawWallPath
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
        drawWallPath(xold,x,yold,y,curWall,mazeSize,screenSize,pen,pathSpeed)
        numMoves=numMoves+1
    return numMoves


maze = backtrackerGen(mazeSize)
pen = Pen()
wn = turtle.Screen()
wn.bgcolor("white")
wn.title(whichSide[side])
wn.setup(screenSize+25,screenSize+25)

drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)

print(follower(maze,mazeSize,side))

wn.exitonclick()

