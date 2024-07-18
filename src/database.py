import mysql.connector
from src.base import get_db_config


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
            database=data['Database']
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
        self.connection.commit()
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
        self.connection.commit()
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

    def is_connection_in_usage(self, id_sender, id_reciever):
        sql_command = "SELECT id FROM connections WHERE (user1=%s AND user2=%s) OR (user1=%s AND user2=%s)"
        cur = self.connection.cursor()
        cur.execute(sql_command, (id_sender, id_reciever, id_reciever, id_sender))
        res = cur.fetchone()
        if res is not None:
            return True
        return False

    def create_connection_request(self, userid1, email_reciever):
        sql_command = "SELECT id FROM users WHERE email = %s"
        cur = self.connection.cursor()
        cur.execute(sql_command, (email_reciever,))
        res = cur.fetchone()
        
        if res is None:
            return False
        if self.is_connection_in_usage(userid1, res[0]):
            return False

        return self.__save('connections', ['user1', 'user2'], [userid1, res[0]])

    def get_users_pending_requests(self, id):
        sql_command= (
            'SELECT '
            'connections.id AS connectionid, '
            'users.email AS usermail '
            'FROM connections '
            'JOIN users ON connections.user1=users.id '
            'WHERE connections.user2=%s AND active=false'
        )

        cur = self.connection.cursor()
        cur.execute(sql_command, (id,))
        res = cur.fetchall()

        if res is None:
            return False
        
        dic = dict(res)
        return dic

    def accept_connection(self, id):
        return self.__save('connections', ['active'], [True], id)
    