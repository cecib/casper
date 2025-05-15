import sys
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from render import GLWidget

gl_format = QSurfaceFormat()
gl_format.setVersion(3, 3)  # set OpenGL version
gl_format.setProfile(QSurfaceFormat.CoreProfile)
QSurfaceFormat.setDefaultFormat(gl_format)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('casper render')
        layout = QVBoxLayout()
        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.last_mouse_pos = None

    def mousePressEvent(self, event):
        self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        # TODO: use last mouse pos for rotation dir
        self.last_mouse_pos = event.position()
        dx = event.position().x()
        dy = event.position().y()
        self.gl_widget.update_rotation(dx, dy)

    def closeEvent(self, event):
        self.gl_widget.cleanup()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
