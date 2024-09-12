import os
import time
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QPushButton,QTextEdit,QApplication
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics,QFontDatabase
from PyQt5.QtCore import Qt, QTimer

class CustomLabel(QLabel):
    def __init__(self, text, parent=None, page_name=None):
        super().__init__(text, parent)
        self.page_name = page_name
        self.default_color = "white"
        self.hover_color = "#1E3A95"
        self.setStyleSheet(f"color: {self.default_color};")
        self.setFont(QFont('aladin', 40))
        

    def enterEvent(self, event):
        self.setStyleSheet(f"color: {self.hover_color};")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(f"color: {self.default_color};")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.page_name:                                # If none evaluate false
            self.parent().navigate_to_page(self.page_name)
        super().mousePressEvent(event)

class Battle(QWidget):
    BASE_IMAGE_DIR = "F:\\vs_folder\\python_V1_6\\photos"
    

    def __init__(self, main_window, db, user_id):
        super().__init__()
        self.main_window = main_window
        self.db = db
        self.user_id = user_id

        self.setGeometry(0, 0, 1920, 1080)
        self.final_words_per_minute = 0
        self.final_accuracy = 0
        self.game_ended = False  # Add a flag to track if the game has ended
        self.load_custom_font()

        # Create background
        self.background = QLabel(self)
        self.set_background_image("ba.jpg")
        self.background.setGeometry(0, 0, 1920, 1080)

        # Define widget properties
        y_position = 40
        x_position = 50
        spacing = 33
        font_size = 40

        # Create font
        font = QFont()
        font.setPointSize(font_size)

        # Create link labels
        self.create_links(font, x_position, y_position, spacing)

        # Create player labels
        self.player1 = QLabel(self)
        self.player1.setFixedSize(400, 560)
        self.set_image(self.player1, "ch1.png")
        self.player1.setGeometry(90, 30, 400, 560)
        self.player1.show()

        self.player2 = QLabel(self)
        self.player2.setFixedSize(400, 560)
        self.set_image(self.player2, "ch2.png")
        self.player2.setGeometry(1400, 30, 400, 560)
        self.player2.show()


        # Create health bars
        self.player1_health = QProgressBar(self)
        self.player1_health.setRange(0, 100)
        self.player1_health.setValue(100)
        self.player1_health.setFixedSize(200, 20)
        self.player1_health.setGeometry(100, 520, 200, 20)

        self.player2_health = QProgressBar(self)
        self.player2_health.setRange(0, 100)
        self.player2_health.setValue(100)
        self.player2_health.setFixedSize(200, 20)
        self.player2_health.setGeometry(1620, 520, 200, 20)




        self.scaling_factor = 1.5  # Variable to control the size of widgets

        # Base dimensions
        base_width_typeB = 560
        base_height_typeB = 275
        base_width_label = 535
        base_height_label = 260

        # Scaled dimensions
        width_typeB = int(base_width_typeB * self.scaling_factor)
        height_typeB = int(base_height_typeB * self.scaling_factor)
        width_label = int(base_width_label * self.scaling_factor)
        height_label = int(base_height_label * self.scaling_factor)

        # Create input background
        self.typeB = QLabel(self)
        self.typeB.setFixedSize(width_typeB, height_typeB)
        self.set_image(self.typeB, "typeB.jpg")
        self.typeB.setGeometry(600, 650, width_typeB, height_typeB)
        self.typeB.show()

        # Create target word label
        self.target_word_label = QLabel(self)
        self.target_word = "here we go again"
        self.target_word_label.setText(self.target_word)
        self.target_word_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.target_word_label.setFont(QFont('Arial', int(30 * self.scaling_factor)))
        self.target_word_label.setWordWrap(True)
        self.target_word_label.setGeometry(607, 657, width_label, height_label)

        # Create text input for player 1
        self.text_input = QTextEdit(self)
        self.text_input.setFixedSize(width_label, height_label)
        self.text_input.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.text_input.setFont(QFont('Arial', int(30 * self.scaling_factor)))
        self.text_input.setStyleSheet("background: transparent; color: white;")
        self.text_input.textChanged.connect(self.handle_text_changed)
        self.text_input.setGeometry(607, 657, width_label, height_label)
        self.update_target_word_position()




        # Create restart button
        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setFixedHeight(60)
        self.restart_button.setFont(QFont('aladin', 30))
        self.restart_button.clicked.connect(self.restart_game)
        self.restart_button.hide()
        self.restart_button.setGeometry(960 - 100, 950, 200, 60)

        # Add typing speed and accuracy labels
        self.speed_label = QLabel("Typing Speed: 0 wpm", self)
        self.speed_label.setFont(QFont('aladin', 30))
        self.speed_label.setGeometry(100, 560, 300, 40)
        self.speed_label.setStyleSheet("color: white;")

        self.accuracy_label = QLabel("Accuracy: 0%", self)
        self.accuracy_label.setFont(QFont('aladin', 30))
        self.accuracy_label.setGeometry(100, 610, 300, 40)
        self.accuracy_label.setStyleSheet("color: white;")

        # Create winning message label
        self.winning_message = QLabel("", self)
        self.winning_message.setFont(QFont('Arial', 40))
        self.winning_message.setAlignment(Qt.AlignCenter)
        self.winning_message.setGeometry(560, 300, 800, 200)
        self.winning_message.setStyleSheet("color: #1E3A95 ; background-color: white; border-radius:30px; border: 10px solid black; font-family:aladin")
        self.winning_message.hide()

        # Initialize typing metrics
        self.start_time = None
        self.total_chars = 0
        self.correct_chars = 0
        self.incorrect_chars = 0
        self.last_update_time = time.time()

        # Bullets list
        self.bullets = []

        # Track current position in target word
        self.current_index = 0

        # Start the second character shooting timer for player 2
        self.player2_shooting_timer = QTimer(self)
        self.player2_shooting_timer.timeout.connect(self.shoot_bullet_from_player2)


    def update_target_word_position(self):
            text_input_rect = self.text_input.geometry()
            x = text_input_rect.x()
            y = text_input_rect.y()
            width = text_input_rect.width()
            self.target_word_label.setGeometry(x, y, width, self.target_word_label.height())


    def create_links(self, font, x_position, y_position, spacing):
        links = [("Home", "home"), ("achievements", "achievements"), ("shop", "shop"),
                 ("inventory", "inventory"), ("league", "league"), ("seseon", "seseon")]

        font_metrics = QFontMetrics(font)
        current_x_position = x_position

        for text, page_name in links:
            text_width = font_metrics.horizontalAdvance(text)
            link = CustomLabel(text, self, page_name)
            link.setGeometry(current_x_position, y_position, text_width, 50)
            link.setFont(font)
            link.setAlignment(Qt.AlignCenter)
            link.show()

            current_x_position += text_width + spacing

    def navigate_to_page(self, page_name):
        self.main_window.navigate_to(page_name)

    def set_background_image(self, filename):
        path = os.path.join(self.BASE_IMAGE_DIR, filename)
        pixmap = QPixmap(path)
        self.background.setPixmap(pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def set_image(self, label, filename):
        path = os.path.join(self.BASE_IMAGE_DIR, filename)
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Error: Could not load image from {path}")
        else:
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.show()

    def handle_text_changed(self):
        if self.game_ended:
            return  # Do nothing if the game has ended

        text = self.text_input.toPlainText()
        target_word = self.target_word

        if self.start_time is None and text:  # Start the timer when the first letter is typed
            self.start_time = time.time()
            self.start_player2_shooting()  # Start player 2 shooting after first letter is typed

        # Update the current index if the typed character matches the target word
        if len(text) > self.current_index:
            if text[self.current_index] == target_word[self.current_index]:
                self.correct_chars += 1
                self.shoot_bullet_from_player1()  # Player 1 shoots a bullet
                self.current_index += 1
            else:
                self.incorrect_chars += 1

        # Reset when the target word is fully typed
        if self.current_index == len(target_word):
            self.current_index = 0
            self.text_input.clear()
            self.target_word_label.setText(self.target_word)
            self.target_word_label.adjustSize()

        self.update_metrics()

    def update_metrics(self):
        if self.start_time is None:
            elapsed_time = 0
        else:
            elapsed_time = time.time() - self.start_time

        self.total_chars = self.correct_chars + self.incorrect_chars

        if elapsed_time > 0:
            # Calculate words per minute (wpm)
            words_per_minute = (self.total_chars / 5) / (elapsed_time / 60)
            total_chars_with_errors = self.total_chars + self.incorrect_chars
            accuracy = (self.correct_chars / max(total_chars_with_errors, 1)) * 100

            self.speed_label.setText(f"Typing Speed: {int(words_per_minute)} wpm")
            self.accuracy_label.setText(f"Accuracy: {int(accuracy)}%")

    def shoot_bullet_from_player1(self):
        if self.game_ended:
            return  # Do nothing if the game has ended

        bullet = QLabel(self)
        bullet.setFixedSize(100, 60)
        path = os.path.join(self.BASE_IMAGE_DIR, "b.png")
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Error: Could not load bullet image from {path}")
        else:
            bullet.setPixmap(pixmap.scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            player_pos = self.player1.geometry()
            bullet.setGeometry(player_pos.x() + player_pos.width() - 90, player_pos.y() + player_pos.height() // 2 - 165, 100, 60)
            bullet.show()

            self.bullets.append(bullet)
            self.animate_bullet(bullet, from_player2=False)

    def shoot_bullet_from_player2(self):
        if self.game_ended:
            return  # Do nothing if the game has ended

        bullet = QLabel(self)
        bullet.setFixedSize(80, 40)
        path = os.path.join(self.BASE_IMAGE_DIR, "b2.png")
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Error: Could not load bullet image from {path}")
        else:
            bullet.setPixmap(pixmap.scaled(80, 40))
            player_pos = self.player2.geometry()
            bullet.setGeometry(player_pos.x() + player_pos.width() - 360, player_pos.y() + player_pos.height() // 2 - 115, 80, 40)
            bullet.show()

            self.bullets.append(bullet)
            self.animate_bullet(bullet, from_player2=True)

    def animate_bullet(self, bullet, from_player2=False):
        def move_bullet():
            if bullet in self.bullets:
                if from_player2:
                    bullet.setGeometry(bullet.geometry().x() - 250, bullet.geometry().y(), 60, 60)
                    if bullet.geometry().x() < 0:
                        bullet.hide()
                        self.bullets.remove(bullet)
                    else:
                        expanded_player1_rect = self.player1.geometry().adjusted(-50, -50, -50, -50)
                        if bullet.geometry().intersects(expanded_player1_rect):
                            bullet.hide()
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            self.update_health(self.player1_health)
                else:
                    bullet.setGeometry(bullet.geometry().x() + 250, bullet.geometry().y(), 60, 60)
                    if bullet.geometry().x() > self.width():
                        bullet.hide()
                        self.bullets.remove(bullet)
                    else:
                        expanded_player2_rect = self.player2.geometry().adjusted(120, 120, 50, 50)
                        if bullet.geometry().intersects(expanded_player2_rect):
                            bullet.hide()
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            self.update_health(self.player2_health)

        timer = QTimer(self)
        timer.timeout.connect(move_bullet)
        timer.start(30)

    def update_health(self, health_bar):
        new_health = health_bar.value() - 10
        health_bar.setValue(new_health)
        if new_health == 0:
            self.end_timer()  # End the timer when a player is defeated
            self.display_winning_message()  # Display the winning message
            self.restart_button.show()
            self.game_ended = True  # Set the flag to indicate the game has ended
            self.player2_shooting_timer.stop()  # Stop the player 2 shooting timer

    def end_timer(self):
        self.end_time = time.time()
        self.update_metrics()  
        self.save_match_data()

    def save_match_data(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='matches';"
        result = self.db.conn.execute(query).fetchone()
        
        if result is None:
            raise Exception("The 'matches' table does not exist in the database.")
        
        if self.start_time and self.end_time:
            elapsed_time = self.end_time - self.start_time
            words_per_minute = (self.total_chars / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
            accuracy = (self.correct_chars / max(self.total_chars + self.incorrect_chars, 1)) * 100
            
            query = "INSERT INTO matches (user_id, date, speed, accuracy) VALUES (?, DATE('now'), ?, ?)"
            self.db.conn.execute(query, (self.user_id, words_per_minute, accuracy))
            self.db.conn.commit()

    def display_winning_message(self):
        elapsed_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        self.final_words_per_minute = (self.total_chars / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
        self.final_accuracy = (self.correct_chars / max(self.total_chars + self.incorrect_chars, 1)) * 100

        if self.player1_health.value() == 0:
            self.winning_message.setText(f"Defeated!\nSpeed: {int(self.final_words_per_minute)} wpm\nAccuracy: {int(self.final_accuracy)}%")
        else:
            self.winning_message.setText(f"You won!\nSpeed: {int(self.final_words_per_minute)} wpm\nAccuracy: {int(self.final_accuracy)}%")
        self.winning_message.show()

    def restart_game(self):
        self.player1_health.setValue(100)
        self.player2_health.setValue(100)
        self.target_word_label.setText(self.target_word)
        self.text_input.clear()
        self.current_index = 0
        self.start_time = None
        self.end_time = None
        self.incorrect_chars = 0  # Reset incorrect characters count

        for bullet in self.bullets:
            bullet.hide()
        self.bullets.clear()
        self.restart_button.hide()

        # Hide winning message
        self.winning_message.hide()

        # Reset typing metrics
        self.total_chars = 0
        self.correct_chars = 0
        self.update_metrics()

        # Reset game ended flag
        self.game_ended = False

    def start_player2_shooting(self):
        self.player2_shooting_timer.start(60000 // 250)  # 50 wpm means 5 bullets every 1.2 seconds (60000ms / 250)


    def load_custom_font(self):
        font_path = os.path.join(self.BASE_IMAGE_DIR , "Aladin.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            QApplication.setFont(QFont(font_family))
        else:
            print("Failed to load font.")
