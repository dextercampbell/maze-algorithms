'''
Created on Apr 2, 2018

@author: dexca
'''
import numpy as np
from collections import deque
import turtle
from root.nested import dijkstraDraw
from dijkstraDraw import backtrackerGen
from dijkstraDraw import Pen
from dijkstraDraw import drawMaze
from dijkstraDraw import dijkstra

mazeSize = 25
screenSize = 500
unitSize = screenSize/mazeSize
pathSpeed = 100
mazeSpeed = 0

maze = backtrackerGen(mazeSize)
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Dijkstra Maze")
wn.setup(screenSize+25,screenSize+25)
pen = Pen()

drawMaze(maze,mazeSize,screenSize,mazeSpeed,pen)
print(dijkstra(maze,mazeSize,screenSize,pen,pathSpeed))
wn.exitonclick()