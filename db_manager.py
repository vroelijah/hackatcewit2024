import sqlite3
import os 
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()

db = os.getenv('DATABASE')

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):

    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                patient_name TEXT,
                room_number TEXT, 
                attending_person_name TEXT,
                audio_id TEXT,
                audio_label TEXT,
                send_timestamp DATETIME,
                reply_timestamp DATETIME,
                admin_comments TEXT,
                message_id INTEGER
            )
        ''')
    except Error as e:
        print(e)

def insert_patient(conn, patient):
    sql = '''INSERT INTO patients(patient_name, room_number, send_timestamp, message_id)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, patient)
    conn.commit()
    return cur.lastrowid

def update_reply_timestamp(conn, message_id, reply_timestamp):
    sql = ''' UPDATE patients
              SET reply_timestamp = ?
              WHERE message_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (reply_timestamp, message_id))
    conn.commit()


conn = create_connection()
create_table(conn)