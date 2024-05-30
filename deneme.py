import sys
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QTimer, pyqtSignal, QObject


class PygameWidget(QWidget):
    my_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)

        # pygame ekranını oluştur
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Pygame in PyQt")

        # pygame için zamanlayıcı oluştur
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(1000 // 60)  # 60 FPS için
        self.radius = 10



    def update_pygame(self):
        # Ekranı temizle
        self.screen.fill((0, 0, 0))

        # Buraya pygame çizim kodlarınızı ekleyin
        pygame.draw.circle(self.screen, (255, 0, 0), (200, 150), self.radius)

        if(self.radius % 10 == 0):
            self.my_signal.emit()

        # Ekranı güncelle
        pygame.display.flip()

    def increase_circle(self):
        self.radius += 1

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt with Pygame")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button = QPushButton("Add Random Point")
        self.button.clicked.connect(self.button_clicked)
        layout.addWidget(self.button)

        # PygameWidget'i oluştur
        self.pygame_widget = PygameWidget(self)
        layout.addWidget(self.pygame_widget)

        self.pygame_widget.my_signal.connect(self.my_slot)

    def button_clicked(self):
        self.pygame_widget.radius += 1

    def my_slot(self):
        print("signal")

if __name__ == "__main__":
    pygame.init()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
