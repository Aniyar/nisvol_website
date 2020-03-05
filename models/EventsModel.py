class EventsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 date VARCHAR(100),
                                 status VARCHAR(15),
                                 name VARCHAR(100),
                                 vol_number INTEGER(3),
                                 content VARCHAR(1000),
                                 city INTEGER(2),
                                 location varchar(100)
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, time, status, name, number, content, city, loc):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO events 
                          (date, status, name, vol_number, content, city, location) 
                          VALUES (?,?,?,?)''''''''''', (time, status, name, number, content, city, loc))
        cursor.close()
        self.connection.commit()

    def get(self, events_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (str(events_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows

    def get_from_city(self, city=None):
        cursor = self.connection.cursor()
        if city:
            cursor.execute("SELECT * FROM events WHERE city = ?", (city,))
        else:
            cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows

    def get_by_status(self, status):
        cursor = self.connection.cursor()
        if status:
            cursor.execute("SELECT * FROM events WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM events")
        rows = cursor.fetchall()
        return rows

    def delete(self, events_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM events WHERE id = ?''', (str(events_id),))
        cursor.close()
        self.connection.commit()
