
import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO 'users' ('user_id') VALUES (?)",
                (user_id,)
            )
            self.connection.commit()

    def user_exists(self, user_id) -> bool:
        with self.connection:
            result = self.cursor.execute(
                """SELECT * FROM "users" WHERE "user_id" = ?""",
                (user_id,)
            ).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, user_nickname):
        with self.connection:
            self.cursor.execute(
                '''UPDATE "users" SET "user_nickname" = ? WHERE "user_id" = ?''',
                (user_nickname, user_id,)
            )
            self.connection.commit()

    def set_name(self, user_id, user_name):
        with self.connection:
            self.cursor.execute(
                '''UPDATE "users" SET "user_name" = ? WHERE "user_id" = ?''',
                (user_name, user_id,)
            )
            self.connection.commit()

    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "user_name" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                name = str(row[0])
            return name

    def set_surname(self, user_id, user_surname):
        with self.connection:
            return self.cursor.execute(
                """UPDATE "users" SET "user_surname" = ? WHERE "user_id" = ?""",
                (user_surname, user_id,)
            )

    def get_surname(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "user_name" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                surname = str(row[0])
            return surname

    def set_age(self, user_id, user_age):
        with self.connection:
            return self.cursor.execute(
                """UPDATE "users" SET "user_age" = ? WHERE "user_id" = ?""",
                (user_age, user_id,)
            )

    def get_age(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "user_name" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                age = str(row[0])
            return age

    def set_phone(self, user_id, user_phone):
        with self.connection:
            return self.cursor.execute(
                """UPDATE "users" SET "user_phone" = ? WHERE "user_id" = ?""",
                (user_phone, user_id,)
            )

    def get_phone(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "user_name" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                phone = str(row[0])
            return phone

    def set_email(self, user_id, user_email):
        with self.connection:
            return self.cursor.execute(
                '''UPDATE "users" SET "user_email" = ? WHERE "user_id" = ?''',
                (user_email, user_id,)
            )

    def get_email(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "user_name" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                email = str(row[0])
            return email

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                '''SELECT "sign_up" FROM "users" WHERE "user_id" = ?''',
                (user_id,)
            ).fetchall()
            for row in result:
                sign_up = str(row[0])
            return sign_up

    def set_signup(self, user_id, sign_up):
        with self.connection:
            return self.cursor.execute(
                '''UPDATE "users" SET "sign_up" = ? WHERE "user_id" = ?''',
                (sign_up, user_id)
            )
