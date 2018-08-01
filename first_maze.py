'''
Created on Mar 11, 2018

@author: dexca
'''

import turtle

wn = turtle.Screen()
wn.bgcolor("White")
wn.title("Small Maze")
wn.setup(400,400)

#create pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)

level = [
    " XXXXXXXXXX",
    "     XXX  X",
    "X X XXXX XX",
    "X X      XX",
    "X   XXXX XX",
    "X X X  X XX",
    "X X   XXXXX",
    "X X X     X",
    "XXX XXXXX X",
    "XXXXXXXXX X",
    "XXXXXXXXX X"
    ]

def record_maze(level):
    for y in range(len(level)):
        for x in range(len(level)):
            character = level[y][x]
            screen_x = -180 + (x*20)
            screen_y = 180 - (y*20)
            if character == "X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                
pen = Pen()

record_maze(level)
wn.exitonclick()