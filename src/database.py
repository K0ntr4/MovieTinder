import mysql.connector
from base import get_db_config
from api import ApiWrapper

api = ApiWrapper()


class Database:
    """
    A class to represent the database operations.
    """

    def __init__(self):
        """
        Initialize the Database instance and open a connection.
        """
        self.connection = None
        self.__open_connection()

    def __open_connection(self):
        """
        Open a connection to the database using configuration from a JSON file.
        """
        data = get_db_config()
        self.connection = mysql.connector.connect(
            host=data['Host'],
            user=data['Username'],
            password=data['Password'],
            database=data['Database'],
            autocommit=True
        )

    def __save(self, table, columns, values, row_id_to_update=-1):
        """
        Save data to the specified table by either inserting or updating a row.

        Args:
            table (str): The name of the table.
            columns (list): List of column names.
            values (list): List of values corresponding to the columns.
            row_id_to_update (int): ID of the row to update. If -1, a new row will be inserted.

        Returns:
            str or bool: Message indicating unequal parameters or the result of the insert/update operation.
        """
        if len(columns) != len(values):
            return 'unequal amount of parameters'

        if row_id_to_update <= 0:
            return self.__insert(table, columns, values)
        else:
            return self.__update(row_id_to_update, table, columns, values)

    def __update(self, row_id, table, columns, values):
        """
        Update a row in the specified table.

        Args:
            row_id (int): ID of the row to update.
            table (str): The name of the table.
            columns (list): List of column names.
            values (list): List of values corresponding to the columns.
        """
        set_columns = ', '.join([f"{columns[i]} = %s" for i in range(len(columns))])
        sql_command = f'UPDATE {table} SET {set_columns} WHERE id = %s'

        cur = self.connection.cursor()
        cur.execute(sql_command, values + [row_id])
        # self.connection.commit()
        return True

    def __insert(self, table, columns, values):
        """
        Insert a new row into the specified table.

        Args:
            table (str): The name of the table.
            columns (list): List of column names.
            values (list): List of values corresponding to the columns.

        Returns:
            bool: True if the insert was successful, False otherwise.
        """
        columns_string = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(values))
        sql_command = f'INSERT INTO {table} ({columns_string}) VALUES ({placeholders})'

        cur = self.connection.cursor()
        try:
            cur.execute(sql_command, values)
        except mysql.connector.errors.IntegrityError:
            return False
        # self.connection.commit()
        return True

    def try_login(self, email, password):
        """
        Attempt to log in a user by verifying the email and password.

        Args:
            email (str): The user's email.
            password (str): The user's hashed password.

        Returns:
            int: The user's ID if login is successful, -1 otherwise.
        """
        sql_command = "SELECT id, password FROM users WHERE email = %s"

        cur = self.connection.cursor()
        cur.execute(sql_command, (email,))
        res = cur.fetchone()

        if res is not None and res[1] == password:
            return res[0]
        return -1

    def sign_up(self, email, password):
        """
        Sign up a new user by inserting their email and hashed password into the database.

        Args:
            email (str): The user's email.
            password (str): The user's hashed password.

        Returns:
            bool: True if sign up was successful, False otherwise.
        """
        return self.__insert('users', ['email', 'password'], [email, password])

    def is_connection_in_usage(self, id_sender, id_receiver):
        """
        Check if a connection between the sender and receiver already exists.

        Args:
            id_sender (int): The ID of the sender.
            id_receiver (int): The ID of the receiver.

        Returns:
            bool: True if a connection exists, False otherwise.
        """
        sql_command = """
            SELECT id 
            FROM connections 
            WHERE (user1=%s AND user2=%s) OR (user1=%s AND user2=%s)
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (id_sender, id_receiver, id_receiver, id_sender))
        result = cursor.fetchone()
        return result is not None

    def create_connection_request(self, userid1, email_receiver):
        """
        Create a connection request from userid1 to the user with email_receiver.

        Args:
            userid1 (int): The ID of the sender.
            email_receiver (str): The email of the receiver.

        Returns:
            bool: True if the connection request was created, False otherwise.
        """
        # Retrieve the ID of the receiver based on their email
        sql_command = "SELECT id FROM users WHERE email = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (email_receiver,))
        result = cursor.fetchone()

        if result is None or result[0] == userid1:
            return False

        # Check if the connection already exists
        if self.is_connection_in_usage(userid1, result[0]):
            return False

        # Save the new connection request
        return self.__save('connections', ['user1', 'user2'], [userid1, result[0]])

    def get_users_connections(self, user_id, pending=False):
        """
        Retrieve all connections for a user.

        Args:
            user_id (int): The ID of the user.
            pending (bool): Whether to retrieve pending connections. Defaults to False.

        Returns:
            dict: A dictionary of connection IDs and user emails for the connections.
        """
        sql_command = """
            SELECT 
                connections.id AS connectionid, 
                users.email AS usermail 
            FROM connections 
            JOIN users ON connections.user1 = users.id 
            WHERE connections.user2 = %s AND active = %s
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (user_id, not pending,))
        result = cursor.fetchall()

        if not result:
            return {}

        # Convert the result to a dictionary
        connections = {row[0]: row[1] for row in result}
        return connections

    def accept_connection(self, connection_id):
        """
        Accept a connection request.

        Args:
            connection_id (int): The ID of the connection to be accepted.

        Returns:
            bool: True if the connection was successfully accepted, False otherwise.
        """
        return self.__save('connections', ['active'], [True], connection_id)

    def add_movie_genre_relation(self, movies, last_row_id, row_count):
        """
        Add the relationship between movies and genres in the movie_x_genres table.

        Args:
            movies (list): List of movies fetched from the API.
            last_row_id (int): The ID of the last inserted movie in the movies table.

        Returns:
            bool: True if the relationships were successfully added, False otherwise.
        """
        api_genres = []
        for movie in movies:
            api_genres += movie["genre_ids"]

        # Fetch genre IDs from the database
        sql_command = f"""
            SELECT api_id, id 
            FROM movie_genres 
            WHERE api_id IN ({', '.join(['%s'] * len(api_genres))})
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_command, api_genres)
        result = cursor.fetchall()

        if not result:
            return False

        # Convert result to a dictionary for easy lookup
        result = dict(result)

        # Prepare the values for the insertion into movie_x_genres
        sql_command = """
            INSERT IGNORE INTO movie_x_genres (movie, genre) VALUES (%s, %s)
        """
        values = []
        for i, movie in enumerate(movies):
            for genre in movie["genre_ids"]:
                values.append((last_row_id - row_count + i + 1, result[genre]))

        cursor.executemany(sql_command, values)
        self.connection.commit()

        return True

    def fetch_movie_genres(self):
        """
        Fetch and store movie genres from the API into the movie_genres table.

        Returns:
            bool: True if genres were successfully fetched and stored, False otherwise.
        """
        genres = api.fetch_movie_genres()
        if genres is None:
            return False

        sql_command = """
            INSERT IGNORE INTO movie_genres (api_id, name) VALUES (%s, %s)
        """
        values = [(genre["id"], genre["name"]) for genre in genres]
        cursor = self.connection.cursor()
        cursor.executemany(sql_command, values)
        self.connection.commit()

        return True

    def fetch_new_movies(self, page=345):
        """
        Fetch and store new movies from the API into the movies table,
        and update their genre relations.

        Args:
            page (int, optional): The page number to fetch movies from. Defaults to 345.

        Returns:
            bool: True if movies were successfully fetched and stored, False otherwise.
        """
        movies = api.fetch_movies(page)
        if movies is None:
            return False

        sql_command = """
            INSERT IGNORE INTO movies (api_id, title, release_date, picture, page) VALUES (%s, %s, %s, %s, %s)
        """
        values = [
            (movie["id"], movie["title"], movie["release_date"], api.fetch_image(movie["poster_path"]), page)
            for movie in movies
        ]
        cursor = self.connection.cursor()
        cursor.executemany(sql_command, values)
        last_row_id = cursor.lastrowid
        self.connection.commit()
        row_count = cursor.rowcount

        self.fetch_movie_genres()
        self.add_movie_genre_relation(movies, last_row_id, row_count)

        return True

    def get_movies_for_user(self, user_id, recursive = False):
        """
        Retrieve movies for a user that the user has not interacted with yet.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: A dictionary of movies with their details.
        """
        sql_command = """
            SELECT
                m.id,
                m.title, 
                m.release_date, 
                m.picture,
                GROUP_CONCAT(g.name SEPARATOR ', ') AS genres,
                m.page
            FROM 
                movies m
            LEFT JOIN 
                movie_x_genres mxg ON m.id = mxg.movie
            LEFT JOIN 
                movie_genres g ON mxg.genre = g.id
            WHERE 
                m.id > COALESCE((
                    SELECT 
                        movie 
                    FROM 
                        movie_user_interests 
                    WHERE 
                        user = %s
                    ORDER BY 
                        movie DESC
                    LIMIT 1
                ), 0) 
            GROUP BY 
                m.id
            LIMIT 8;
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (user_id,))
        result = cursor.fetchall()

        if not recursive and not result:
            self.fetch_new_movies()
            return self.get_movies_for_user(user_id, True)
        elif not result:
            return None

        # If less than 5 movies are fetched, fetch more movies from the api
        if len(result) < 5:
            self.fetch_new_movies(result[0][5] - 1)

        movies = {
            row[0]: {
                "title": row[1],
                "release_date": row[2],
                "picture": row[3],
                "genres": row[4]
            }
            for row in result
        }
        return movies

    def add_user_interest(self, user_id, movie_id, is_liked):
        """
        Add a user's interest in a movie to the database.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            is_liked (bool): Whether the user liked the movie (True) or not (False).

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        return self.__save(
            'movie_user_interests',
            ['user', 'movie', 'liked'],
            [user_id, movie_id, is_liked]
        )

    def get_other_user_from_connection(self, user_id, connection_id):
        """
        Retrieve the user ID of the other party in a connection.

        Args:
            user_id (int): The ID of the current user.
            connection_id (int): The ID of the connection.

        Returns:
            int: The ID of the other user in the connection, or -1 if not found.
        """
        sql_command = '''
            SELECT user1, user2
            FROM connections
            WHERE id = %s
        '''
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (connection_id,))
        result = cursor.fetchone()

        if result is None:
            return -1

        # Return the user ID that is not equal to the current user ID
        return result[1] if result[0] == user_id else result[0]

    def get_user_matches(self, user1, connection_id, movie_id=0):
        """
        Retrieve movies liked by both the current user and the other user in a connection.

        Args:
            user1 (int): The ID of the current user.
            connection_id (int): The ID of the connection.
            movie_id (int, optional): The minimum movie ID to start the search from. Defaults to 0.

        Returns:
            dict: A dictionary where keys are movie IDs and values are dictionaries with movie details.
                  Returns None if no matches are found.
        """
        other_user = self.get_other_user_from_connection(user1, connection_id)

        if other_user == -1:
            return None

        sql_command = """
            SELECT 
                md.id, 
                md.title, 
                md.release_date, 
                md.picture, 
                GROUP_CONCAT(g.name SEPARATOR ', ') AS genres
            FROM 
                movie_user_interests m1
            JOIN 
                movie_user_interests m2 ON m1.movie = m2.movie
            JOIN 
                movies md ON m1.movie = md.id
            LEFT JOIN 
                movie_x_genres mxg ON md.id = mxg.movie
            LEFT JOIN 
                movie_genres g ON mxg.genre = g.id
            WHERE 
                m1.user = %s
                AND m2.user = %s
                AND m1.liked = 1
                AND m2.liked = 1
                AND m1.movie > %s
            GROUP BY 
                md.id
            LIMIT 20;
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_command, (user1, other_user, movie_id))
        result = cursor.fetchall()

        if not result:
            return None

        movies = {
            row[0]: {
                "title": row[1],
                "release_date": row[2],
                "picture": row[3],
                "genres": row[4]
            }
            for row in result
        }
        return movies
