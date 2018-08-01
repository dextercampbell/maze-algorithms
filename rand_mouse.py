'''
Created on Mar 12, 2018

@author: dexca
'''

import numpy as np

direction = {0: "left", 1: "up", 2: "right", 3: "down"}

typeMaze = np.array([(    [1,0],     [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [1,1],        [0,1],        [0,1],        [0,1],        [0,1],        [1,1],        [0,1],        [0,1],        [1,0]        ),
(    [1,0],        [1,1],        [0,1],        [0,1],        [0,1],        [0,1],        [1,0],        [1,0],        [0,1],        [1,1],        [0,1],        [0,0],        [0,0],        [1,1],        [0,0],        [1,0]        ),
(    [1,0],        [1,0],        [1,0],        [0,1],        [0,1],        [1,0],        [1,0],        [0,1],        [0,1],        [1,0],        [1,1],        [0,1],        [0,1],        [0,1],        [1,1],        [1,0]        ),
(    [1,0],        [1,0],        [0,1],        [1,1],        [0,0],        [1,0],        [1,1],        [0,1],        [1,0],        [0,0],        [1,0],        [1,1],        [0,1],        [1,0],        [1,0],        [1,0]        ),
(    [1,0],        [0,1],        [1,0],        [1,0],        [1,1],        [0,0],        [1,0],        [1,1],        [0,1],        [0,1],        [0,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,0],        [0,1],        [1,0],        [1,1],        [0,0],        [1,1],        [0,0],        [1,0],        [1,1],        [0,1],        [0,1],        [1,0],        [1,0],        [0,0],        [0,0],        [1,0]        ),
(    [1,1],        [0,0],        [1,0],        [1,0],        [1,1],        [0,1],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0],        [0,1],        [1,1],        [0,1],        [1,0]        ),
(    [1,0],        [0,1],        [0,0],        [1,0],        [1,0],        [1,0],        [0,0],        [1,0],        [0,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,1],        [0,1],        [1,0],        [1,0],        [1,0],        [0,1],        [0,1],        [0,1],        [1,1],        [0,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,1],        [1,0]        ),
(    [1,0],        [1,0],        [0,0],        [1,0],        [0,1],        [0,1],        [1,0],        [1,1],        [0,0],        [1,1],        [0,0],        [1,0],        [1,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,0],        [1,1],        [1,1],        [0,1],        [0,1],        [0,0],        [1,0],        [1,0],        [1,1],        [0,0],        [1,1],        [0,0],        [1,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,0],        [0,0],        [1,0],        [1,1],        [0,1],        [0,1],        [0,0],        [1,0],        [1,0],        [0,1],        [1,0],        [1,1],        [1,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,1],        [0,1],        [0,0],        [1,0],        [0,1],        [0,1],        [1,1],        [0,0],        [1,1],        [0,0],        [1,0],        [1,0],        [0,0],        [1,0],        [1,0],        [1,0]        ),
(    [1,0],        [0,1],        [0,1],        [0,1],        [0,1],        [1,0],        [0,0],        [1,0],        [1,0],        [1,1],        [1,0],        [0,1],        [0,1],        [0,0],        [1,0],        [1,0]        ),
(    [1,0],        [0,1],        [0,1],        [0,1],        [1,0],        [0,1],        [0,1],        [0,0],        [1,0],        [0,0],        [0,1],        [0,1],        [0,1],        [0,1],        [0,0],        [1,0]        ),
(    [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,0],        [0,0]        )
])

def convert(maze,size):
    four_maze = np.zeros((size,size,4),dtype = np.int)
    for x in range(size):
        for y in range(size):
            four_maze[x][y][0]=maze[x][y][0]
            four_maze[x][y][1]=maze[x][y][1]
            four_maze[x][y][2]=maze[x][y+1][0]
            four_maze[x][y][3]=maze[x+1][y][1]  
            
    four_maze[0][0][1]=1
    four_maze[14][14][3]=-1
    return four_maze
maze = convert(typeMaze,15)


def rand_mouse(maze):
    x = 0
    y = 0
    numMoves = 0
    dirChoices = np.asarray([0,0,0,0], dtype=int)
    dirGo = 0
    dirFrom = 1
    numChoices = 0
    while(maze[y][x][3]!=-1): 
        for i in range(4):
            if maze[y][x][i] == 0 and i != dirFrom:
                dirChoices[numChoices]=i  
                numChoices=numChoices+1      
        if numChoices==0:
            dirGo=dirFrom
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
        
        if dirGo == 0:
            print("go left")
            dirFrom = 2
        elif dirGo == 1:
            print("go up")
            dirFrom = 3
        elif dirGo == 2:
            print("go right")
            dirFrom = 0
        else:
            print("go down")
            dirFrom = 1   
          
        if dirGo == 0 or dirGo == 2:
            if dirGo == 0:
                while(maze[y][x][dirGo]!=1):     
                    x = x - 1           
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break
            else:
                while(maze[y][x][dirGo]!=1):
                    x = x + 1   
                    if maze[y][x][1]==0 or maze[y][x][3]==0:
                        break             
        elif dirGo == 1:
            while(maze[y][x][dirGo]!=1):    
                y = y - 1
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break            
        else:
            while(maze[y][x][dirGo]!=1):    
                y = y + 1  
                if maze[y][x][0]==0 or maze[y][x][2]==0:
                    break             

        numChoices = 0
        
        print(x,y)

        numMoves = numMoves + 1
    return numMoves

print(rand_mouse(maze))
            
        
