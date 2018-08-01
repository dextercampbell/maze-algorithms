'''
Created on Apr 6, 2018

@author: dexca
'''
'''
Created on Apr 2, 2018

@author: dexca
'''
import numpy as np
import turtle

# settings
mazeSize=35
screenSize = 500
unitSize = screenSize/mazeSize
pathSpeed = 555
mazeSpeed = 0







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
    if mazeSpeed == 0:
        turtle.update() # @UndefinedVariable


def drawMousePath(x1,x2,y1,y2,mazeSize,screenSize,pen,pathSpeed):
    turtle.tracer(pathSpeed,0) # @UndefinedVariable
    unitSize = screenSize/mazeSize
    pen.color("blue")

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





def rand_mouse(maze,mazeSize,screenSize,pen,pathSpeed):
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
    drawMousePath(0,x,0,y,mazeSize,screenSize,pen,pathSpeed)
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
                        print("PROB")
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
        
        drawMousePath(oldx,x,oldy,y,mazeSize,screenSize,pen,pathSpeed)
        
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves



maze = backtrackerGen(mazeSize,10)
pen = Pen()
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Random Mouse Maze")
wn.setup(screenSize+25,screenSize+25)

drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)


for i in range(50):
    turtle.clearscreen()
    maze = backtrackerGen(mazeSize,0)
    drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)
    
    print(rand_mouse(maze,mazeSize,screenSize,pen,pathSpeed))

#wn.exitonclick()
