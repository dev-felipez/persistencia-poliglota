import sqlite3

def conectar():
    conn = sqlite3.connect("banco.db")
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_cidade(nome, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cidades (nome, estado) VALUES (?, ?)", (nome, estado))
    conn.commit()
    conn.close()

def listar_cidades():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cidades")
    dados = cursor.fetchall()
    conn.close()
    return dados