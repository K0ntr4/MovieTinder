import base
import re
import mysql.connector


class Database:

    def __init__(self):
        self.__open_connection()
        return

    def __open_connection(self):
        data = base.getdbconfig()
        self.connection = mysql.connector.connect(
            host=data['Host'],
            user=data['Username'],
            password=data['Password'],
            database=data['Database']
        )
        return

    # def __del__(self):
    #     self.connection.close()
    #     return

    def __save(self, id, tablename, columns, values):
        if (columns.len != values.len):
            return 'unequal amount of parameters'

        if id <= 0:
            return self.__insert(tablename, columns, values)
        else:
            return self.__update(id, tablename, columns, values)

    def __update(self, id, tablename, columns, values):
        temp = []
        for i in range(columns.len):
            temp.append(f"{columns[i]}='{values}'")

        set_columne = ', '.join(temp).rstrip(', ')
        set_columne = re.sub(r", $", '', set_columne)
        sql_command = f'UPDATE {tablename} SET {set_columne} WHERE id={id}'

        cur = self.connection.cursor()
        cur.execute(sql_command, values)
        self.connection.commit()

    def __insert(self, tablename, columns, values):
        names_string = ', '.join(columns).rstrip(', ')
        names_string = re.sub(r", $", '', names_string)

        var = ''
        for x in range(len(values)):
            var += f'%s, '
        var = re.sub(r", $", '', var)

        sql_command = f'INSERT INTO {tablename} ({names_string}) VALUES ({var})'

        print(sql_command)

        cur = self.connection.cursor()
        try:
            cur.execute(sql_command, values)
        except mysql.connector.errors.IntegrityError:
            return False
        self.connection.commit()
        return True

    def try_login(self, email, password):
        cmd = "SELECT id, password FROM users WHERE email = %s"

        cur = self.connection.cursor()
        cur.execute(cmd, (email,))
        res = cur.fetchone()

        if res is not None and res[1] == password:
            return id
        return -1

    def signup(self, email, password):
        return self.__insert('users', ['email, password'], [email, password])
