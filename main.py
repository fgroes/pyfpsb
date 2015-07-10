import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys
import ctypes
from program import Program
from shader import Shader, ShaderType
from shader_codes import vertex_shader_code, fragment_shader_code
from data import load_data, load_cube



def translate(v):
    t = np.eye(4, 4)
    t[0:3, 3] = v
    return t


def perspective(near, far, right, left, top, bottom):
    p = np.zeros((4, 4), dtype=np.float32)
    p[0, 0] = 2 * near / (right - left)
    p[0, 2] = (right + left) / (right - left)
    p[1, 1] = 2 * near / (top - bottom)
    p[1, 2] = (top + bottom) / (top - bottom)
    p[2, 2] = - (far + near) / (far - near)
    p[2, 3] = - 2 * near * far / (far - near)
    p[3, 2] = -1
    return p


def perspective_fov(near, far, angle, aspect):
    p = np.zeros((4, 4), dtype=np.float32)
    f = 1.0 / np.tan(angle / 2)
    p[0, 0] = f / aspect
    p[1, 1] = f
    p[2, 2] = - (far + near) / (near - far)
    p[2, 3] = 2 * near * far / (near - far)
    p[3, 2] = 1
    return p


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
    gl.glDrawElements(gl.GL_TRIANGLES, 9, gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
    glut.glutSwapBuffers()


def reshape(width, height):
    gl.glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == "\033": sys.exit()


class GraphicsError(Exception):
    pass


class NoVertexShaderCodeError(GraphicsError):
    pass


class NoFragmentShaderCodeError(GraphicsError):
    pass



class Graphics(object):

    def __init__(self):
        self.window_width = 1280
        self.window_height = 800
        self.window_title = "pyfpsb"
        self.vertex_shader_code = None
        self.fragment_shader_code = None

    def init_graphics(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
        glut.glutCreateWindow(self.window_title)
        glut.glutReshapeWindow(self.window_width, self.window_height)
        glut.glutReshapeFunc(reshape)
        glut.glutDisplayFunc(display)
        glut.glutKeyboardFunc(keyboard)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def set_data(self, data, indices):
        self.data = data
        self.indices = indices
        vertex_buffer_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        stride = self.data.strides[0]
        offset = ctypes.c_void_p(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)
        offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)

        index_buffer_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, index_buffer_id)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(1)

        m = translate(np.array([0, 0, 0]))
        loc = gl.glGetUniformLocation(self.program.program_id, "model")
        gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, m)

        v = np.eye(4, 4)
        loc = gl.glGetUniformLocation(self.program.program_id, "view")
        gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, v)

#        p = perspective(4.0, -4.0, 4.0, -4.0, 4.0, -4.0)
        p = perspective_fov(4.0, -4.0, 2.0, 16.0 / 9.0)
        loc = gl.glGetUniformLocation(self.program.program_id, "projection")
        gl.glUniformMatrix4fv(loc, 1, gl.GL_FALSE, p)

    def create_program(self):
        if not self.vertex_shader_code:
            raise NoVertexShaderCodeError("No vertex shader defined for instance of class Graphics")
        if not self.fragment_shader_code:
            raise NoFragmentShaderCodeError("No fragment shader defined for instance of class Graphics")
        self.vertex_shader = Shader(ShaderType.VERTEX)
        self.vertex_shader.set_shader_source(self.vertex_shader_code)
        self.vertex_shader.compile()

        self.fragment_shader = Shader(ShaderType.FRAGMENT)
        self.fragment_shader.set_shader_source(self.fragment_shader_code)
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
    g.vertex_shader_code = vertex_shader_code
    g.fragment_shader_code = fragment_shader_code
    g.init_graphics()
    data, indices = load_data()
    g.create_program()
    g.set_data(data, indices)
    g.start()
