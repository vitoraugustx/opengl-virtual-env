
vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

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
    

pygame.init()
display = (640, 480)

pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

model = OBJ('src/blender_objs/logo_furg.obj')
box = model.box()
center = [(box[0][i] + box[1][i])/2 for i in range(3)]
size = [box[1][i] - box[0][i] for i in range(3)]
scale(0.1)
run = True
while run:
    clock.tick(100)
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
                    scale(0.1)

    
                if event.key == pygame.K_p:
                    frustum(-1, 1, -1, 1, 1, 100)
                    
                    
   
                    
                    

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    model.render()
    glPopMatrix()

    
    pygame.display.flip()

pygame.quit()
quit()