import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def rotateX(angle):
    m = np.array([
        [1, 0, 0, 0], 
        [0, np.cos(angle*np.pi/180), -np.sin(angle*np.pi/180), 0],
        [0, np.sin(angle*np.pi/180), np.cos(angle*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)
   
def rotateY(angle):
    m = np.array([
        [np.cos(angle*np.pi/180), 0, np.sin(angle*np.pi/180), 0], 
        [0, 1, 0, 0],
        [-np.sin(angle*np.pi/180), 0, np.cos(angle*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

def rotateZ(angle):
    m = np.array([
        [np.cos(angle*np.pi/180), -np.sin(angle*np.pi/180), 0, 0], 
        [np.sin(angle*np.pi/180), np.cos(angle*np.pi/180), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

def rotateXYZ(x, y, z):
    m = np.array([
        [np.cos(y*np.pi/180)*np.cos(z*np.pi/180), -np.cos(y*np.pi/180)*np.sin(z*np.pi/180), np.sin(y*np.pi/180), 0],
        [np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.cos(x*np.pi/180)*np.sin(z*np.pi/180), -np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.cos(x*np.pi/180)*np.cos(z*np.pi/180), -np.sin(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [-np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.sin(x*np.pi/180)*np.sin(z*np.pi/180), np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.sin(x*np.pi/180)*np.cos(z*np.pi/180), np.cos(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)


    m = np.array([
        [1, 0, 0, 0], 
        [0, 1, 0, 0],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m.T)

def translateXYZ(x, y, z):
    m = np.array([
        [1, 0, 0, x], 
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m.T)

def scale(ratio):
    m = np.array([
        [ratio, 0, 0, 0], 
        [0, ratio, 0, 0],
        [0, 0, ratio, 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -8)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scale(1.1)
                else:
                    scale(0.9)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    rotateXYZ(event.rel[1], event.rel[0], 0)
                if pygame.mouse.get_pressed()[2]:
                    translateXYZ(event.rel[0]/100, -event.rel[1]/100, 0)
                
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
        
main()