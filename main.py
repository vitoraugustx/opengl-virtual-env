import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from obj_loader import *
import math

def rotateX(angle):
    m=np.array([
        [1,0,0,0],
        [0,math.cos(angle),-math.sin(angle),0],
        [0,math.sin(angle),math.cos(angle),0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

def rotateY(angle):
    m=np.array([
        [math.cos(angle),0,math.sin(angle),0],
        [0,1,0,0],
        [-math.sin(angle),0,math.cos(angle),0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

def rotateZ(angle):
    m=np.array([
        [math.cos(angle),-math.sin(angle),0,0],
        [math.sin(angle),math.cos(angle),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

def rotateXYZ(x,y,z):
    m=np.array([
        [np.cos(y*np.pi/180)*np.cos(z*np.pi/180), -np.cos(y*np.pi/180)*np.sin(z*np.pi/180), np.sin(y*np.pi/180), 0],
        [np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.cos(x*np.pi/180)*np.sin(z*np.pi/180), -np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.cos(x*np.pi/180)*np.cos(z*np.pi/180), -np.sin(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [-np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.sin(x*np.pi/180)*np.sin(z*np.pi/180), np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.sin(x*np.pi/180)*np.cos(z*np.pi/180), np.cos(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

def translateXYZ(x,y,z):

    m=np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [x,y,z,1]
    ])
    glMultMatrixf(m)

def scale(rate):
    m=np.array([
        [rate,0,0,0],
        [0,rate,0,0],
        [0,0,rate,0],
        [0,0,0,1]
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
        glLoadIdentity()
        
        m = np.array([
            [2*near/(right-left), 0, (right+left)/(right-left), 0],
            [0, 2*near/(top-bottom), (top+bottom)/(top-bottom), 0],
            [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
            [0, 0, -1, 0]
        ])
        projection = m
        glMultMatrixf(projection)
        glTranslatef(0, 0, -10)
        scale(0.9)
    
def setZBuffer():
	glEnable(GL_DEPTH_TEST)

def setLight():
    # Iluminação
    glEnable(GL_LIGHTING)

    # Conjuto de luzes
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    # Propriedades da cor do material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (.2, .2, .2, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (.1, .1, .1, 1))
    glLight(GL_LIGHT0, GL_POSITION,  (0, 5, 6, 1))

    # Luz 4
    glLightfv(GL_LIGHT1, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (.1, .1, .1, 1))
    glLight(GL_LIGHT1, GL_POSITION,  (5, 0, 6, 1))

    # Luz 5
    glLightfv(GL_LIGHT2, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT2, GL_DIFFUSE, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT2, GL_SPECULAR, (.1, .1, .1, 1))
    glLight(GL_LIGHT2, GL_POSITION,  (-5, 0, 6, 1))


pygame.init()
display = (800, 450)

pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
clock = pygame.time.Clock()

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
setZBuffer()
glTranslatef(0.0,0.0, -15)
scale(rate=0.5)

setLight()

model = OBJ('src/blender_objs/logo_furg.obj')

run = True
while run:
    clock.tick(120)
    keys = pygame.key.get_pressed()
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
                rotateXYZ(-event.rel[1], -event.rel[0], 0)
                
            if pygame.mouse.get_pressed()[2]:
                translateXYZ(event.rel[0]/100, -event.rel[1]/100, 0)

        if keys[pygame.K_w]:
            translateXYZ(0, 0, 0.1)

        if keys[pygame.K_s]:
            translateXYZ(0, 0, -0.1)

        if keys[pygame.K_RIGHT]:
            rotateXYZ(0, 0, -1)
        
        if keys[pygame.K_LEFT]:
            rotateXYZ(0, 0, 1)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                glLoadIdentity()
                ortho(-1, 1, -1, 1, -1, 1)
                scale(0.05)
                setLight()

                
            if event.key == pygame.K_r:
                glLoadIdentity()
                gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
                glTranslatef(0.0,0.0, -15)
                scale(rate=0.5)
                setLight()

            if event.key == pygame.K_p:
                frustum(-1, 1, -1, 1, 1, 100)  
                setLight()
                  
                    

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.31, 0.31, 0.31, 0.5)
    
    glPushMatrix()
    
    model.render()
    glPopMatrix()

    
    pygame.display.flip()

pygame.quit()
quit()