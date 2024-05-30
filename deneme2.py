import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtGui import QPainter


class BarChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Bar Chart Example")
        self.setGeometry(100, 100, 800, 600)

        self.chart = QChart()
        self.series = QBarSeries()

        self.set0 = QBarSet("Set 1")
        self.update_data()

        self.series.append(self.set0)
        self.chart.addSeries(self.series)
        self.chart.setTitle("Random Bar Chart Example")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setAnimationOptions(QChart.NoAnimation)

        categories = ["A", "B", "C", "D", "E"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(axisX, self.series)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.button = QPushButton("Update Data")
        self.button.clicked.connect(self.update_data)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart_view)
        self.layout.addWidget(self.button)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def update_data(self):
        random_data = [random.randint(1, 10) for _ in range(5)]
        self.set0.remove(0, len(self.set0))  # Remove all existing values
        self.set0.append(random_data)  # Add new random values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarChartWindow()
    window.show()
    sys.exit(app.exec_())
