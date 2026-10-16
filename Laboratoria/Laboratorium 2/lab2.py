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


def paintQuad(x, y, a, b):  # Task 2
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)
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


def paintTriangles():  # Task 1
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


def drawSierpinski(x, y, a, b, depth, d=0.0):   # Task 4
    if depth == 0:
        return

    w = a / 3.0
    h = b / 3.0

    # Wycięcie środkowego otworu przy użyciu koloru tła (szary: 0.5, 0.5, 0.5)
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(x + w, y + h)
    glVertex2f(x + 2 * w, y + h)
    glVertex2f(x + 2 * w, y + 2 * h)
    glVertex2f(x + w, y + 2 * h)
    glEnd()

    # Wywołania rekurencyjne dla 8 otaczających ćwiartek
    drawSierpinski(x, y, w, h, depth - 1, d)
    drawSierpinski(x + w, y, w, h, depth - 1, d)
    drawSierpinski(x + 2 * w, y, w, h, depth - 1, d)

    drawSierpinski(x, y + h, w, h, depth - 1, d)
    drawSierpinski(x + 2 * w, y + h, w, h, depth - 1, d)

    drawSierpinski(x, y + 2 * h, w, h, depth - 1, d)
    drawSierpinski(x + w, y + 2 * h, w, h, depth - 1, d)
    drawSierpinski(x + 2 * w, y + 2 * h, w, h, depth - 1, d)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    random.seed(42)

    N = 3
    def_val = 0.0

    glBegin(GL_QUADS)
    glColor3f(0.6, 0.25, 0.05)
    glVertex2f(-90, -50)
    glVertex2f(90, -50)
    glVertex2f(90, 50)
    glVertex2f(-90, 50)
    glEnd()

    drawSierpinski(-90, -50, 180, 100, depth=N, d=def_val)

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