import pygame

import pywavefront
from pywavefront import Wavefront
from objLoader import ObjLoader
from OpenGL.GL.shaders import compileProgram, compileShader
from pygame.locals import *
import pyrr

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

class Window():
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
    
    def __init__(self) -> None:   
        pygame.init()
        self.display = (800,600)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)

         # load here the 3d meshes
        self.chibi_indices, self.chibi_buffer = ObjLoader.load_model("src/blender_objs/logo_furg.obj")
        self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))

        # VAO and VBO
        self.VAO = glGenVertexArrays(2)
        self.VBO = glGenBuffers(2)
        # Chibi VAO
        glBindVertexArray(self.VAO[0])
        # Chibi Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.chibi_buffer.nbytes, self.chibi_buffer, GL_STATIC_DRAW)
        # chibi vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.chibi_buffer.itemsize * 8, ctypes.c_void_p(0))
        # chibi textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.chibi_buffer.itemsize * 8, ctypes.c_void_p(12))
        # chibi normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.chibi_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        glUseProgram(self.shader)
        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        self.chibi_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -5, -10]))

        self.view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
        self.model_loc = glGetUniformLocation(self.shader, "model")
        self.proj_loc = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)
        self.model = self.chibi_pos
        self.scale(0.3)
   
 
    
    def rotateX(self,angle):
        self.rot_x = np.array([
        [1, 0, 0, 0], 
        [0, np.cos(angle*np.pi/180), -np.sin(angle*np.pi/180), 0],
        [0, np.sin(angle*np.pi/180), np.cos(angle*np.pi/180), 0],
        [0, 0, 0, 1]
        ])
        self.model=pyrr.matrix44.multiply(self.rot_x,self.chibi_pos)
        self.chibi_pos=self.model
        
    def rotateY(self,angle):
        self.rot_y = np.array([
        [np.cos(angle*np.pi/180), 0, np.sin(angle*np.pi/180), 0], 
        [0, 1, 0, 0],
        [-np.sin(angle*np.pi/180), 0, np.cos(angle*np.pi/180), 0],
        [0, 0, 0, 1]
    ])
        self.model=pyrr.matrix44.multiply(self.rot_y,self.chibi_pos)
        self.chibi_pos=self.model

    def rotateZ(self,angle):
        self.rot_z =  np.array([
        [np.cos(angle*np.pi/180), -np.sin(angle*np.pi/180), 0, 0], 
        [np.sin(angle*np.pi/180), np.cos(angle*np.pi/180), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
        self.model=pyrr.matrix44.multiply(self.rot_z,self.chibi_pos)
        self.chibi_pos=self.model

    def rotateXYZ(self,x, y, z):
        self.rot_x_y_z=np.array([
            [np.cos(y*np.pi/180)*np.cos(z*np.pi/180), -np.cos(y*np.pi/180)*np.sin(z*np.pi/180), np.sin(y*np.pi/180), 0],
            [np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.cos(x*np.pi/180)*np.sin(z*np.pi/180), -np.sin(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.cos(x*np.pi/180)*np.cos(z*np.pi/180), -np.sin(x*np.pi/180)*np.cos(y*np.pi/180), 0],
            [-np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.cos(z*np.pi/180)+np.sin(x*np.pi/180)*np.sin(z*np.pi/180), np.cos(x*np.pi/180)*np.sin(y*np.pi/180)*np.sin(z*np.pi/180)+np.sin(x*np.pi/180)*np.cos(z*np.pi/180), np.cos(x*np.pi/180)*np.cos(y*np.pi/180), 0],
            [0, 0, 0, 1]
        ])
        self.model=pyrr.matrix44.multiply(self.rot_x_y_z,self.chibi_pos)
        self.chibi_pos=self.model
            

         
       

       
    def draw(self):

        glBindVertexArray(self.VAO[0])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE,self.model)
        glDrawArrays(GL_TRIANGLES, 0, len(self.chibi_indices))
    def translateXYZ(self, x, y, z):
        self.translate = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])
        self.model=pyrr.matrix44.multiply(self.model,self.translate)
        self.chibi_pos=self.model

    def scale(self,ratio):
        m = np.array([
            [ratio, 0, 0, 0], 
            [0, ratio, 0, 0],
            [0, 0, ratio, 0],
            [0, 0, 0, 1]
        ])
        self.model=pyrr.matrix44.multiply(self.model,m)
        self.chibi_pos=self.model

    def ortho(self,left, right, bottom, top, near, far):
        self.__init__()
        

    def frustum(self,left, right, bottom, top, near, far):
        self.__init__()
        m = np.array([
            [2*near/(right-left), 0, (right+left)/(right-left), 0],
            [0, 2*near/(top-bottom), (top+bottom)/(top-bottom), 0],
            [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
            [0, 0, -1, 0]
        ])
        self.projection = m.T
        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)


    def setZBuffer(self):
        glEnable(GL_DEPTH_TEST)
        
    def Phong(self):
        self.__init__()
        self.light_pos = np.array([0, 0, 0, 1])
        self.light_color = np.array([1, 1, 1, 1])
        self.ambient_color = np.array([0.1, 0.1, 0.1, 1])
        self.diffuse_color = np.array([0.5, 0.5, 0.5, 1])
        self.specular_color = np.array([0.5, 0.5, 0.5, 1])
        self.shininess = 100
        self.ambient_loc = glGetUniformLocation(self.shader, "ambient_color")
        self.diffuse_loc = glGetUniformLocation(self.shader, "diffuse_color")
        self.specular_loc = glGetUniformLocation(self.shader, "specular_color")
        self.light_pos_loc = glGetUniformLocation(self.shader, "light_pos")
        self.light_color_loc = glGetUniformLocation(self.shader, "light_color")
        self.shininess_loc = glGetUniformLocation(self.shader, "shininess")
        glUniform4fv(self.ambient_loc, 1, self.ambient_color)
        glUniform4fv(self.diffuse_loc, 1, self.diffuse_color)
        glUniform4fv(self.specular_loc, 1, self.specular_color)
        glUniform4fv(self.light_pos_loc, 1, self.light_pos)
        glUniform4fv(self.light_color_loc, 1, self.light_color)
        glUniform1f(self.shininess_loc, self.shininess)
        self.setZBuffer()
        self.loadTexture()

       





    def Point(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        glColor(1,1,1)
        glVertex3f(pos_luz[0], pos_luz[1], pos_luz[2])
        glEnd()


    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.scale(1.1)
                    else:
                        self.scale(0.9)
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        self.rotateXYZ(event.rel[1], event.rel[0], 0)
                    if pygame.mouse.get_pressed()[2]:
                        self.translateXYZ(event.rel[0]/100, -event.rel[1]/100, 0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        self.ortho(-1, 1, -1, 1, -1, 1)
     
                    if event.key == pygame.K_p:
                        glLoadIdentity()
                        self.frustum(-1, 1, -1, 1, 1, 500)

                        
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.draw()      
            
            pygame.display.flip()
            pygame.time.wait(10)
            
if __name__ == "__main__":
    main = Window()
    main.main()