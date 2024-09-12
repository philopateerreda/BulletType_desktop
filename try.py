import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QApplication, \
    QStackedWidget, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

IMAGE_DIR = "C:\\Users\\ASUS\\Desktop\\VS\\.vscode\\python V1\\photos"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Achievements")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #ff007f;")
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Create a widget for the buttons with a common background color
        button_widget = QWidget()
        button_widget.setStyleSheet("background-color: #002366; border-radius: 20px;")
        button_layout = QVBoxLayout(button_widget)

        button1 = QPushButton("King of battles")
        button2 = QPushButton("Endurance")
        button3 = QPushButton("Winning")

        for button in [button1, button2, button3]:
            button.setStyleSheet("font-size: 30px; color: white; padding: 5px; margin: 5px;")
            button_layout.addWidget(button)

        # Create a stacked widget to switch between different achievements
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_achievement_widget("King of battles", [("Complete 10 battles", 30),
                                                                                         ("Complete 20 battles", 50)]))
        self.stacked_widget.addWidget(
            self.create_achievement_widget("Endurance", [("Complete 5 battles", 20), ("Complete 20 battles", 50)]))
        self.stacked_widget.addWidget(
            self.create_achievement_widget("Winning", [("Complete 100 battles", 100), ("Complete 20 battles", 50)]))

        # Connect buttons to switch between widgets
        button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        button3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # Add the button layout and stacked widget to the main layout
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.stacked_widget)

        # Set the layout of the main widget
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_achievement_widget(self, title, achievements):
        widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #002366;")
        layout.addWidget(title_label)

        for achievement, reward in achievements:
            achievement_layout = QHBoxLayout()

            achievement_label = QLabel(achievement)
            achievement_label.setStyleSheet(
                "font-size: 30px; color: #002366; background-color: #E0E0E0; padding: 5px; border-radius: 15px;")

            achievement_layout.addWidget(achievement_label)
            layout.addLayout(achievement_layout)

        widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollArea > QWidget > QWidget { border: none; }
            QWidget { border-radius: 20px; }
        """)
        return scroll


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
