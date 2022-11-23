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

pos_luz = [20,8,-5,1]
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

def ortho(left, right, bottom, top, near, far):
    m = np.array([
        [2/(right-left), 0, 0, -(right+left)/(right-left)],
        [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
        [0, 0, -2/(far-near), -(far+near)/(far-near)],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

def frustum(left, right, bottom, top, near, far):
    m = np.array([
        [2*near/(right-left), 0, (right+left)/(right-left), 0],
        [0, 2*near/(top-bottom), (top+bottom)/(top-bottom), 0],
        [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
        [0, 0, -1, 0]
    ])
    #m=np.transpose(m)
    glMultMatrixf(m)



def loadTexture():
    textureSurface = pygame.image.load('imgs/texture.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid

def renderLight():
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	glShadeModel(GL_SMOOTH)
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_TEXTURE_2D)
	specReflection = [1.0, 1.0, 1.0, 1.0]
	glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)
	glMateriali(GL_FRONT, GL_SHININESS, 30)
	glLightfv(GL_LIGHT0, GL_POSITION, pos_luz)
    
def Point():
    glPointSize(10)

    glBegin(GL_POINTS)
    glColor(1,1,1)
    glVertex3f(pos_luz[0], pos_luz[1], pos_luz[2])
    glEnd()

def Cube(lines):
    if lines:
        glBegin(GL_LINES)
        for edge in edges:
            glColor3fv((1, 1, 1))
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
    else:
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0,  1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0, -1.0,  1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    loadTexture()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    renderLight()
    Point()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    glLoadIdentity()
                    ortho(-1, 1, -1, 1, -1, 1)
                    scale(0.5)
                if event.key == pygame.K_p:
                    glLoadIdentity()
                    frustum(-1, 1, -1, 1, 1, 500)
                    glTranslatef(0.0,0.0, -8)

                if event.key == pygame.K_r:
                    glLoadIdentity()
                    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
                    glTranslatef(0.0,0.0, -8)

  
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube(False)
        pygame.display.flip()
        pygame.time.wait(10)
        
main()