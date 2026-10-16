#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def paintQuad(x,y,a,b): # Task 2
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x+a, y+b)
    glVertex2f(x, y+b)
    glEnd()


def paintQuad2(x, y, a, b, d=0):  # Task 3
    random.seed(d)
    glBegin(GL_QUADS)

    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + random.uniform(-d, d), y + random.uniform(-d, d))
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a + random.uniform(-d, d), y + random.uniform(-d, d))
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + a + random.uniform(-d, d), y + b + random.uniform(-d, d))
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(x + random.uniform(-d, d), y + b + random.uniform(-d, d))

    glEnd()


def paintTriangles():   # Task 1
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.0, 0.0)
    glVertex2f(-60, 10)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-100, -50)
    glColor3f(0.0, 0.75, 0.75)
    glVertex2f(-15, -15)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-100, 50)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(50, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(100, 100)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #paintTriangles()
    #paintQuad(-50,-50,50,100)
    paintQuad2(-50,-50,50,100, 150)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
