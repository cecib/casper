import sys
import glm
import numpy as np
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


vertex_shader = """
#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""

fragment_shader = """
#version 330 core
out vec4 fragColor;
void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


class Ray():
    def __init__(self, x1_y1, x2_y2):
        self._x1, self._y1 = x1_y1
        self._x2, self._y2 = x2_y2


class GLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.shader = None
        self.vertices = None
        self.vao = None
        self.vbo = None

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        try:
            self.shader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            )
        except Exception as e:
            print(f"Error compiling shaders: {e}")

        self.setupCube()

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

        # use shader program
        glUseProgram(self.shader)

        # set transform matrices
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'projection'), 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'model'), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader, 'view'), 1, GL_FALSE, glm.value_ptr(view))

        # draw cube
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices) // 3)
        glBindVertexArray(0)

    def setupCube(self):
        """Set up cube and bind buffers."""
        self.vertices = np.array([
            # front face
            -0.5, -0.5,  0.5,   0.5, -0.5,  0.5,   0.5,  0.5,  0.5,
            -0.5, -0.5,  0.5,   0.5,  0.5,  0.5,  -0.5,  0.5,  0.5,
            # back face
            -0.5, -0.5, -0.5,  -0.5,  0.5, -0.5,   0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,   0.5,  0.5, -0.5,   0.5, -0.5, -0.5,
            # left face
            -0.5, -0.5, -0.5,  -0.5, -0.5,  0.5,  -0.5,  0.5,  0.5,
            -0.5, -0.5, -0.5,  -0.5,  0.5,  0.5,  -0.5,  0.5, -0.5,
            # right face
            0.5, -0.5, -0.5,   0.5,  0.5, -0.5,   0.5,  0.5,  0.5,
            0.5, -0.5, -0.5,   0.5,  0.5,  0.5,   0.5, -0.5,  0.5,
            # top face
            -0.5,  0.5, -0.5,   0.5,  0.5, -0.5,   0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,   0.5,  0.5,  0.5,  -0.5,  0.5,  0.5,
            # bottom face
            -0.5, -0.5, -0.5,  -0.5, -0.5,  0.5,   0.5, -0.5,  0.5,
            -0.5, -0.5, -0.5,   0.5, -0.5,  0.5,   0.5, -0.5, -0.5
        ], dtype=np.float32)

        # create buffer
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              3 * self.vertices.itemsize, None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # unbind VAO
        glBindVertexArray(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Casper Render')

        layout = QVBoxLayout()
        gl_widget = GLWidget()
        layout.addWidget(gl_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    format = QSurfaceFormat()
    format.setVersion(3, 3)  # set OpenGL version
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
