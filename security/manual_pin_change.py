import sqlite3
from datetime import datetime

DB = 'users.db'

def registrar_solicitud(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO solicitudes_pin (user_id, fecha) VALUES (?, ?)", (user_id, datetime.now()))
    conn.commit()
    conn.close()

def listar_solicitudes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM solicitudes_pin")
    data = c.fetchall()
    conn.close()
    return data

def marcar_como_atendida(solicitud_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE solicitudes_pin SET atendida = 1 WHERE id = ?", (solicitud_id,))
    conn.commit()
    updated = c.rowcount
    conn.close()
    return updated > 0