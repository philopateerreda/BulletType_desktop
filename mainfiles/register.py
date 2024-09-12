import os
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,QApplication
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt
from database import Database

class Register(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(0, 0, 1920, 1080)

        # Initialize database
        self.db = Database()

        self.base_dir = "F:\\vs_folder\\python_V1_6\\photos"
        
        self.load_background_image("register.jpg")

        self.transparent_rect = QLabel(self)
        self.transparent_rect.setGeometry(564, 310, 761, 610)
        self.transparent_rect.setStyleSheet("background-color: rgba(0, 0, 0, 10); border-radius: 15px;")

        self.page_indicator = QLabel("Sign In", self)
        self.page_indicator.setGeometry(564, 350, 761, 60)
        self.page_indicator.setAlignment(Qt.AlignCenter)
        self.page_indicator.setStyleSheet("color: #1E3A95; font-size: 40px;")
        self.page_indicator.setFont(QFont("Aladin", 32))

        self.create_social_media_logos()
        self.create_sign_in_elements()
        self.create_sign_up_elements()

        self.hide_sign_in_elements()
        self.show_sign_up_elements()

        self.sign_in_button.clicked.connect(self.sign_in)
        self.sign_up_button.clicked.connect(self.sign_up)


    def load_background_image(self, image_name):
        pixmap = QPixmap(os.path.join(self.base_dir, image_name))
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap.scaled(1920, 1080, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setGeometry(0, 0, 1920, 1080)

    def create_social_media_logos(self):
        x_offset = 564 + 290

        self.google_logo = QLabel(self)
        self.google_logo.setGeometry(x_offset, 440, 50, 50)
        self.google_logo.setPixmap(QPixmap(os.path.join(self.base_dir, "google.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.google_logo.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        self.facebook_logo = QLabel(self)
        self.facebook_logo.setGeometry(x_offset + 60, 440, 50, 50)
        self.facebook_logo.setPixmap(QPixmap(os.path.join(self.base_dir, "facebook.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.facebook_logo.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        self.github_logo = QLabel(self)
        self.github_logo.setGeometry(x_offset + 120, 440, 50, 50)
        self.github_logo.setPixmap(QPixmap(os.path.join(self.base_dir, "github.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.github_logo.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

    def create_sign_in_elements(self):
        y_offset = 500

        self.username_label = QLabel("Username:", self)
        self.username_label.setGeometry(690, y_offset, 200, 40)
        self.username_label.setStyleSheet("color: #1E3A95; font-size: 26px;")
        self.username_label.setFont(QFont("Aladin", 24))

        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(784, y_offset, 400, 40)
        self.username_input.setStyleSheet("border: 2px solid black; border-radius: 10px; padding: 5px; font-size: 24px;")

        self.password_label = QLabel("Password:", self)
        self.password_label.setGeometry(690, y_offset + 60, 200, 40)
        self.password_label.setStyleSheet("color: #1E3A95; font-size: 26px;")
        self.password_label.setFont(QFont("Aladin", 18))

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(784, y_offset + 60, 400, 40)
        self.password_input.setStyleSheet("border: 2px solid black; border-radius: 10px; padding: 5px; font-size: 20px;")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.sign_in_button = QPushButton("Sign In", self)
        self.sign_in_button.setGeometry(784, y_offset + 120, 400, 40)
        self.sign_in_button.setStyleSheet("border: 2px solid black; border-radius: 10px; background-color: #1E3A95; color: white; font-size: 25px;")
        self.sign_in_button.setFont(QFont("Aladin", 18))

        self.signup_prompt = QLabel("You don't have an account? Sign up.", self)
        self.signup_prompt.setGeometry(784, y_offset + 180, 400, 40)
        self.signup_prompt.setStyleSheet("color: #1E3A95; font-size: 18px;")
        self.signup_prompt.setFont(QFont("Aladin", 18))
        self.signup_prompt.mousePressEvent = self.show_sign_up

    def create_sign_up_elements(self):
        y_offset = 500

        self.email_label = QLabel("Email:", self)
        self.email_label.setGeometry(695, y_offset, 200, 40)
        self.email_label.setStyleSheet("color: #1E3A95; font-size: 26px;")
        self.email_label.setFont(QFont("Aladin", 24))

        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(784, y_offset, 400, 40)
        self.email_input.setStyleSheet("border: 2px solid black; border-radius: 10px; padding: 5px; font-size: 24px;")

        self.new_username_label = QLabel("Username:", self)
        self.new_username_label.setGeometry(690, y_offset + 60, 200, 40)
        self.new_username_label.setStyleSheet("color: #1E3A95; font-size: 26px;")
        self.new_username_label.setFont(QFont("Aladin", 24))

        self.new_username_input = QLineEdit(self)
        self.new_username_input.setGeometry(784, y_offset + 60, 400, 40)
        self.new_username_input.setStyleSheet("border: 2px solid black; border-radius: 10px; padding: 5px; font-size: 24px;")

        self.new_password_label = QLabel("Password:", self)
        self.new_password_label.setGeometry(690, y_offset + 120, 200, 40)
        self.new_password_label.setStyleSheet("color: #1E3A95; font-size: 26px;")
        self.new_password_label.setFont(QFont("Aladin", 18))

        self.new_password_input = QLineEdit(self)
        self.new_password_input.setGeometry(784, y_offset + 120, 400, 40)
        self.new_password_input.setStyleSheet("border: 2px solid black; border-radius: 10px; padding: 5px; font-size: 20px;")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.sign_up_button = QPushButton("Sign Up", self)
        self.sign_up_button.setGeometry(784, y_offset + 180, 400, 40)
        self.sign_up_button.setStyleSheet("border: 2px solid black; border-radius: 10px; background-color: #1E3A95; color: white; font-size: 25px;")
        self.sign_up_button.setFont(QFont("Aladin", 18))

        self.signin_prompt = QLabel("Already have an account? Sign In.", self)
        self.signin_prompt.setGeometry(784, y_offset + 240, 400, 40)
        self.signin_prompt.setStyleSheet("color: #1E3A95; font-size: 18px;")
        self.signin_prompt.setFont(QFont("Aladin", 18))
        self.signin_prompt.mousePressEvent = self.show_sign_in

    def show_sign_in(self, event):
        self.hide_sign_up_elements()
        self.show_sign_in_elements()

    def show_sign_up(self, event):
        self.hide_sign_in_elements()
        self.show_sign_up_elements()

    def show_sign_in_elements(self):
        self.page_indicator.setText("Sign In")
        self.username_label.show()
        self.username_input.show()
        self.password_label.show()
        self.password_input.show()
        self.sign_in_button.show()
        self.signup_prompt.show()
        self.google_logo.show()
        self.facebook_logo.show()
        self.github_logo.show()

    def hide_sign_in_elements(self):
        self.username_label.hide()
        self.username_input.hide()
        self.password_label.hide()
        self.password_input.hide()
        self.sign_in_button.hide()
        self.signup_prompt.hide()
        self.google_logo.hide()
        self.facebook_logo.hide()
        self.github_logo.hide()

    def show_sign_up_elements(self):
        self.page_indicator.setText("Sign Up")
        self.email_label.show()
        self.email_input.show()
        self.new_username_label.show()
        self.new_username_input.show()
        self.new_password_label.show()
        self.new_password_input.show()
        self.sign_up_button.show()
        self.signin_prompt.show()
        self.google_logo.show()
        self.facebook_logo.show()
        self.github_logo.show()

    def hide_sign_up_elements(self):
        self.email_label.hide()
        self.email_input.hide()
        self.new_username_label.hide()
        self.new_username_input.hide()
        self.new_password_label.hide()
        self.new_password_input.hide()
        self.sign_up_button.hide()
        self.signin_prompt.hide()
        self.google_logo.hide()
        self.facebook_logo.hide()
        self.github_logo.hide()



        

    def sign_in(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.db.validate_user(username, password):
            # Retrieve user_id after successful sign-in
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            user_id = cursor.fetchone()[0]

            # Set user_id in the main window
            self.main_window.set_user_id(user_id)

            self.main_window.navigate_to("home")
        else:
            QMessageBox.critical(self, "Error", "Invalid Username or Password!")



    def sign_up(self):
        username = self.new_username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.new_password_input.text().strip()
        
        if not username or not email or not password:
            QMessageBox.critical(self, "Error", "All fields are required!")
            return
        
        if self.db.user_exists(username, email):
            QMessageBox.critical(self, "Error", "Username or Email already exists!")
        else:
            if self.db.register_user(username, email, password):
                QMessageBox.information(self, "Success", "Sign Up Successful!")
                self.show_sign_in(None)
            else:
                QMessageBox.critical(self, "Error", "Sign Up Failed!")
