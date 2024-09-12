import os
import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont, QPixmap, QFontMetrics
from PyQt5.QtCore import Qt

# Define the image directory
IMAGE_DIR = "F:\\vs_folder\\python_V1_6\\photos"

class CustomLabel(QLabel):
    def __init__(self, text, parent=None, page_name=None):
        super().__init__(text, parent)
        self.page_name = page_name
        self.default_color = "white"
        self.hover_color = "#1E3A95"
        self.setStyleSheet(f"color: {self.default_color}; background: transparent;")
        self.setFont(QFont('aladin', 40))  # Font size is set here

    def enterEvent(self, event):
        self.setStyleSheet(f"color: {self.hover_color}; background: transparent;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"color: {self.default_color}; background: transparent;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.page_name:
            self.parent().navigate_to(page_name=self.page_name)
        super().mousePressEvent(event)

class Stats(QWidget):
    def __init__(self, main_window, db, user_id):
        super().__init__()
        self.main_window = main_window
        self.db = db
        self.user_id = user_id

        # Set up the widget
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #2E2E2E;")

        # Set background image
        self.set_background_image(os.path.join(IMAGE_DIR, "ba.jpg"))

        # Initialize UI elements
        self.init_ui()

    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Unable to load image at {image_path}")
            return

        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap.scaled(1920, 1080, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, 1920, 1080)
        self.background_label.setScaledContents(True)

    def init_ui(self):
        font = QFont()
        font.setPointSize(60)

        self.typing_speed_label = QLabel("Average Typing Speed: -- wpm", self)
        self.typing_speed_label.setFont(font)
        self.typing_speed_label.setStyleSheet("color: white; background: transparent;")
        self.typing_speed_label.setGeometry(50, 150, 1000, 80)

        self.accuracy_label = QLabel("Average Accuracy: --%", self)
        self.accuracy_label.setFont(font)
        self.accuracy_label.setStyleSheet("color: white; background: transparent;")
        self.accuracy_label.setGeometry(50, 250, 1000, 80)

        self.matches_label = QLabel("Number of Matches Played: --", self)
        self.matches_label.setFont(font)
        self.matches_label.setStyleSheet("color: white; background: transparent;")
        self.matches_label.setGeometry(50, 350, 1000, 80)

        self.create_links()

    def load_statistics(self):
        try:
            cursor = self.db.conn.cursor()

            # Get average typing speed for the current user
            cursor.execute('''
                SELECT AVG(speed) FROM matches WHERE user_id = ?
            ''', (self.user_id,))
            avg_speed = cursor.fetchone()[0] or 0

            # Get average accuracy for the current user
            cursor.execute('''
                SELECT AVG(accuracy) FROM matches WHERE user_id = ?
            ''', (self.user_id,))
            avg_accuracy = cursor.fetchone()[0] or 0

            # Get the number of matches played by the current user
            cursor.execute('''
                SELECT COUNT(*) FROM matches WHERE user_id = ?
            ''', (self.user_id,))
            num_matches = cursor.fetchone()[0]

            # Update labels with the retrieved data
            self.typing_speed_label.setText(f'Average Typing Speed: {avg_speed:.2f} wpm')
            self.accuracy_label.setText(f'Average Accuracy: {avg_accuracy:.2f}%')
            self.matches_label.setText(f'Number of Matches Played: {num_matches}')
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def create_links(self):
        links = [("Home", "home"), ("Achievements", "achievements"), ("Shop", "shop"), 
                 ("Inventory", "inventory"), ("League", "league"), ("Season", "season")]

        y_position = 40
        x_position = 50
        spacing = 50

        font = QFont('aladin', 40)
        font_metrics = QFontMetrics(font)

        for text, page_name in links:
            text_width = font_metrics.horizontalAdvance(text)
            link = CustomLabel(text, self, page_name)
            link.setGeometry(x_position, y_position, text_width, 50)
            link.setFont(font)
            link.show()

            x_position += text_width + spacing

    def navigate_to(self, page_name):
        self.main_window.navigate_to(page_name)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_statistics()
