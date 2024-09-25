import os.path
import sqlite3
from BackEnd import Database
import bcrypt

Base_Dir = os.path.dirname(__file__)
db_path = os.path.join(Base_Dir, "gerenciamento_funcionarios.db")

def add_admin():
    db = Database(db_path)
    
    username = 'admin'
    password = 'masterkey'
    role = 'admin'
        
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            try:
                cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)", 
                               (username, hashed_password, role))
                conn.commit()
                print("Usuário admin criado com sucesso!")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao criar usuário admin: {e}")
        else:
            print("Usuário admin já existe.")

if __name__ == "__main__":
    add_admin()
