import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, \
    QMessageBox, QStackedLayout
from PySide6.QtCore import QFile, QTextStream


class LoginSignUpApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login and Sign Up")

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        self.main_layout = QStackedLayout()

        # Create login and sign up widgets
        self.login_widget = self.create_login_widget()
        self.signup_widget = self.create_signup_widget()

        # Add widgets to the main layout
        self.main_layout.addWidget(self.login_widget)
        self.main_layout.addWidget(self.signup_widget)

        # Set initial widget to login
        self.main_layout.setCurrentWidget(self.login_widget)

        central_layout = QVBoxLayout(central_widget)
        central_layout.addLayout(self.main_layout)

        # Apply the stylesheet
        self.apply_stylesheet()

        # Placeholder for user database
        self.user_database = {}

    def create_login_widget(self):
        login_widget = QWidget()
        layout = QVBoxLayout()

        self.username_login = QLineEdit()
        self.username_login.setPlaceholderText("Username")
        self.password_login = QLineEdit()
        self.password_login.setPlaceholderText("Password")
        self.password_login.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        switch_to_signup_button = QPushButton("Sign Up Instead")

        layout.addWidget(self.username_login)
        layout.addWidget(self.password_login)
        layout.addWidget(login_button)
        layout.addWidget(switch_to_signup_button)

        login_widget.setLayout(layout)

        login_button.clicked.connect(self.login)
        switch_to_signup_button.clicked.connect(self.switch_to_signup)

        return login_widget

    def create_signup_widget(self):
        signup_widget = QWidget()
        layout = QVBoxLayout()

        self.username_signup = QLineEdit()
        self.username_signup.setPlaceholderText("Username")
        self.password_signup = QLineEdit()
        self.password_signup.setPlaceholderText("Password")
        self.password_signup.setEchoMode(QLineEdit.Password)
        self.confirm_password_signup = QLineEdit()
        self.confirm_password_signup.setPlaceholderText("Confirm Password")
        self.confirm_password_signup.setEchoMode(QLineEdit.Password)

        signup_button = QPushButton("Sign Up")
        switch_to_login_button = QPushButton("Back to Login")

        layout.addWidget(self.username_signup)
        layout.addWidget(self.password_signup)
        layout.addWidget(self.confirm_password_signup)
        layout.addWidget(signup_button)
        layout.addWidget(switch_to_login_button)

        signup_widget.setLayout(layout)

        signup_button.clicked.connect(self.sign_up)
        switch_to_login_button.clicked.connect(self.switch_to_login)

        return signup_widget

    def apply_stylesheet(self):
        file = QFile("../resources/stylesheet.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def login(self):
        username = self.username_login.text()
        password = self.password_login.text()

        if username in self.user_database and self.user_database[username] == password:
            QMessageBox.information(self, "Login", "Login Successful")
        else:
            QMessageBox.warning(self, "Login", "Login Failed")

    def sign_up(self):
        username = self.username_signup.text()
        password = self.password_signup.text()
        confirm_password = self.confirm_password_signup.text()

        if username in self.user_database:
            QMessageBox.warning(self, "Sign Up", "Username already exists")
        elif password != confirm_password:
            QMessageBox.warning(self, "Sign Up", "Passwords do not match")
        else:
            self.user_database[username] = password
            QMessageBox.information(self, "Sign Up", "Sign Up Successful")

    def switch_to_signup(self):
        self.clear_signup_fields()
        self.main_layout.setCurrentWidget(self.signup_widget)

    def switch_to_login(self):
        self.clear_login_fields()
        self.main_layout.setCurrentWidget(self.login_widget)

    def clear_login_fields(self):
        self.username_login.clear()
        self.password_login.clear()

    def clear_signup_fields(self):
        self.username_signup.clear()
        self.password_signup.clear()
        self.confirm_password_signup.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginSignUpApp()
    window.show()
    sys.exit(app.exec())
