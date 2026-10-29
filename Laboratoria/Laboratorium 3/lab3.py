#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

N = 50
tab = [[[0.0] * 3 for i in range(N)] for j in range(N)]
colors = [[[0.0] * 3 for i in range(N)] for j in range(N)]

u_array = [i / (N - 1) for i in range(N)]
v_array = [i / (N - 1) for i in range(N)]


def calculate_egg():
    for i in range(N):
        u = u_array[i]
        for j in range(N):
            v = v_array[j]

            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * 2 * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * 2 * v)

            tab[i][j][0] = x
            tab[i][j][1] = y
            tab[i][j][2] = z

            colors[i][j][0] = random.random()
            colors[i][j][1] = random.random()
            colors[i][j][2] = random.random()

    for i in range(N):
        colors[i][N - 1] = colors[i][0]


def spin(angle):
    glRotatef(angle, 1.0, 1.0, 0.0)


def draw_egg_points():
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])
    glEnd() #


def draw_egg_lines():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(N):
        for j in range(N):
            if i < N - 1:
                glVertex3fv(tab[i][j])
                glVertex3fv(tab[i + 1][j])
            if j < N - 1:
                glVertex3fv(tab[i][j])
                glVertex3fv(tab[i][j + 1])
    glEnd()


def draw_egg_triangles():
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
            glColor3fv(colors[i][j + 1])
            glVertex3fv(tab[i][j + 1])

            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
            glColor3fv(colors[i + 1][j + 1])
            glVertex3fv(tab[i + 1][j + 1])
            glColor3fv(colors[i][j + 1])
            glVertex3fv(tab[i][j + 1])
    glEnd()


def draw_egg_triangle_strip():
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            glColor3fv(colors[i + 1][j])
            glVertex3fv(tab[i + 1][j])
        glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    calculate_egg()


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    angle = time * 180 / math.pi
    spin(angle)

    axes()
    # draw_egg_points()
    # draw_egg_lines()
    # draw_egg_triangles()
    draw_egg_triangle_strip()

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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