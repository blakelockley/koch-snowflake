#!/usr/bin/env python3

from PIL import Image, ImageDraw
from math import sqrt,cos, sin, pi

# canvas
SIDE = 1000
THIRD = SIDE / 3
HALF = SIDE / 2

# shape
LINE_LENGTH = SIDE * 0.4
COLOR = (0, 255, 0)
ITERATIONS = 2


# helper function to determine the length of a line (distance between two points)
def distance(start, end):
    x = end[0] - start[0]
    y = end[1] - start[1]
    
    return sqrt(x * x + y * y)


# helper function to add two points
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


# helper function to normalise a vector
def normalise(vec):
    x = vec[0]
    y = vec[1]
    
    len = sqrt(x*x + y*y)
    
    return (x / len, y / len)


# helper function to determine a vector from two points
def vectorise(start, end):
    vec = (end[0] - start[0], end[1] - start[1])
    return normalise(vec)


# helper funciton to rotate a vector
# | cos t -sin t | | x | = | x * cos t - y * -sin t |
# | sin t  cos t | | y |   | x * sin t + y *  cos t |
def rotate(vec, degrees):
    # convert degrees to radians
    angle = degrees * pi / 180
    
    cos_t = cos(angle)
    sin_t = sin(angle)
    
    x = vec[0]
    y = vec[1]
    
    rx = x * cos_t + y * -sin_t
    ry = x * sin_t + y *  cos_t
    
    return (rx, ry)


# helper function to multiply a vector by a scalar
def multiply(vec, s):
    return (vec[0] * s, vec[1] * s)


# initalise image and painter (draw)
im = Image.new("RGB", (SIDE, SIDE))
draw = ImageDraw.Draw(im)

# define recursive function to draw the line segment
def segment(start, end, n):
    if n == 0:
        draw.line(start + end, fill=COLOR)
        return
    
    vec = vectorise(start, end)
    r = rotate(vec, 60)

    segment_length = distance(start, end) * (1 / 3)

    # how we want to draw our line:
    # start -> one_third -> middle -> two_third -> end

    # make our points
    one_third = add(multiply(vec, segment_length), start)
    middle    = add(multiply(r,   segment_length), one_third)
    two_third = add(multiply(vec, 2 * segment_length), start)

    # draw our four line segments
    segment(start, one_third, n - 1)
    segment(one_third, middle, n - 1)
    segment(middle, two_third, n - 1)
    segment(two_third, end, n - 1)

# make top level trianagle points
center = (HALF, HALF)
up_vec = (0, -1)
left_vec = rotate(up_vec, 120)
right_vec = rotate(up_vec, -120)

# determine triangles points
top   = add(center, multiply(up_vec, LINE_LENGTH))
left  = add(center, multiply(left_vec, LINE_LENGTH))
right = add(center, multiply(right_vec, LINE_LENGTH))

# draw segments
segment(top, right, ITERATIONS)
segment(right, left, ITERATIONS)
segment(left, top, ITERATIONS)

# display and save the image
im.show()
with open("out.png", "wb") as f:
    im.save(f)







