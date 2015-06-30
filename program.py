import OpenGL.GL as gl


class Program(object):

    def __init__(self):
        self.program_id = gl.glCreateProgram()

    def attach_shader(self, shader):
        gl.glAttachShader(self.program_id, shader.shader_id)

    def link(self):
        gl.glLinkProgram(self.program_id)

    def use(self):
        gl.glUseProgram(self.program_id)
