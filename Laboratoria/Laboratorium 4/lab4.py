#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

eye_x = 0.0
eye_y = 0.0
eye_z = 10.0

yaw = -90.0
pitch = 0.0

keys = {
    GLFW_KEY_W: False,
    GLFW_KEY_S: False,
    GLFW_KEY_A: False,
    GLFW_KEY_D: False
}

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    gluSphere(quadric, 1.5, 10, 10)
    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)
    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)
    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)
    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global eye_x, eye_y, eye_z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    yaw_rad = math.radians(yaw)
    pitch_rad = math.radians(pitch)

    front_x = math.cos(yaw_rad) * math.cos(pitch_rad)
    front_y = math.sin(pitch_rad)
    front_z = math.sin(yaw_rad) * math.cos(pitch_rad)

    right_x = math.cos(yaw_rad - math.pi / 2.0)
    right_z = math.sin(yaw_rad - math.pi / 2.0)

    speed = 0.1
    if keys[GLFW_KEY_W]:
        eye_x += front_x * speed
        eye_y += front_y * speed
        eye_z += front_z * speed
    if keys[GLFW_KEY_S]:
        eye_x -= front_x * speed
        eye_y -= front_y * speed
        eye_z -= front_z * speed
    if keys[GLFW_KEY_A]:
        eye_x -= right_x * speed
        eye_z -= right_z * speed
    if keys[GLFW_KEY_D]:
        eye_x += right_x * speed
        eye_z += right_z * speed

    gluLookAt(eye_x, eye_y, eye_z,
              eye_x + front_x, eye_y + front_y, eye_z + front_z,
              0.0, 1.0, 0.0)

    axes()
    example_object()
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)
    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key in keys:
        if action == GLFW_PRESS:
            keys[key] = True
        elif action == GLFW_RELEASE:
            keys[key] = False


def mouse_motion_callback(window, x_pos, y_pos):
    global mouse_x_pos_old, mouse_y_pos_old, yaw, pitch

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old
    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    if left_mouse_button_pressed:
        yaw += delta_x * 0.2
        pitch -= delta_y * 0.2

        if pitch > 89.0:
            pitch = 89.0
        elif pitch < -89.0:
            pitch = -89.0


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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