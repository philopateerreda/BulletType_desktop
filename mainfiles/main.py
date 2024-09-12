import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from home import Home
from battle import Battle
from register import Register
from stats import Stats
from achievements import Achievements
from database import Database  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the database
        self.db = Database()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize pages without user_id
        self.home = Home(self)
        self.battle = Battle(self, self.db, None)  # Initialize with None for user_id
        self.register = Register(self)
        self.stats = Stats(self, self.db, None)  # Initialize with None for user_id
        self.achievements = Achievements(self)

        # Add pages to the stacked widget
        self.central_widget.addWidget(self.register)
        self.central_widget.addWidget(self.home)
        self.central_widget.addWidget(self.battle)
        self.central_widget.addWidget(self.stats)
        self.central_widget.addWidget(self.achievements)

    def set_user_id(self, user_id):
        self.user_id = user_id
        # Update pages with the new user_id
        self.battle.user_id = user_id
        self.stats.user_id = user_id

    def navigate_to(self, page_name):
        if page_name == "home":
            self.central_widget.setCurrentWidget(self.home)
        elif page_name == "battle":
            self.central_widget.setCurrentWidget(self.battle)
        elif page_name == "register":
            self.central_widget.setCurrentWidget(self.register)
        elif page_name == "stats":
            self.central_widget.setCurrentWidget(self.stats)
            self.stats.load_statistics()  # Ensure statistics are updated
        elif page_name == "achievements":
            self.central_widget.setCurrentWidget(self.achievements)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize the main window without a user_id
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
