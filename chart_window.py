import torch
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QTimer

from dql_agent import DQLAgent
from environment import Environment

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bar Chart Example")
        self.setGeometry(100, 100, 500, 1080)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.reward_chart = self.create_reward_chart()
        reward_chart_view = QChartView(self.reward_chart)
        reward_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(reward_chart_view)

        self.distance_chart = self.create_distance_chart()
        distance_chart_view = QChartView(self.distance_chart)
        distance_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(distance_chart_view)

        self.action_chart = self.create_action_chart()
        action_chart_view = QChartView(self.action_chart)
        action_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(action_chart_view)

        self.button = QPushButton("Save Model")
        self.button.clicked.connect(self.save_button_clicked)
        layout.addWidget(self.button)

        self.environment = Environment(False, self)
        layout.addWidget(self.environment)

        self.timer = QTimer(self)
        # self.test()
        self.train()

    def test(self):
        self.agent = DQLAgent(self.environment, "model/model24.pt")
        self.state = self.environment.reset()
        self.time = 0
        self.total_reward = 0
        self.episode = 0
        self.timer.timeout.connect(self.loop_function_for_test)
        self.timer.start(1000 // 60)  # 60 FPS için

    def loop_function_for_test(self):
        self.update_distance_chart(self.state)

        # select an action
        action, output_percentages = self.agent.act(self.state)
        self.update_action_chart(output_percentages)

        # step
        next_state, reward, done = self.environment.update(action)

        self.total_reward += reward

        # update state
        self.state = next_state
        self.environment.handle_events()

        self.time += 1
        if done:
            print("Episode: {}, time: {}, reward: {}".format(self.episode, self.time, self.total_reward))
            self.update_reward_chart((self.episode, self.total_reward))
            self.state = self.environment.reset()
            self.time = 0
            self.total_reward = 0
            self.episode += 1

    def train(self):
        self.agent = DQLAgent(self.environment)
        self.state = self.environment.reset()
        self.time = 0
        self.total_reward = 0
        self.episode = 0
        self.timer.timeout.connect(self.loop_function_for_train)
        self.timer.start(1000 // 60)  # 60 FPS için

    def loop_function_for_train(self):
        batch_size = 16
        self.update_distance_chart(self.state)

        # select an action
        action, output_percentages = self.agent.act(self.state)
        self.update_action_chart(output_percentages)

        # step
        next_state, reward, done = self.environment.update(action)

        self.total_reward += reward

        # remember / storage
        self.agent.remember(self.state, action, reward, next_state, done)

        # update state
        self.state = next_state

        # replay
        self.agent.replay(batch_size)

        # adjust epsilon
        self.agent.adaptiveEGreedy()

        self.environment.handle_events()
        self.time += 1

        if done:
            print("Episode: {}, time: {}, reward: {}".format(self.episode, self.time, self.total_reward))
            self.update_reward_chart((self.episode, self.total_reward))
            self.state = self.environment.reset()
            self.time = 0
            self.total_reward = 0
            self.episode += 1
    def create_distance_chart(self):
        self.barset = QBarSet("Data")

        # Örnek verileri ekle
        self.barset.append([1, 1, 1, 1, 1])

        series = QBarSeries()
        series.append(self.barset)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Sensor Distance")
        chart.legend().setVisible(False)

        axisX = QBarCategoryAxis()
        axisX.append(["Left", "L_Cross", "Front", "R_Cross", "Right"])
        axisX.setLabelsAngle(-90)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        return chart

    def create_action_chart(self):
        self.action_barset = QBarSet("Data")

        # Örnek verileri ekle
        self.action_barset.append([100, 100, 100])

        series = QBarSeries()
        series.append(self.action_barset)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Actions")
        chart.legend().setVisible(False)

        axisX = QBarCategoryAxis()
        axisX.append(["Left", "Straight", "Right"])
        axisX.setLabelsAngle(-90)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        return chart

    def create_reward_chart(self):
        self.series = QLineSeries()

        chart = QChart()
        chart.addSeries(self.series)
        chart.createDefaultAxes()
        chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)

        # X ekseni için bir QValueAxis oluştur ve isim ver
        axisX = QValueAxis()
        axisX.setTitleText("Episode")
        chart.setAxisX(axisX, self.series)

        # Y ekseni için bir QValueAxis oluştur ve isim ver
        axisY = QValueAxis()
        axisY.setTitleText("Reward")
        chart.setAxisY(axisY, self.series)

        return chart

    def update_distance_chart(self, data):
        self.barset.remove(0, len(self.barset))  # Remove all existing values
        self.barset.append(data)  # Add new random values
        pass

    def update_action_chart(self, data):
        if sum(data) != 0:
            self.action_barset.remove(0, len(self.action_barset))
            self.action_barset.append(data)

    def update_reward_chart(self, data):
        x, y = data
        self.series.append(x, y)
        x_values = [point.x() for point in self.series.points()]
        y_values = [point.y() for point in self.series.points()]

        if x_values and y_values:
            self.reward_chart.axisX().setRange(0, max(x_values))
            self.reward_chart.axisY().setRange(min(y_values), max(y_values))

    def save_button_clicked(self):
        torch.save(self.agent.model.state_dict(), "model/model" + str(self.episode) + ".pt")