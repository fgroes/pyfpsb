import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys
import ctypes
from program import Program
from shader import Shader, ShaderType
from shader_codes import vertex_shader_code, fragment_shader_code
from data import load_data


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
    gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
    glut.glutSwapBuffers()


def reshape(width, height):
    gl.glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == "\033": sys.exit()


class Graphics(object):

    def __init__(self):
        self._init_graphics()

    def _init_graphics(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
        glut.glutCreateWindow("Hello world!")
        glut.glutReshapeWindow(512, 512)
        glut.glutReshapeFunc(reshape)
        glut.glutDisplayFunc(display)
        #glut.glutKeyboardFunc(keyboard)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def set_data(self, data, indices):
        self.data = data
        self.indices = indices 

    def buffer_data(self):
        vertex_buffer_id = gl.glGenBuffers(1)
        offset = ctypes.c_void_p(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        stride = 6 * data.itemsize
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)

        index_buffer_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, index_buffer_id)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(1)
        offset = ctypes.c_void_p(3 * data.itemsize)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)  

    def create_program(self):
        self.vertex_shader = Shader(ShaderType.VERTEX)
        self.vertex_shader.set_shader_source(vertex_shader_code)
        self.vertex_shader.compile()

        self.fragment_shader = Shader(ShaderType.FRAGMENT)
        self.fragment_shader.set_shader_source(fragment_shader_code)
        self.fragment_shader.compile()

        self.program = Program()
        self.program.attach_shader(self.vertex_shader)
        self.program.attach_shader(self.fragment_shader)
        self.program.link()
        self.program.use()

    def start(self):
        glut.glutMainLoop()


if __name__ == "__main__":
    g = Graphics()
    data, indices = load_data() 
    g.set_data(data, indices)
    g.buffer_data()
    g.create_program()
    g.start()
