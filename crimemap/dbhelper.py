import pymysql
import dbconfig


class DBHelper:

    def connect(self, database="crimemap"):
        return pymysql.connect(host="localhost",
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            # The following introduces a deliberate security flaw. See section on SQL injection below
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                print("ADD cursor.execute Done")
                connection.commit()
                print("ADD connection.commit Done")
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                print("Clear cursor.execute Done")
                connection.commit()
                print("Clear connection.commit Done")
        finally:
            connection.close()
