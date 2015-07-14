import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import sys
import ctypes
from program import Program
from shader import Shader, ShaderType
from shader_codes import vertex_shader_code, fragment_shader_code
from data import load_data, load_cube


def translate(v):
    t = np.eye(4, 4, dtype=np.float32)
    t[0:3, 3] = v
    return t


def rotate_x(angle):
    r = np.eye(4, 4, dtype=np.float32)
    c = np.cos(angle)
    s = np.sin(angle)
    r[0, 0] = 1.0
    r[1, 1] = c
    r[1, 2] = -s
    r[2, 1] = s
    r[2, 2] = c
    r[3, 3] = 1.0
    return r

def rotate_y(angle):
    r = np.eye(4, 4, dtype=np.float32)
    c = np.cos(angle)
    s = np.sin(angle)
    r[0, 0] = c
    r[0, 2] = s
    r[2, 0] = -s
    r[2, 2] = c
    r[1, 1] = 1.0
    r[3, 3] = 1.0
    return r

def rotate_z(angle):
    r = np.eye(4, 4, dtype=np.float32)
    c = np.cos(angle)
    s = np.sin(angle)
    r[0, 0] = c
    r[0, 1] = -s
    r[1, 0] = s
    r[1, 1] = c
    r[2, 2] = 1.0
    r[3, 3] = 1.0
    return r


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


def perspective_fov(angle, aspect, near, far):
    p = np.zeros((4, 4), dtype=np.float32)
    f = 1.0 / np.tan(angle / 2)
    p[0, 0] = f / aspect
    p[1, 1] = f
    p[2, 2] = - (far + near) / (near - far)
    p[2, 3] = 2 * near * far / (near - far)
    p[3, 2] = -1
    return p


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
        self.position = np.zeros((3), dtype=np.float32)
        self._mouse_x = 0
        self._mouse_y = 0
        self.angle_x = 0
        self.angle_y = 0
        self.velocity = 0.1
        self.angle_velocity = 0.02

    def init_graphics(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
        glut.glutCreateWindow(self.window_title)
        glut.glutReshapeWindow(self.window_width, self.window_height)
        glut.glutReshapeFunc(self.reshape)
        glut.glutDisplayFunc(self.display)
        glut.glutKeyboardFunc(self.keyboard)
        glut.glutMouseFunc(self.mouse)
        glut.glutPassiveMotionFunc(self.mouse_move)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def display(self):
        #m = translate(np.array([0.0, 0.0, 0.0], dtype=np.float32))
        T = translate(np.array([0.0, 0.0, -5.0], dtype=np.float32))
        M = np.array(np.matrix(T))
        # m = t
        # loc = gl.glGetUniformLocation(self.program.program_id, "model")
        # gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, M)

        V = np.eye(4, 4, dtype=np.float32)
        #r = rotate_y(angle)
        P_pos = translate(self.position)
        V_R_y = rotate_y(self.angle_y)
        V = np.array(np.matrix(V_R_y) * np.matrix(P_pos))
        # loc = gl.glGetUniformLocation(self.program.program_id, "view")
        # gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, V)
        x = 0.5
        aspect = 1.0 * self.window_width / self.window_height
        P = perspective(1.0, 10.0, x, - x, x / aspect, - x / aspect)
        #P = perspective_fov(np.pi / 10, 16.0 / 10.0, 1.0, 20.0)
        PVM = np.array(np.matrix(P) * np.matrix(V) * np.matrix(M))
        loc = gl.glGetUniformLocation(self.program.program_id, "pvm")
        gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, PVM)


        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        gl.glDrawElements(gl.GL_TRIANGLES, self.indices.size, gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
        glut.glutSwapBuffers()

    def keyboard(self, key, x, y):
        if key == "\033":
            sys.exit()
        elif key == "w":
            self.position[2] += self.velocity
            # position[2] -= np.cos(angle) * velocity
            # position[0] -= np.sin(angle) * velocity
        elif key == "s":
            self.position[2] -= self.velocity
            # position[2] += np.cos(angle) * velocity
            # position[0] += np.sin(angle) * velocity
        glut.glutPostRedisplay()

    def mouse(self, button, state, x, y):
        print(button, state, x, y)

    def mouse_move(self, x, y):
        self.angle_y += -self.angle_velocity * (1.0 * (x) / self.window_width - 0.5)
        self.angle_x += -self.angle_velocity * (1.0 * (y) / self.window_height - 0.5)
        self._mouse_x = x
        self._mouse_y = y
        glut.glutPostRedisplay()

    def reshape(self, width, height):
        gl.glViewport(0, 0, width, height)

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

        #p = perspective(2.0, 10.0, 6.0, -6.0, 4.0, -4.0)
        #p = perspective_fov(2.0, 16.0 / 9.0, -2.0, -10.0)
        # glu.gluPerspective(2.0, 16.0 / 9.0, -2.0, -10.0)
        # loc = gl.glGetUniformLocation(self.program.program_id, "projection")
        # gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, p)

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
    graphics = Graphics()
    graphics.vertex_shader_code = vertex_shader_code
    graphics.fragment_shader_code = fragment_shader_code
    graphics.init_graphics()
    data, indices = load_cube()
    graphics.create_program()
    graphics.set_data(data, indices)
    graphics.start()
