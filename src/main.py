import sys
from src.base import hash_password
from src.database import Database
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, \
    QStackedLayout, QListWidget, QHBoxLayout
from PySide6.QtCore import QFile, QTextStream


class MovieTinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.id = None
        self.requests_list = None
        self.email_input = None
        self.confirm_password_signup = None
        self.password_signup = None
        self.email_signup = None
        self.password_login = None
        self.email_login = None
        self.main_page_widget = None
        self.signup_widget = None
        self.login_widget = None
        self.main_layout = None
        self.setWindowTitle("MovieTinder")

        self.init_ui()

    def init_ui(self):
        """Initialize the main UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main stacked layout to switch between login, sign up, and main page views
        self.main_layout = QStackedLayout()

        # Create login, sign up, and main page widgets
        self.login_widget = self.create_login_widget()
        self.signup_widget = self.create_signup_widget()
        self.main_page_widget = self.create_main_page_widget()

        # Add widgets to the main stacked layout
        self.main_layout.addWidget(self.login_widget)
        self.main_layout.addWidget(self.signup_widget)
        self.main_layout.addWidget(self.main_page_widget)

        # Set initial widget to login view
        self.main_layout.setCurrentWidget(self.login_widget)

        # Set central layout
        central_layout = QVBoxLayout(central_widget)
        central_layout.addLayout(self.main_layout)

        # Apply the stylesheet
        self.apply_stylesheet()

    def create_login_widget(self):
        """Create the login widget."""
        login_widget = QWidget()
        layout = QVBoxLayout()

        self.email_login = QLineEdit()
        self.email_login.setPlaceholderText("Email")
        self.password_login = QLineEdit()
        self.password_login.setPlaceholderText("Password")
        self.password_login.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        switch_to_signup_button = QPushButton("Sign Up Instead")

        layout.addWidget(self.email_login)
        layout.addWidget(self.password_login)
        layout.addWidget(login_button)
        layout.addWidget(switch_to_signup_button)

        login_widget.setLayout(layout)

        # Connect button signals to slots
        login_button.clicked.connect(self.login)
        switch_to_signup_button.clicked.connect(self.switch_to_signup)

        return login_widget

    def create_signup_widget(self):
        """Create the sign-up widget."""
        signup_widget = QWidget()
        layout = QVBoxLayout()

        self.email_signup = QLineEdit()
        self.email_signup.setPlaceholderText("Email")
        self.password_signup = QLineEdit()
        self.password_signup.setPlaceholderText("Password")
        self.password_signup.setEchoMode(QLineEdit.Password)
        self.confirm_password_signup = QLineEdit()
        self.confirm_password_signup.setPlaceholderText("Confirm Password")
        self.confirm_password_signup.setEchoMode(QLineEdit.Password)

        signup_button = QPushButton("Sign Up")
        switch_to_login_button = QPushButton("Back to Login")

        layout.addWidget(self.email_signup)
        layout.addWidget(self.password_signup)
        layout.addWidget(self.confirm_password_signup)
        layout.addWidget(signup_button)
        layout.addWidget(switch_to_login_button)

        signup_widget.setLayout(layout)

        # Connect button signals to slots
        signup_button.clicked.connect(self.sign_up)
        switch_to_login_button.clicked.connect(self.switch_to_login)

        return signup_widget

    def create_main_page_widget(self):
        """Create the main page widget."""
        main_page_widget = QWidget()
        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email to add user")
        add_button = QPushButton("Add")
        self.requests_list = QListWidget()
        accept_button = QPushButton("Accept")
        refresh_button = QPushButton("Refresh Requests")

        # Add a horizontal layout for the email input and add button
        email_input_layout = QHBoxLayout()
        email_input_layout.addWidget(self.email_input)
        email_input_layout.addWidget(add_button)

        # Add a horizontal layout for the requests list and accept button
        requests_list_layout = QHBoxLayout()
        requests_list_layout.addWidget(self.requests_list)
        requests_list_layout.addWidget(accept_button)

        layout.addLayout(email_input_layout)
        layout.addLayout(requests_list_layout)
        layout.addWidget(refresh_button)

        main_page_widget.setLayout(layout)

        # Connect button signals to slots
        add_button.clicked.connect(self.add_user_by_email)
        accept_button.clicked.connect(self.accept_request)
        refresh_button.clicked.connect(self.refresh_requests)

        return main_page_widget

    def apply_stylesheet(self):
        """Apply external CSS stylesheet to the application."""
        file = QFile("../resources/stylesheet.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def login(self):
        """Attempt to log in with the provided email and password."""
        global db

        email = self.email_login.text()
        if email == '':
            QMessageBox.warning(self, "Login", "Email can't be empty")
            return
        if self.password_login.text() == '':
            QMessageBox.warning(self, "Login", "Password can't be empty")
            return
        password = hash_password(self.password_login.text())

        self.id = db.try_login(email, password)

        if self.id == -1:
            QMessageBox.warning(self, "Login", "Login Failed")
            return
        else:
            QMessageBox.information(self, "Login", "Login Successful")
            self.main_layout.setCurrentWidget(self.main_page_widget)
            # Display requests
            self.refresh_requests()

    def sign_up(self):
        """Attempt to sign up with the provided email, password, and confirmation password."""
        email = self.email_signup.text()
        if email == '':
            QMessageBox.warning(self, "Sign Up", "Email can't be empty")
            return
        if self.password_signup.text() == '':
            QMessageBox.warning(self, "Sign Up", "Password can't be empty")
            return
        password = hash_password(self.password_signup.text())
        confirm_password = hash_password(self.confirm_password_signup.text())

        if password != confirm_password:
            QMessageBox.warning(self, "Sign Up", "Passwords do not match")
            return
        if not db.sign_up(email, password):
            QMessageBox.warning(self, "Sign Up", "email already exists")
            return
        else:
            QMessageBox.information(self, "Sign Up", "Sign Up Successful")
            self.switch_to_login()

    def switch_to_signup(self):
        """Switch to the sign-up view and clear sign-up input fields."""
        self.clear_signup_fields()
        self.main_layout.setCurrentWidget(self.signup_widget)

    def switch_to_login(self):
        """Switch to the login view and clear login input fields."""
        self.clear_login_fields()
        self.main_layout.setCurrentWidget(self.login_widget)

    def clear_login_fields(self):
        """Clear input fields in the login widget."""
        self.email_login.clear()
        self.password_login.clear()

    def clear_signup_fields(self):
        """Clear input fields in the sign-up widget."""
        self.email_signup.clear()
        self.password_signup.clear()
        self.confirm_password_signup.clear()

    def add_user_by_email(self):
        """Add another user."""
        email = self.email_input.text()
        # Add logic to add another user

    def accept_request(self):
        """Accept the selected email from the requests list."""
        selected_items = self.requests_list.selectedItems()
        if selected_items:
            email = selected_items[0].text()
            QMessageBox.information(self, "Email Accepted", f"Accepted Request: {email}")
        else:
            QMessageBox.warning(self, "No Selection", "No email selected")

    def refresh_requests(self):
        """Refresh the requests list (clear and reload, if necessary)."""
        self.requests_list.clear()
        # Add logic to reload the list


if __name__ == "__main__":
    db = Database()
    app = QApplication(sys.argv)
    window = MovieTinder()
    window.show()
    sys.exit(app.exec())
