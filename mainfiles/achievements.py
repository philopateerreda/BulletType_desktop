import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics
from PyQt5.QtCore import Qt

class Achievements(QWidget):
    IMAGE_DIR = "F:\\vs_folder\\python_V1_6\\photos"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setGeometry(0, 0, 1920, 1080)

        # Create background
        self.background = QLabel(self)
        self.set_background_image("ba.jpg")
        self.background.setGeometry(0, 0, 1920, 1080)

        # Create navigation links
        self.create_links()

        # Create the achievements UI
        self.init_achievements_ui()

        # Variable to track the current active button
        self.current_active_button = None

        # Set the first button as active by default
        self.buttons[0].click()



        
        # Create and add the number label for the coins
        self.coin_number_label = QLabel("30", self)
        self.coin_number_label.setFont(QFont('aladin', 30))
        self.coin_number_label.setStyleSheet("color: white;")
        self.coin_number_label.setGeometry(1670, 42, 50, 50)  # Adjust position and size as needed
        self.coin_number_label.setAlignment(Qt.AlignCenter)
        self.coin_number_label.show()

        # Create and add the coin image label
        self.coin_image_label = QLabel(self)
        coin_image_path = os.path.join(self.IMAGE_DIR, "coin.png")  # Change to the path of your coin image
        self.coin_pixmap = QPixmap(coin_image_path)
        
        self.scaled_coin_pixmap = self.coin_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the size as needed
        self.coin_image_label.setGeometry(1730, 25, 70, 70)  # Adjust position and size as needed
        self.coin_image_label.setPixmap(self.scaled_coin_pixmap)


# Create and add the profile picture label
        self.profile_picture_label = QLabel(self)
        profile_picture_path = os.path.join(self.IMAGE_DIR, "home.png")  # Change to the path of your profile picture
        pixmap = QPixmap(profile_picture_path)
        if pixmap.isNull():
            print(f"Failed to load profile picture from {profile_picture_path}")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust the size as needed
        self.profile_picture_label.setPixmap(scaled_pixmap)

        # Position the profile picture label in the top right corner
        self.profile_picture_label.setGeometry(1870 - scaled_pixmap.width(), 10, scaled_pixmap.width(), scaled_pixmap.height())
        self.profile_picture_label.show()




    def set_background_image(self, filename):
        path = os.path.join(self.IMAGE_DIR, filename)
        pixmap = QPixmap(path)
        self.background.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def create_links(self):
        links = [("Home", "home"), ("Achievements", "achievements"), ("Shop", "shop"), 
                 ("Inventory", "inventory"), ("League", "league"), ("Season", "season")]

        y_position = 40
        x_position = 50
        spacing = 33
        font_size = 40

        # Create font
        font = QFont()
        font.setPointSize(font_size)
        font_metrics = QFontMetrics(font)

        for text, page_name in links:
            text_width = font_metrics.horizontalAdvance(text)
            link = CustomLabel(text, self, page_name)
            link.setGeometry(x_position, y_position, text_width, 50)
            link.setFont(font)
            link.show()

            # Update x_position for the next link
            x_position += text_width + spacing

    def init_achievements_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)  # Margin of 40px

        # Create a widget for the achievements section with rounded corners
        achievements_widget = QWidget()
        achievements_widget.setStyleSheet("""
            QWidget {
                border-radius: 20px;
                background-color: #f5f5f5;
                border: 2px solid #002366;
                padding: 20px;
            }
        """)
        
        # Increase the height of the achievements widget
        achievements_widget.setFixedHeight(800)  # Adjust this height as needed

        achievements_layout = QHBoxLayout(achievements_widget)
        achievements_layout.setContentsMargins(20, 20, 20, 20)  # Internal margins

        # Create a widget for the buttons with a common background color
        button_widget = QWidget()
        button_widget.setStyleSheet("background-color: #002366; border-radius: 20px;")
        button_layout = QVBoxLayout(button_widget)

        self.buttons = [
            QPushButton("King of battles"),
            QPushButton("Endurance"),
            QPushButton("Winning")
        ]

        for button in self.buttons:
            button.setStyleSheet("font-size: 30px; color: white; padding: 5px; margin: 5px;")
            button.setFixedWidth(200)  # Set a fixed width for buttons
            button.setFixedHeight(100)  # Set a fixed height for buttons
            button_layout.addWidget(button)

        # Create a stacked widget to switch between different achievements
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_achievement_widget("King of battles", [
            ("Complete 10 battles", 30),
            ("Complete 20 battles", 50),
            ("Complete 30 battles", 70),
            ("Complete 40 battles", 100),
            ("Complete 50 battles", 150),
            ("Complete 60 battles", 200),
            ("Complete 70 battles", 250),
            ("Complete 80 battles", 300),
            ("Complete 90 battles", 350),
            ("Complete 100 battles", 400)
        ]))
        self.stacked_widget.addWidget(self.create_achievement_widget("Endurance", [
            ("Complete 5 battles", 20),
            ("Complete 10 battles", 30),
            ("Complete 15 battles", 50),
            ("Complete 20 battles", 70),
            ("Complete 25 battles", 90),
            ("Complete 30 battles", 110),
            ("Complete 35 battles", 130),
            ("Complete 40 battles", 150),
            ("Complete 45 battles", 170),
            ("Complete 50 battles", 200)
        ]))
        self.stacked_widget.addWidget(self.create_achievement_widget("Winning", [
            ("Win 5 battles", 10),
            ("Win 10 battles", 20),
            ("Win 15 battles", 30),
            ("Win 20 battles", 40),
            ("Win 25 battles", 50),
            ("Win 30 battles", 60),
            ("Win 35 battles", 70),
            ("Win 40 battles", 80),
            ("Win 45 battles", 90),
            ("Win 50 battles", 100)
        ]))

        # Connect buttons to switch between widgets and update styles
        self.buttons[0].clicked.connect(lambda: self.switch_widget(0, self.buttons[0]))
        self.buttons[1].clicked.connect(lambda: self.switch_widget(1, self.buttons[1]))
        self.buttons[2].clicked.connect(lambda: self.switch_widget(2, self.buttons[2]))

        # Add the button widget and stacked widget to achievements layout
        achievements_layout.addWidget(button_widget)
        achievements_layout.addWidget(self.stacked_widget)

        # Add the achievements section to the main layout
        main_layout.addWidget(achievements_widget)

        # Set the layout of the main widget
        self.setLayout(main_layout)

    def switch_widget(self, index, button):
        self.stacked_widget.setCurrentIndex(index)
        self.update_button_styles(button)

    def update_button_styles(self, active_button):
        if self.current_active_button:
            self.current_active_button.setStyleSheet("font-size: 30px; color: white; padding: 5px; margin: 5px; background-color: #002366;")

        active_button.setStyleSheet("font-size: 30px; color: #1E3A95; padding: 5px; margin: 0px; background-color: white; ")
        self.current_active_button = active_button

    def create_achievement_widget(self, title, achievements):
        widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #002366;")
        layout.addWidget(title_label)

        for achievement, reward in achievements:
            achievement_layout = QHBoxLayout()

            achievement_label = QLabel(f"{achievement} - Reward: {reward}")
            achievement_label.setStyleSheet(
                "font-size: 30px; color: #002366; background-color: #E0E0E0; padding: 5px; border-radius: 15px;")
            achievement_label.setFixedHeight(90)  # Set height for each achievement
           

            # Create a button for each achievement with a coin image and reward text
            achievement_button = QPushButton()
            achievement_button.setFixedHeight(90)  # Keep original height
            achievement_button.setFixedWidth(150)  # Smaller width for the button
            achievement_button.setStyleSheet(
                "background-color: #002366; border: 20px solid #002366; border-radius: 15px; padding: 5px;")

            button_layout = QHBoxLayout(achievement_button)
            button_layout.setContentsMargins(5, 5, 5, 5)
            button_layout.setSpacing(5)

            coin_image = QLabel()
            coin_image.setStyleSheet("border:none; ")
            coin_image.setFixedWidth(120)
            pixmap = QPixmap(os.path.join(self.IMAGE_DIR, "coin.png"))
            coin_image.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            button_layout.addWidget(coin_image)

            reward_label = QLabel(str(reward))
            reward_label.setFixedWidth(120)
            reward_label.setStyleSheet("font-size: 40px; color: #F5DA48; border:none")
            button_layout.addWidget(reward_label)

            achievement_layout.addWidget(achievement_label)
            achievement_layout.addWidget(achievement_button)  # Add the button to the layout

            layout.addLayout(achievement_layout)

        widget.setLayout(layout)
        
        # Create a scroll area for the achievements widget
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QScrollArea > QWidget > QWidget { border: none; }
            QWidget { border-radius: 20px; }
        """)
        
        return scroll

    def navigate_to(self, page_name):
        self.main_window.navigate_to(page_name)

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
