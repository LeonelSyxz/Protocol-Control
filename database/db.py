# database/db.py

import sqlite3
from pathlib import Path

DB_PATH = Path("database/mysqlite.db")

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip TEXT NOT NULL UNIQUE,
        os TEXT,
        direction TEXT DEFAULT 'up',
        status BOOLEAN DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        loop_interval INTEGER DEFAULT 40
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO config (id, loop_interval) VALUES (1, 40)")

    conn.commit()
    conn.close()

def get_tvs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tv")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_tv(name, ip, os, direction, status=True):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tv (name, ip, os, direction, status) VALUES (?, ?, ?, ?, ?)",
                   (name, ip, os, direction, int(status)))
    conn.commit()
    conn.close()

def update_tv(tv_id, name, ip, os, direction, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tv SET name=?, ip=?, os=?, direction=?, status=? WHERE id=?",
                   (name, ip, os, direction, int(status), tv_id))
    conn.commit()
    conn.close()

def delete_tv(tv_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tv WHERE id=?", (tv_id,))
    conn.commit()
    conn.close()

def get_loop_interval():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT loop_interval FROM config WHERE id=1")
    (interval,) = cursor.fetchone()
    conn.close()
    return interval

def update_loop_interval(seconds):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE config SET loop_interval=? WHERE id=1", (seconds,))
    conn.commit()
    conn.close()
