class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def get_connection(self):
        return self.connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             email VARCHAR(50),
                             password_hash VARCHAR(256),
                             surname VARCHAR(20),
                             name VARCHAR(20),
                             fname VARCHAR(20),
                             birthdate VARCHAR(100),
                             city INTEGER (2),
                             school INTEGER(2),
                             doc_id VARCHAR(12),
                             img VARCHAR(128)
                             )''')
        # cursor.close()
        self.connection.commit()

    def insert(self, email, password_hash, surname, name, fname, date, city, school, doc_id, img="banner.jpg"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (email, password_hash, surname, name, fname, birthdate, city, school, doc_id, img) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''''''''''''''''''''', (email, password_hash, surname, name, fname, date,
                                                                        city, school, doc_id, img))
        # cursor.close()
        self.connection.commit()

    def get_email(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE id = ?", (id, ))
        row = cursor.fetchone()
        return row[0]

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, email, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?",
                       (email, password_hash))
        row = cursor.fetchone()
        return True if row else False

    def change_avatar(self, uname, img):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users 
                            SET img = ?
                            WHERE user_name = ?;''', (img, uname))
        # cursor.close()
        self.connection.commit()

    def get_avatar(self, uname):
        cursor = self.connection.cursor()
        cursor.execute("SELECT img FROM users WHERE user_name = ?",
                       (uname, ))
        row = cursor.fetchone()
        if row:
            print(row[0])
        return row[0]