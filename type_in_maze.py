'''
Created on Mar 12, 2018

@author: dexca
'''
import numpy as np
import turtle
screen_size = 400
maze_size = 15
unit_size = screen_size/maze_size

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


   

#input_maze(maze_size)
maze = np.array([(    [1,0],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [0,1],        [1,1],        [0,1],        [0,1],        [0,1],        [0,1],        [1,1],        [0,1],        [0,1],        [1,0]        ),
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
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Small Maze")
wn.setup(screen_size+10,screen_size+10)
pen = Pen()

draw_maze(maze)

for x in range(maze_size+1):
    print(maze[x]) 
wn.exitonclick()
