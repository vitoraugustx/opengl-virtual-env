import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from obj_loader import *
import math

# Rotação no eixo X
def rotateX(angle):
    m=np.array([
        [1,0,0,0],
        [0,math.cos(angle),-math.sin(angle),0],
        [0,math.sin(angle),math.cos(angle),0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

# Rotação no eixo Y	
def rotateY(angle):
    m=np.array([
        [math.cos(angle),0,math.sin(angle),0],
        [0,1,0,0],
        [-math.sin(angle),0,math.cos(angle),0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

# Rotação no eixo Z
def rotateZ(angle):
    m=np.array([
        [math.cos(angle),-math.sin(angle),0,0],
        [math.sin(angle),math.cos(angle),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

# Rotação no eixo XYZ
def rotateXYZ(x,y,z):
    m=np.array([
        [np.cos(y*np.pi/180)*np.cos(z*np.pi/180), -np.cos(y*np.pi/180)*np.sin(z*np.pi/180), np.sin(y*np.pi/180), 0],
        [np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.cos(x*np.pi/180)*np.sin(z*np.pi/180), -np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.cos(x*np.pi/180)*np.cos(z*np.pi/180), -np.sin(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [-np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.sin(x*np.pi/180)*np.sin(z*np.pi/180), np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.sin(x*np.pi/180)*np.cos(z*np.pi/180), np.cos(x*np.pi/180)*np.cos(y*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

# Translação no eixo XYZ
def translateXYZ(x,y,z):
    m=np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [x,y,z,1]
    ])
    glMultMatrixf(m)

# Função de escala
def scale(rate):
    m=np.array([
        [rate,0,0,0],
        [0,rate,0,0],
        [0,0,rate,0],
        [0,0,0,1]
    ])
    glMultMatrixf(m)

# Projeção ortográfica
def ortho(left, right, bottom, top, near, far):
    m = np.array([
        [2/(right-left), 0, 0, -(right+left)/(right-left)],
        [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
        [0, 0, -2/(far-near), -(far+near)/(far-near)],
        [0, 0, 0, 1]
    ])
    glMultMatrixf(m)

# Projeção perspectiva
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
        scale(0.8)
    
# Habilita o algoritmo z-buffer
def setZBuffer():
	glEnable(GL_DEPTH_TEST)

def perspective(fov, aspect, near, far):
    glLoadIdentity()
    m=np.array([
        [1/(aspect*np.tan(fov/2)), 0, 0, 0],
        [0, 1/np.tan(fov/2), 0, 0],
        [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
        [0, 0, -1, 0]
    ])
    glMultMatrixf(m.T)
    glTranslatef(0, 0, -15)
    scale(0.7)

# Define as luzes
def setLight(intensity = 1):
    # Iluminação
    glEnable(GL_LIGHTING)

    # Conjuto de luzes
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)

    # Propriedades da cor do material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz 0
    # Componentes de cor ambiente, difusa e especular
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (.2, .2, .2, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (.1, .1, .1, 1))
    # Intensidade da luz
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, intensity)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, intensity)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, intensity)
    # Posição da luz
    glLight(GL_LIGHT0, GL_POSITION,  (0, 5, 8, 1))

    # Luz 1
    # Componentes de cor ambiente, difusa e especular
    glLightfv(GL_LIGHT1, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (.2, .2, .2, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (.1, .1, .1, 1))
    # Intensidade da luz
    glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, intensity)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, intensity)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, intensity)
    # Posição da luz
    glLight(GL_LIGHT1, GL_POSITION,  (5, 0, 8, 1))

    # Luz 2
    # Componentes de cor ambiente, difusa e especular
    glLightfv(GL_LIGHT2, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT2, GL_DIFFUSE, (.2, .2, .2, 1))
    glLightfv(GL_LIGHT2, GL_SPECULAR, (.1, .1, .1, 1))
    # Intensidade da luz
    glLightfv(GL_LIGHT2, GL_CONSTANT_ATTENUATION, intensity)
    glLightfv(GL_LIGHT2, GL_LINEAR_ATTENUATION, intensity)
    glLightfv(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, intensity)
    # Posição da luz
    glLight(GL_LIGHT2, GL_POSITION,  (-5, 0, 8, 1))

    # Luz 3
    # Componentes de cor ambiente, difusa e especular
    glLightfv(GL_LIGHT3, GL_AMBIENT, (.1, .1, .1, 1))
    glLightfv(GL_LIGHT3, GL_DIFFUSE, (.2, .2, .2, 1))
    glLightfv(GL_LIGHT3, GL_SPECULAR, (.1, .1, .1, 1))
    # Intensidade da luz
    glLightfv(GL_LIGHT3, GL_CONSTANT_ATTENUATION, intensity)
    glLightfv(GL_LIGHT3, GL_LINEAR_ATTENUATION, intensity)
    glLightfv(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, intensity)
    # Posição da luz
    glLight(GL_LIGHT3, GL_POSITION,  (0, 0, 8, 1))

# MAIN
pygame.init()

# Tamanho da tela
display = (850, 450)

# Inicializa a tela
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
pygame.display.set_caption("Sistemas gráficos - Logos FURG e C3")

# Definição de relógio para controle de FPS
clock = pygame.time.Clock()

# Inicializa a projeção como perspectiva
perspective(45, display[0]/display[1], 0.1, 50.0)

# Algoritmo de visualização
setZBuffer()

# Inicializa as luzes
setLight()

# Carrega o modelo
model = OBJ('src/blender_objs/logo_furg.obj')
#model = OBJ('src/blender_objs/logo_c3.obj')

# Loop principal
while True:
    clock.tick(120)
    # Eventos
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        # Sair
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Redimensionar
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                scale(1.1)
            else:
                scale(0.9)

        # Rotacionar
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                rotateXYZ(-event.rel[1], -event.rel[0], 0)
                
            if pygame.mouse.get_pressed()[2]:
                translateXYZ(event.rel[0]/100, -event.rel[1]/100, 0)

        # Transladar em Z
        if keys[pygame.K_w]:
            translateXYZ(0, 0, 0.1)

        if keys[pygame.K_s]:
            translateXYZ(0, 0, -0.1)

        # Rotacionar em Z
        if keys[pygame.K_RIGHT]:
            rotateXYZ(0, 0, -1)
        
        if keys[pygame.K_LEFT]:
            rotateXYZ(0, 0, 1)

        if event.type == pygame.KEYDOWN:
            # Projeção ortográfica
            if event.key == pygame.K_o:
                glLoadIdentity()
                ortho(-1, 1, -1, 1, -1, 1)
                scale(0.09)
                setLight()

            # Recarrega a cena na projeção perspectiva
            if event.key == pygame.K_r:
                perspective(45, (display[0]/display[1]), 0.1, 50.0)
                setLight()
            
            # Projeção perspectiva alternativa (frustrum)
            if event.key == pygame.K_p:
                translateXYZ(0, 0, 10)
                frustum(-1, 1, 0, 1, 1, 50)  
                setLight()
                    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Defini cor de fundo
    glClearColor(0.31, 0.31, 0.31, 0.5)
    
    # Desenha o modelo
    glPushMatrix()
    model.render()
    glPopMatrix()

    pygame.display.flip()

pygame.quit()
quit()
