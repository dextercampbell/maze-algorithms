'''
Created on Apr 2, 2018

@author: dexca
'''
import numpy as np
import turtle

# settings
mazeSize=30
screenSize = 500
unitSize = screenSize/mazeSize
pathSpeed = 100000
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





def rand_mouse(maze,mazeSize,screenSize,pen,pathSpeed):
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
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break
            #going right
            else:
                while(maze[y][x][dirGo]!=1):
                    x = x + 1   
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break     
        
        # moving up       
        elif dirGo == 1:
            while(maze[y][x][dirGo]!=1):    
                y = y - 1
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break   
                
        #moving down         
        else:
            while(maze[y][x][dirGo]!=1):    
                y = y + 1  
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break             
        #reset, increment, draw
        numChoices = 0
        numMoves = numMoves + 1
        drawMousePath(oldx,x,oldy,y,mazeSize,screenSize,pen,pathSpeed)
    if pathSpeed == 0:
        turtle.update() # @UndefinedVariable
    return numMoves



maze = backtrackerGen(mazeSize)
pen = Pen()
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Random Mouse Maze")
wn.setup(screenSize+25,screenSize+25)

drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)

print(rand_mouse(maze,mazeSize,screenSize,pen,pathSpeed))

wn.exitonclick()
