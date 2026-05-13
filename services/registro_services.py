# services/registro_service.py
import sqlite3
import pandas as pd

DB_PATH = "data/registro.db"

COLUMNAS = [
    "Tipo", "Marca", "Modelo", "Serie",
    "Estado", "Usuario", "IMEI_HOST",
    "LINEA", "LOCALIDAD", "RITM",
    "Accesorios", "FechaRegistro",
    "FechaEntrega", "CapturadoPor"
]


# ---------- CONEXIÓN ----------
import os

def get_connection():
    # Crear carpeta si no existe
    os.makedirs("/data", exist_ok=True)

    return sqlite3.connect("/data/registro.db", check_same_thread=False)

# ---------- INICIALIZAR BD ----------
def inicializar_bd():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Tipo TEXT,
            Marca TEXT,
            Modelo TEXT,
            Serie TEXT UNIQUE,
            Estado TEXT,
            Usuario TEXT,
            IMEI_HOST TEXT,
            LINEA TEXT,
            LOCALIDAD TEXT,
            RITM TEXT,
            Accesorios TEXT,
            FechaRegistro TEXT,
            FechaEntrega TEXT,
            CapturadoPor TEXT
        )
    """)
    conn.commit()
    conn.close()


# ---------- CARGAR ----------
def cargar_registro():
    inicializar_bd()
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM registros", conn)
    conn.close()
    return df if not df.empty else pd.DataFrame(columns=COLUMNAS)

# ---------- GUARDAR ----------
def guardar_registro(nuevo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registros (
            Tipo, Marca, Modelo, Serie,
            IMEI_HOST, LINEA, LOCALIDAD,
            Estado, Usuario, RITM,
            Accesorios, FechaRegistro,
            FechaEntrega, CapturadoPor
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nuevo.get("Tipo"),
        nuevo.get("Marca"),
        nuevo.get("Modelo"),
        nuevo.get("Serie"),
        nuevo.get("IMEI_HOST"),
        nuevo.get("LINEA"),
        nuevo.get("LOCALIDAD"),
        nuevo.get("Estado"),
        nuevo.get("Usuario"),
        nuevo.get("RITM"),
        nuevo.get("Accesorios"),
        nuevo.get("FechaRegistro"),
        nuevo.get("FechaEntrega"),
        nuevo.get("CapturadoPor"),
    ))

    conn.commit()
    conn.close()

# ---------- VALIDACIONES ----------
def validar_campos(nuevo):
    obligatorios = ["Modelo", "Serie", "Marca", "Tipo", "Estado", "Usuario"]
    return [c for c in obligatorios if not nuevo.get(c)]

def serie_existe(df, serie):
    return serie in df["Serie"].values
def eliminar_registro_por_serie(serie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM registros WHERE Serie = ?",
        (serie,)
    )
    conn.commit()
    conn.close()
