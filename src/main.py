import sys
from datetime import datetime
from src.base import hash_password
from src.database import Database
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, \
    QStackedLayout, QListWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QFile, QByteArray, QTextStream, Qt


class MovieTinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.match_ids = None
        self.match_index = -1
        self.matches = None
        self.selected_connection = None
        self.movie_ids = None
        self.movies = None
        self.movie_index = -1
        self.connections = None
        self.match_movie_genres_label = None
        self.match_movie_release_date_label = None
        self.match_movie_cover_label = None
        self.match_movie_title_label = None
        self.matches_list = None
        self.movie_genres_label = None
        self.movie_release_date_label = None
        self.movie_cover_label = None
        self.movie_title_label = None
        self.requests = None
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
        self.swiping_widget = None
        self.matches_widget = None
        self.match_details_widget = None
        self.main_layout = None
        self.setWindowTitle("MovieTinder")

        self.init_ui()

    def init_ui(self):
        """Initialize the main UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main stacked layout to switch between login, sign up, main page, swiping page, and matches page views
        self.main_layout = QStackedLayout()

        # Create login, sign up, main page, swiping page, and matches page widgets
        self.login_widget = self.create_login_widget()
        self.signup_widget = self.create_signup_widget()
        self.main_page_widget = self.create_main_page_widget()
        self.swiping_widget = self.create_swiping_widget()
        self.matches_widget = self.create_matches_widget()
        self.match_details_widget = self.create_match_details_widget()

        # Add widgets to the main stacked layout
        self.main_layout.addWidget(self.login_widget)
        self.main_layout.addWidget(self.signup_widget)
        self.main_layout.addWidget(self.main_page_widget)
        self.main_layout.addWidget(self.swiping_widget)
        self.main_layout.addWidget(self.matches_widget)
        self.main_layout.addWidget(self.match_details_widget)

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
        switch_to_swiping_button = QPushButton("Start Swiping")
        switch_to_matches_button = QPushButton("View Matches")

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
        layout.addWidget(switch_to_swiping_button)
        layout.addWidget(switch_to_matches_button)

        main_page_widget.setLayout(layout)

        # Connect button signals to slots
        add_button.clicked.connect(self.add_user_by_email)
        accept_button.clicked.connect(self.accept_request)
        refresh_button.clicked.connect(self.refresh_requests)
        switch_to_swiping_button.clicked.connect(self.switch_to_swiping)
        switch_to_matches_button.clicked.connect(self.switch_to_matches)

        return main_page_widget

    def create_swiping_widget(self):
        """Create the swiping page widget."""
        swiping_widget = QWidget()
        layout = QVBoxLayout()

        self.movie_title_label = QLabel("Movie Title Placeholder")
        self.movie_title_label.setAlignment(Qt.AlignCenter)

        self.movie_cover_label = QLabel()
        self.movie_cover_label.setPixmap(QPixmap("../resources/placeholder_image.png"))
        self.movie_cover_label.setAlignment(Qt.AlignCenter)

        self.movie_release_date_label = QLabel("Release Date: Placeholder")
        self.movie_release_date_label.setAlignment(Qt.AlignCenter)

        self.movie_genres_label = QLabel("Genres: Placeholder")
        self.movie_genres_label.setAlignment(Qt.AlignCenter)

        like_button = QPushButton()
        like_button.setText("✔️")
        dislike_button = QPushButton()
        dislike_button.setText("❌")
        back_to_main_button = QPushButton("Back to Main Page")

        layout.addWidget(self.movie_title_label)
        layout.addWidget(self.movie_cover_label)
        layout.addWidget(self.movie_release_date_label)
        layout.addWidget(self.movie_genres_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(dislike_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(like_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)
        layout.addWidget(back_to_main_button, alignment=Qt.AlignCenter)

        swiping_widget.setLayout(layout)

        # Connect button signals to slots
        like_button.clicked.connect(self.like_movie)
        dislike_button.clicked.connect(self.dislike_movie)
        back_to_main_button.clicked.connect(self.switch_to_main_page)

        return swiping_widget

    def create_matches_widget(self):
        """Create the matches page widget."""
        matches_widget = QWidget()
        layout = QVBoxLayout()

        self.matches_list = QListWidget()
        view_match_button = QPushButton("View Match")
        back_to_main_button = QPushButton("Back to Main Page")

        layout.addWidget(self.matches_list)
        layout.addWidget(view_match_button)
        layout.addWidget(back_to_main_button)

        matches_widget.setLayout(layout)

        # Connect button signals to slots
        view_match_button.clicked.connect(self.view_match)
        back_to_main_button.clicked.connect(self.switch_to_main_page)

        return matches_widget

    def create_match_details_widget(self):
        """Create the match details widget."""
        match_details_widget = QWidget()
        layout = QVBoxLayout()

        self.match_movie_title_label = QLabel("Movie Title Placeholder")
        self.match_movie_title_label.setAlignment(Qt.AlignCenter)

        self.match_movie_cover_label = QLabel()
        self.match_movie_cover_label.setPixmap(QPixmap("../resources/placeholder_image.png"))
        self.match_movie_cover_label.setAlignment(Qt.AlignCenter)

        self.match_movie_release_date_label = QLabel("Release Date: Placeholder")
        self.match_movie_release_date_label.setAlignment(Qt.AlignCenter)

        self.match_movie_genres_label = QLabel("Genres: Placeholder")
        self.match_movie_genres_label.setAlignment(Qt.AlignCenter)

        previous_button = QPushButton("Previous")
        next_button = QPushButton("Next")
        back_to_matches_button = QPushButton("Back to Matches Page")

        layout.addWidget(self.match_movie_title_label)
        layout.addWidget(self.match_movie_cover_label)
        layout.addWidget(self.match_movie_release_date_label)
        layout.addWidget(self.match_movie_genres_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(previous_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(next_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)
        layout.addWidget(back_to_matches_button, alignment=Qt.AlignCenter)

        match_details_widget.setLayout(layout)

        # Connect button signals to slots
        previous_button.clicked.connect(self.previous_match)
        next_button.clicked.connect(self.next_match)
        back_to_matches_button.clicked.connect(self.switch_to_matches)

        return match_details_widget

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

    def switch_to_main_page(self):
        """Switch to the main page view."""
        self.main_layout.setCurrentWidget(self.main_page_widget)

    def switch_to_swiping(self):
        """Switch to the swiping page view."""
        self.main_layout.setCurrentWidget(self.swiping_widget)
        self.movie_index -= 1
        self.display_next_movie()

    def switch_to_matches(self):
        """Switch to the matches page view."""
        self.main_layout.setCurrentWidget(self.matches_widget)
        self.matches_list.clear()
        connections = db.get_users_connections(self.id)
        self.connections = {value: key for (key, value) in connections.items()}
        self.matches_list.addItems(list(connections.values()))

    def switch_to_match_details(self):
        """Switch to the match details view."""
        self.main_layout.setCurrentWidget(self.match_details_widget)
        self.match_index = -1
        self.next_match()

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
        if email == '':
            QMessageBox.warning(self, "Request", "Email can't be empty")
            return
        if not db.create_connection_request(self.id, email):
            QMessageBox.information(self, "Request", f"Failed to send Request to: {email}")
            return
        QMessageBox.information(self, "Request", f"Sent Request to: {email}")
        self.email_input.clear()

    def accept_request(self):
        """Accept the selected email from the requests list."""
        selected_items = self.requests_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "No email selected")
            return
        for item in selected_items:
            db.accept_connection(self.requests[item.text()])
            QMessageBox.information(self, "Request Accepted", f"Accepted Request: {item.text()}")
        self.refresh_requests()

    def refresh_requests(self):
        """Refresh the requests list (clear and reload, if necessary)."""
        self.requests_list.clear()
        requests = db.get_users_connections(self.id, True)
        self.requests = {value: key for (key, value) in requests.items()}
        self.requests_list.addItems(list(requests.values()))

    def like_movie(self):
        """Handle liking a movie."""
        db.add_user_interest(self.id, self.movie_ids[self.movie_index], True)
        self.display_next_movie()

    def dislike_movie(self):
        """Handle disliking a movie."""
        db.add_user_interest(self.id, self.movie_ids[self.movie_index], False)
        self.display_next_movie()

    def display_next_movie(self):
        """Display the next movie (placeholder)."""
        self.movie_index += 1
        if self.movies is None or len(self.movies) <= self.movie_index:
            movies = db.get_movies_for_user(self.id)
            if movies is None:
                QMessageBox.warning(self, "Swiping", "Error fetching movies, please try again later")
                self.switch_to_main_page()
                return
            self.movies = list(movies.values())
            self.movie_ids = list(movies.keys())
            self.movie_index = 0
        self.movie_title_label.setText(self.movies[self.movie_index]["title"])

        # Load the image to QPixmap from blob
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(self.movies[self.movie_index]["picture"]))
        self.movie_cover_label.setPixmap(pixmap)

        # Format date to German date format
        release_date = datetime.strptime(
            str(self.movies[self.movie_index]["release_date"]), "%Y-%m-%d"
        ).strftime("%d.%m.%Y")
        self.movie_release_date_label.setText(f"Release Date: {release_date}")

        self.movie_genres_label.setText(f"Genres: {self.movies[self.movie_index]['genres']}")

    def view_match(self):
        """Handle viewing a match."""
        selected_items = self.matches_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "No connection selected")
            return

        self.selected_connection = self.connections[selected_items[0].text()]
        matches = db.get_user_matches(self.id, self.selected_connection, 0)
        if matches is None:
            QMessageBox.warning(self, "Matches", "No matches with this user")
            self.switch_to_matches()
            return
        self.matches = list(matches.values())
        self.match_ids = list(matches.keys())
        self.switch_to_match_details()

    def previous_match(self):
        """Handle showing the previous match."""
        self.match_index = max(0, self.match_index - 1)
        self.display_match()

    def next_match(self):
        """Handle showing the next match."""
        self.match_index += 1
        self.display_match()

    def display_match(self):
        """Display the next match"""
        if len(self.matches) <= self.match_index:
            matches = db.get_user_matches(self.id, self.selected_connection, self.match_ids[-1])
            if matches is None:
                QMessageBox.warning(self, "Matches", "No more Matches")
                return
            self.matches += list(matches.values())
            self.match_ids = list(matches.keys())
        self.match_movie_title_label.setText(self.matches[self.match_index]["title"])

        # Load the image to QPixmap from blob
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(self.matches[self.match_index]["picture"]))
        self.match_movie_cover_label.setPixmap(pixmap)

        # Format date to German date format
        release_date = datetime.strptime(
            str(self.matches[self.match_index]["release_date"]), "%Y-%m-%d"
        ).strftime("%d.%m.%Y")
        self.match_movie_release_date_label.setText(f"Release Date: {release_date}")

        self.match_movie_genres_label.setText(f"Genres: {self.matches[self.match_index]['genres']}")


if __name__ == "__main__":
    db = Database()
    app = QApplication(sys.argv)
    window = MovieTinder()
    window.show()
    sys.exit(app.exec())
