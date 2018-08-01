'''
Created on Apr 2, 2018

@author: dexca
'''
mazeSize = 90

import numpy as np
from collections import deque

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
    
    
def recurs(mazeSize):
    ### uses movex, movey, getRev
    ### uses numpy
    
    origGrid = np.full((mazeSize,mazeSize,4),1,dtype=int)
    
    #visited matrix (with outside boundary)
    visGrid = np.zeros((mazeSize+2,mazeSize+2),dtype=int)
    for i in range(mazeSize+2):
        visGrid[0][i]=1
        visGrid[mazeSize+2-1][i]=1
        visGrid[i][0]=1
        visGrid[i][mazeSize+2-1]=1
        
    #random starting point
    x=np.random.randint(0,mazeSize)
    y=np.random.randint(0,mazeSize)
    
    #initialize 
    dirGo = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    numChoices = 0
    lastx = [0]
    lasty = [0]
    
    while(1): 
        
        #find potential moves
        for i in range(4):
            if visGrid[movey(y+1,i)][movex(x+1,i)]==0:
                dirChoices[numChoices]=i
                numChoices=numChoices+1
        
        #if no moves, backtrack        
        if numChoices==0:
            if len(lastx)==0:
                break
            visGrid[y+1][x+1]=1
            x=lastx.pop()
            y=lasty.pop()

        else:       
            #if only 1 move
            if numChoices==1:
                dirGo=dirChoices[0]
                
            #if multiple moves - mark as backtracking point - pick a random direction
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
                    
            #reset counter, mark visited
            numChoices = 0     
            visGrid[y+1][x+1]=1     
            
            #remove wall, move, remove wall on other side
            origGrid[y][x][dirGo]=0
            x=movex(x,dirGo)
            y=movey(y,dirGo)
            origGrid[y][x][getRev(dirGo)]=0

    return origGrid
        
def dijkstra(maze,mazeSize):
    ### uses movex, movey
    ### uses numpy
    ### uses deque
    
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
        
        #find potential moves   
        for i in range(4):
            if maze[y][x][i]==0:
                y1=movey(y,i)
                x1=movex(x,i)
                
                # if potential move is visited - move to next
                if visited[y1][x1]==1:
                    continue
                
                #otherwise process the move
                else:
                    # calc distance
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
                    numMoves=numMoves+1
        
        #all potential moves processed, remove current location from queue, mark as visited
        queuey.popleft()
        queuex.popleft()
        visited[y][x]=1   
    
    return numMoves

print(dijkstra(recurs(mazeSize),mazeSize))