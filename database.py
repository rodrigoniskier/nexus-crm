import sqlite3
import pandas as pd
from datetime import date

# --- CONEXÃO COM O BANCO ---
def get_connection():
    # O check_same_thread=False é necessário para o Streamlit não reclamar de threads
    return sqlite3.connect("nexus.db", check_same_thread=False)

# --- INICIALIZAÇÃO (CRIA A TABELA SE NÃO EXISTIR) ---
def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Tabela simples mas robusta para negócios
    c.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            status TEXT,
            value REAL,
            entry_date DATE,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- CREATE (CRIAR NOVO NEGÓCIO) ---
def add_deal(company, contact, email, phone, status, value, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO deals (company_name, contact_person, email, phone, status, value, entry_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company, contact, email, phone, status, value, date.today(), notes))
    conn.commit()
    conn.close()

# --- READ (LER TODOS OS DADOS) ---
def view_all_deals():
    conn = get_connection()
    # Pandas lê SQL direto, muito mais prático
    df = pd.read_sql_query("SELECT * FROM deals", conn)
    conn.close()
    return df

# --- UPDATE (ATUALIZAR STATUS) ---
def update_status(deal_id, new_status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE deals SET status = ? WHERE id = ?', (new_status, deal_id))
    conn.commit()
    conn.close()

# --- DELETE (APAGAR REGISTRO) ---
def delete_deal(deal_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM deals WHERE id = ?', (deal_id,))
    conn.commit()
    conn.close()