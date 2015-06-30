import OpenGL.GL as gl


class ShaderError(Exception):
    pass


class WrongShaderTypeError(ShaderError):
    pass


class ShaderType(object):
    VERTEX = 0
    FRAGMENT = 1 


class Shader(object):

    def __init__(self, shader_type):
        self.shader_type = shader_type
        if self.shader_type == ShaderType.VERTEX:
            self.shader_id = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        elif self.shader_type == ShaderType.FRAGMENT:
            self.shader_id = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        else:
            raise WrongShaderTypeError()
            
    def set_shader_source(self, source):
        gl.glShaderSource(self.shader_id, source)

    def compile(self):
        gl.glCompileShader(self.shader_id)
