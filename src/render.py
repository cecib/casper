import os
import glm
import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from PIL import Image


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def check_gl_errors():
    gl_error = glGetError()
    if gl_error != GL_NO_ERROR:
        print(f"OpenGL Error: {gl_error}")


class GLWidget(QOpenGLWidget):

    WIDTH, HEIGHT = 560, 560
    SHELL_NUM = 40
    SHELL_OFFSET = 0.005

    def __init__(self):
        super().__init__()
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.timer = QTimer(self)
        self.shader = None
        self.vertices = None
        self.vao = None
        self.vbo = None
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.texture_ids = []

    def load_texture(self, path, num_textures):
        if not os.path.exists(path):
            print(f"File does not exist {path}. Skipping texture.")
            return

        image = Image.open(path)
        image = image.convert('RGBA')
        image_data = np.array(image)

        tex = glGenTextures(1)
        self.texture_ids.append(tex)
        glActiveTexture(GL_TEXTURE0 + num_textures)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return tex

    def initializeGL(self):
        glClearColor(1., .6, 1., 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)

        # glDisable(GL_CULL_FACE)

        self.setup_cube()

        try:
            # compile shaders
            vertex_shader_id = compileShader(
                read_file('vertex_shader.glsl'), GL_VERTEX_SHADER)
            vertex_shader_status = glGetShaderiv(
                vertex_shader_id, GL_COMPILE_STATUS)
            print(
                f"Vertex shader compilation status: {vertex_shader_status}")

            fragment_shader_id = compileShader(
                read_file('fragment_shader.glsl'), GL_FRAGMENT_SHADER)
            fragment_shader_status = glGetShaderiv(
                fragment_shader_id, GL_COMPILE_STATUS)
            print(
                f"Fragment shader compilation status: {fragment_shader_status}")

            self.shader = compileProgram(vertex_shader_id, fragment_shader_id)

        except Exception as e:
            print(f"Error compiling shaders: {e}")

        # load textures
        self.load_texture("./images/seamless_cow.jpg", 0)
        self.load_texture("./images/fur_texture.png", 1)

        self.timer.timeout.connect(self.update)  # trigger paintGL
        self.timer.start(16)  # ~60 FPS



    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # projection matrix
        projection = glm.perspective(glm.radians(45.0), 1.0, 0.1, 100.0)

        # view matrix
        eye = glm.vec3(0.0, 0.0, 4.0)
        center = glm.vec3(0.0, 0.0, 0.0)
        up = glm.vec3(0.0, 1.0, 0.0)
        view = glm.lookAt(eye, center, up)

        # transform model matrix
        model = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(
            self.rotation_x % 360), glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, glm.radians(
            self.rotation_y % 360), glm.vec3(0.0, 1.0, 0.0))

        # use shader program
        glUseProgram(self.shader)

        # send transforms to shader
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'projection'), 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'model'), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'view'), 1, GL_FALSE, glm.value_ptr(view))

        glUniform1i(glGetUniformLocation(self.shader, "shellIndex"), 0)
        glUniform1f(glGetUniformLocation(self.shader, "shellOffset"), self.SHELL_OFFSET)

        # send texture to shader
        glUniform1i(glGetUniformLocation(self.shader, 'textureSampler'), 0)
        glUniform1i(glGetUniformLocation(self.shader, 'furTexture'), 1)
        glUniform1f(glGetUniformLocation(self.shader, "alpha"), 1.0)

        # draw cube
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
        glBindVertexArray(0)
        check_gl_errors()

        for shell in range(self.SHELL_NUM):
            glUniform1i(glGetUniformLocation(self.shader, "shellIndex"), shell)
            glUniform1i(glGetUniformLocation(self.shader, "numShells"), self.SHELL_NUM)
            glUniform1f(glGetUniformLocation(self.shader, "shellOffset"), self.SHELL_OFFSET)
            glUniform1f(glGetUniformLocation(self.shader, "alpha"), 1.0 - shell / self.SHELL_NUM)

            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
            glBindVertexArray(0)
            check_gl_errors()


    def setup_cube(self):
        """Set up cube and bind buffers."""
        self.vertices = np.array([
            # right face (+x)
            [0.5, -0.5, 0.5, 1, 0, 0, 1.0, 0.0],
            [0.5, -0.5, -0.5, 1, 0, 0, 0.0, 0.0],
            [0.5, 0.5, -0.5, 1, 0, 0, 0.0, 1.0],
            [0.5, -0.5, 0.5, 1, 0, 0, 1.0, 0.0],
            [0.5, 0.5, -0.5, 1, 0, 0, 0.0, 1.0],
            [0.5, 0.5, 0.5, 1, 0, 0, 1.0, 1.0],

            # left face (-x)
            [-0.5, -0.5, -0.5, -1, 0, 0, 1.0, 0.0],
            [-0.5, -0.5, 0.5, -1, 0, 0, 0.0, 0.0],
            [-0.5, 0.5, 0.5, -1, 0, 0, 0.0, 1.0],
            [-0.5, -0.5, -0.5, -1, 0, 0, 1.0, 0.0],
            [-0.5, 0.5, 0.5, -1, 0, 0, 0.0, 1.0],
            [-0.5, 0.5, -0.5, -1, 0, 0, 1.0, 1.0],

            # top face (+y)
            [-0.5, 0.5, 0.5, 0, 1, 0, 0.0, 1.0],
            [0.5, 0.5, 0.5, 0, 1, 0, 1.0, 1.0],
            [0.5, 0.5, -0.5, 0, 1, 0, 1.0, 0.0],
            [-0.5, 0.5, 0.5, 0, 1, 0, 0.0, 1.0],
            [0.5, 0.5, -0.5, 0, 1, 0, 1.0, 0.0],
            [-0.5, 0.5, -0.5, 0, 1, 0, 0.0, 0.0],

            # bottom face (-y)
            [-0.5, -0.5, -0.5, 0, -1, 0, 0.0, 1.0],
            [0.5, -0.5, -0.5, 0, -1, 0, 1.0, 1.0],
            [0.5, -0.5, 0.5, 0, -1, 0, 1.0, 0.0],
            [-0.5, -0.5, -0.5, 0, -1, 0, 0.0, 1.0],
            [0.5, -0.5, 0.5, 0, -1, 0, 1.0, 0.0],
            [-0.5, -0.5, 0.5, 0, -1, 0, 0.0, 0.0],

            # front face (+z)
            [-0.5, -0.5, 0.5, 0, 0, 1, 0.0, 0.0],
            [0.5, -0.5, 0.5, 0, 0, 1, 1.0, 0.0],
            [0.5, 0.5, 0.5, 0, 0, 1, 1.0, 1.0],
            [-0.5, -0.5, 0.5, 0, 0, 1, 0.0, 0.0],
            [0.5, 0.5, 0.5, 0, 0, 1, 1.0, 1.0],
            [-0.5, 0.5, 0.5, 0, 0, 1, 0.0, 1.0],

            # back face (-z)
            [0.5, -0.5, -0.5, 0, 0, -1, 0.0, 0.0],
            [-0.5, -0.5, -0.5, 0, 0, -1, 1.0, 0.0],
            [-0.5, 0.5, -0.5, 0, 0, -1, 1.0, 1.0],
            [0.5, -0.5, -0.5, 0, 0, -1, 0.0, 0.0],
            [-0.5, 0.5, -0.5, 0, 0, -1, 1.0, 1.0],
            [0.5, 0.5, -0.5, 0, 0, -1, 0.0, 1.0],
        ], dtype=np.float32)

        # create buffer
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)

        len_vertex = 8 * self.vertices.itemsize

        # positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              len_vertex, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, len_vertex, ctypes.c_void_p(
            3 * self.vertices.itemsize))
        glEnableVertexAttribArray(1)

        # uvs
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, len_vertex, ctypes.c_void_p(
            6 * self.vertices.itemsize))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)  # unbind VAO

    def update_rotation(self, dx, dy):
        self.rotation_x = dy + self.HEIGHT//2
        self.rotation_y = -dx - self.WIDTH//2

    def cleanup(self):
        for texture_id in self.texture_ids:
            glDeleteTextures(1, texture_id)
        pass