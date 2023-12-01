import sqlite3



class ContactDatabase:
    def __init__(self, db='contacts.db'):
        self.db = db
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)")

    def _execute(self, query, parameters=()):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()

    def create_record(self, name, phone, email):
        self._execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))

    def read_records(self):
        return self._execute("SELECT * FROM contacts")

    def update_record(self, record_id, name, phone, email):
        self._execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                      (name, phone, email, record_id))

    def delete_record(self, record_id):
        self._execute("DELETE FROM contacts WHERE id = ?", (record_id,))
