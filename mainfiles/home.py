import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics
from PyQt5.QtCore import Qt

# Define the base path for images
IMAGE_DIR = "F:\\vs_folder\\python_V1_6\\photos"

class CustomLabel(QLabel):
    def __init__(self, text, parent=None, page_name=None):
        super().__init__(text, parent)
        self.page_name = page_name
        self.default_color = "white"
        self.hover_color = "#1E3A95"
        self.setStyleSheet(f"color: {self.default_color};")
        self.setFont(QFont('aladin', 40))  # Font size is set here

    def enterEvent(self, event):
        self.setStyleSheet(f"color: {self.hover_color};")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"color: {self.default_color};")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.page_name:
            self.parent().navigate_to(page_name=self.page_name)
        super().mousePressEvent(event)

class Home(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(0, 0, 1920, 1080)  # Set the size and position of the window

        # Set the background image
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(os.path.join(IMAGE_DIR, "ba.jpg")).scaled(1920, 1080, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, 1920, 1080)  # Absolute position and size of the label

        # Create the middle photo
        self.create_center_image()

        # Create navigation links
        self.create_links()

        # Create and position the battle button
        self.battle_button = QPushButton("Go to Battle", self)
        self.battle_button.setGeometry(50, 290, 400, 100)  # Set position and size of the button
        self.battle_button.clicked.connect(self.go_battle)
        self.battle_button.setStyleSheet(
            "font-size:30px; color:#1E3A95; background-color: white;"
            "border-radius: 50px; border: 2px solid #1E3A95;"
        )
        self.battle_button.show()  # Make sure the button is shown

        # Create and position the stats button
        self.stats_button = QPushButton("Go to Stats", self)
        self.stats_button.setGeometry(50, 430, 400, 100)  # Set position and size of the button
        self.stats_button.clicked.connect(self.go_stats)
        self.stats_button.setStyleSheet(
            "font-size:30px; color:#1E3A95; background-color: white;"
            "border-radius: 50px; border: 2px solid #1E3A95;"
        )
        self.stats_button.show()  # Make sure the button is shown

        # Create the advertisement widget
        self.create_advertisement()

        # Create the daily challenges widget
        self.create_daily_challenges()

    def create_links(self):
        links = [("Home", "home"), ("Achievements", "achievements"), ("Shop", "shop"), 
                 ("Inventory", "inventory"), ("League", "league"), ("Seseon", "seseon")]

        y_position = 40
        x_position = 50
        spacing = 33
        font_size = 40

        # Create font
        font = QFont('aladin', font_size)
        font_metrics = QFontMetrics(font)

        for text, page_name in links:
            text_width = font_metrics.horizontalAdvance(text)
            link = CustomLabel(text, self, page_name)
            link.setGeometry(x_position, y_position, text_width, 50)
            link.setFont(font)
            link.show()

            # Update x_position for the next link
            x_position += text_width + spacing

        # Create and add the number label for the coins
        self.coin_number_label = QLabel("30", self)
        self.coin_number_label.setFont(QFont('aladin', 30))
        self.coin_number_label.setStyleSheet("color: white;")
        self.coin_number_label.setGeometry(1670, 42, 50, 50)  # Adjust position and size as needed
        self.coin_number_label.setAlignment(Qt.AlignCenter)
        self.coin_number_label.show()

        # Create and add the coin image label
        self.coin_image_label = QLabel(self)
        coin_image_path = os.path.join(IMAGE_DIR, "coin.png")  # Change to the path of your coin image
        coin_pixmap = QPixmap(coin_image_path)
        if coin_pixmap.isNull():
            print(f"Failed to load coin image from {coin_image_path}")
        scaled_coin_pixmap = coin_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the size as needed
        self.coin_image_label.setPixmap(scaled_coin_pixmap)

        # Position the coin image label in the top right corner
        self.coin_image_label.setGeometry(1800 - scaled_coin_pixmap.width(), 30, scaled_coin_pixmap.width(), scaled_coin_pixmap.height())
        self.coin_image_label.show()

        # Create and add the profile picture label
        self.profile_picture_label = QLabel(self)
        profile_picture_path = os.path.join(IMAGE_DIR, "home.png")  # Change to the path of your profile picture
        pixmap = QPixmap(profile_picture_path)
        if pixmap.isNull():
            print(f"Failed to load profile picture from {profile_picture_path}")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the size as needed
        self.profile_picture_label.setPixmap(scaled_pixmap)

        # Position the profile picture label in the top right corner
        self.profile_picture_label.setGeometry(1870 - scaled_pixmap.width(), 10, scaled_pixmap.width(), scaled_pixmap.height())
        self.profile_picture_label.show()

    def create_center_image(self):
        self.center_image_label = QLabel(self)
        center_image_path = os.path.join(IMAGE_DIR, "ch1.png")  # Change to the path of your image
        pixmap = QPixmap(center_image_path)
        if pixmap.isNull():
            print(f"Failed to load center image from {center_image_path}")
        scaled_pixmap = pixmap.scaled(1200, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Larger size
        self.center_image_label.setPixmap(scaled_pixmap)

        # Calculate the center position
        center_x = (1920 - scaled_pixmap.width()) // 2
        center_y = (1080 - scaled_pixmap.height()) // 3

        self.center_image_label.setGeometry(center_x, center_y, scaled_pixmap.width(), scaled_pixmap.height())
        self.center_image_label.setAlignment(Qt.AlignCenter)
        self.center_image_label.show()

    def create_advertisement(self):
        self.advertisement_widget = QWidget(self)
        self.advertisement_widget.setGeometry(1400, 250, 500, 230)  # Adjusted position and size
        self.advertisement_widget.setStyleSheet(
            "background-color: white; color: #1E3A95; padding: 10px;"
            "border-radius: 20px; border: 2px solid #1E3A95;"
        )

        advertisement_layout = QVBoxLayout(self.advertisement_widget)

        # Create and add the "Advertisement" label
        advertisement_label = QLabel("Advertisement", self.advertisement_widget)
        advertisement_label.setFont(QFont('aladin', 45))  # Increased font size for the header
        advertisement_label.setAlignment(Qt.AlignCenter)  # Center align the text
        advertisement_layout.addWidget(advertisement_label)

    def create_daily_challenges(self):
        self.daily_challenges_widget = QWidget(self)
        self.daily_challenges_widget.setGeometry(1400, 530, 500, 350)  # Adjusted position and size
        self.daily_challenges_widget.setStyleSheet(
            "background-color: white; color: #1E3A95; padding: 10px;"
            "border-radius: 20px; border: 2px solid #1E3A95;"
        )

        self.daily_challenges_layout = QVBoxLayout(self.daily_challenges_widget)

        # Create and add the "Daily Challenges:" label
        daily_challenges_label = QLabel("Daily Challenges:", self.daily_challenges_widget)
        daily_challenges_label.setFont(QFont('aladin', 40))  # Increased font size for the header
        self.daily_challenges_layout.addWidget(daily_challenges_label)

        # Add space for challenges
        challenges = ["Challenge 1: Register for the first time", "Challenge 2: Win your first battle", "Challenge 3: Get an 80% accuracy"]
        for challenge in challenges:
            challenge_label = QLabel(challenge, self.daily_challenges_widget)
            challenge_label.setFont(QFont('aladin', 20))  # Increased font size for challenges
            self.daily_challenges_layout.addWidget(challenge_label)

    def navigate_to(self, page_name):
        self.main_window.navigate_to(page_name)

    def go_battle(self):
        self.main_window.navigate_to("battle")

    def go_register(self):
        self.main_window.navigate_to("register")

    def go_stats(self):
        self.main_window.navigate_to("stats")
