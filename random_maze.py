'''
Created on Mar 12, 2018

@author: dexca
'''
import numpy as np
import turtle
import random

screen_size = 600
maze_size = 25
unit_size = screen_size/maze_size

maze = np.zeros((maze_size+1,maze_size+1,2),dtype=np.int)


direction = {0: "left", 1: "up"}

def input_maze(size):
    for x in range(size+1):
        for y in range(size+1):
            for k in range(2):
                temp = random.randint(0,1)
                print ("cell",x,y,direction[k], temp)
                maze[x][y][k] = temp 

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
    for y in range(maze_size+1):
        for x in range(maze_size+1):
            screen_x = -(screen_size/2) + (x*unit_size)
            screen_y = (screen_size/2) - (y*unit_size)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][1]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()  
    
    for x in range(maze_size+1):
        for y in range(maze_size+1):
            screen_x = -(screen_size/2) + (x*unit_size)
            screen_y = (screen_size/2) - (y*unit_size)            
            pen.goto(screen_x,screen_y)
            if maze[y][x][0]==1:
                pen.pendown()
            else:
                pen.penup()
        pen.penup()       
    
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Small Maze")
wn.setup(screen_size+10,screen_size+10)


pen = Pen()
input_maze(maze_size)
draw_maze(maze)

wn.exitonclick()


