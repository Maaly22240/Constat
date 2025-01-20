import sqlite3
import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'constat.db')
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS accidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER,
                location TEXT,
                description TEXT,
                participants TEXT,
                photos TEXT,
                sketch TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def save_accident(self, accident_data):
        query = '''
            INSERT INTO accidents 
            (timestamp, location, description, participants, photos, sketch, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        values = (
            int(datetime.now().timestamp()),
            accident_data.get('location'),
            accident_data.get('description'),
            json.dumps(accident_data.get('participants', [])),
            json.dumps(accident_data.get('photos', [])),
            accident_data.get('sketch'),
            'draft'
        )
        cursor = self.conn.execute(query, values)
        self.conn.commit()
        return cursor.lastrowid

    def get_accident(self, accident_id):
        cursor = self.conn.execute('SELECT * FROM accidents WHERE id = ?', (accident_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_dict(row)
        return None

    def get_all_accidents(self):
        cursor = self.conn.execute('SELECT * FROM accidents ORDER BY timestamp DESC')
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def _row_to_dict(self, row):
        return {
            'id': row[0],
            'timestamp': row[1],
            'location': row[2],
            'description': row[3],
            'participants': json.loads(row[4]),
            'photos': json.loads(row[5]),
            'sketch': row[6],
            'status': row[7]
        }
