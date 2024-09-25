
import sqlite3
from BackEnd import Database
import bcrypt

def add_admin():
    db = Database("C:\\Users\\Lucas\\Desktop\\Gerenciamento_Func-main-caio\\gerenciamento_funcionarios.db")
    
    username = 'admin'
    password = 'masterkey'
    role = 'admin'
    
    # Verificar se o usuário admin já existe
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            # Hash da senha
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
