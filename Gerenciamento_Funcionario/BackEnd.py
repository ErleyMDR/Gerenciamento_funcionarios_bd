import sqlite3 
import bcrypt


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_employees(self):
        self.cursor.execute("""
            SELECT F.ID, Pe.NOME, Pe.CPF, F.EMAIL, F.SALARIO, F.CARGO, D.NOME
            FROM FUNC AS F JOIN
            PESSOAL AS PE ON F.ID_NOME = Pe.ID JOIN
            DEPARTAMENTO AS D ON F.ID_DEP = D.ID                           
        """)
        return self.cursor.fetchall()

    def add_employee(self, id_pessoal, email, salario, cargo, id_dep, user_id):
        self.cursor.execute("INSERT INTO FUNC (ID_NOME, EMAIL, SALARIO, CARGO, ID_DEP, USER_ID) VALUES (?, ?, ?, ?, ?, ?)", 
                            (id_pessoal, email, salario, cargo, id_dep, user_id))
        self.connection.commit()

    def get_departments(self):
        self.cursor.execute("SELECT * FROM DEPARTAMENTO")
        return self.cursor.fetchall()

    def add_department(self, nome):
        self.cursor.execute("INSERT INTO DEPARTAMENTO (NOME) VALUES (?)", (nome,))
        self.connection.commit()

    def add_user(self, username, password, role):
        self.cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)", (username, password, role))
        self.connection.commit()
        return self.cursor.lastrowid
    
    def delete_employee(self,id_func):
        self.cursor.execute("DELETE FROM FUNC WHERE ID = ?", (id_func,))
        self.connection.commit()
    
    def delete_department(self,id_dep):
        self.cursor.execute("DELETE FROM DEPARTAMENTO WHERE ID = ?",(id_dep,))
        self.connection.commit()
    
    def close(self):
        self.connection.close()

    # ======== CRUD para PESSOAL ========
    def add_pessoal(self, nome, cpf, telefone=None, data_nascimento=None):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PESSOAL (NOME, CPF, TELEFONE, DATA_NASCIMENTO)
                VALUES (?, ?, ?, ?)
            """, (nome, cpf, telefone, data_nascimento))
            conn.commit()
            return cursor.lastrowid

    def get_pessoal_by_id(self, id_pessoal):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, NOME, CPF, TELEFONE, DATA_NASCIMENTO
                FROM PESSOAL
                WHERE ID = ?
            """, (id_pessoal,))
            return cursor.fetchone()

    def update_pessoal(self, id_pessoal, nome, cpf, telefone, data_nascimento):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PESSOAL
                SET NOME = ?, CPF = ?, TELEFONE = ?, DATA_NASCIMENTO = ?
                WHERE ID = ?
            """, (nome, cpf, telefone, data_nascimento, id_pessoal))
            conn.commit()
            
    def delete_pessoal(self, id_pessoal):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM FUNC WHERE ID_NOME = ?", (id_pessoal,))
            cursor.execute("DELETE FROM PESSOAL WHERE ID = ?", (id_pessoal,))
            conn.commit()

    # ======== CRUD para ENDERECO ========
    def add_endereco(self, id_func, rua, cidade, estado, cep):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ENDERECO (ID_FUNC, RUA, CIDADE, ESTADO, CEP)
                VALUES (?, ?, ?, ?, ?)
            """, (id_func, rua, cidade, estado, cep))
            conn.commit()
            return cursor.lastrowid

    def get_enderecos_by_user(self, id_func):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, RUA, CIDADE, ESTADO, CEP
                FROM ENDERECO
                WHERE ID_FUNC = ?
            """, (id_func,))
            return cursor.fetchall()

    def update_endereco(self, id_endereco, rua, cidade, estado, cep):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ENDERECO
                SET RUA = ?, CIDADE = ?, ESTADO = ?, CEP = ?
                WHERE ID = ?
            """, (rua, cidade, estado, cep, id_endereco))
            conn.commit()

    def delete_endereco(self, id_endereco):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ENDERECO WHERE ID = ?", (id_endereco,))
            conn.commit()

    # ======== CRUD para TAREFAS ========
    def add_task(self, tarefa, idfunc):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TAREFAS (TAREFA, IDFUNC) VALUES (?, ?)", 
                           (tarefa, idfunc))
            conn.commit()
            return cursor.lastrowid

    def get_tasks(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TAREFAS")
            return cursor.fetchall()
        
    def get_tasks_by_user(self,id_func):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, TAREFA FROM TAREFAS WHERE IDFUNC = ?
            """, (id_func,))
            conn.commit()
            return cursor.fetchall()

    def update_task(self, id_tarefa, tarefa, idfunc):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE TAREFAS 
                SET TAREFA = ?, IDFUNC = ? 
                WHERE ID = ?
            """, (tarefa, idfunc, id_tarefa))
            conn.commit()

    def delete_task(self, id_tarefa):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TAREFAS WHERE ID = ?", (id_tarefa,))
            conn.commit()

    # ======== CRUD para PROJETOS ========
    def add_project(self, nome, cliente):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PROJETO (NOME, CLIENTE)
                VALUES (?, ?)
            """, (nome, cliente))
            conn.commit()
            return cursor.lastrowid

    def get_projects(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PROJETO")
            return cursor.fetchall()

    def update_project(self, id_projeto, nome, cliente, cargo):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PROJETO
                SET NOME = ?, CLIENTE = ?, CARGO = ?
                WHERE ID = ?
            """, (nome, cliente, cargo, id_projeto))
            conn.commit()

    def delete_project(self, id_projeto):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PROJETO WHERE ID = ?", (id_projeto,))
            conn.commit()

    # ======== Método de Verificação de Usuário ========
    def verify_user(self, username, password):
        with self.connection as conn:
            self.cursor.execute("SELECT PASSWORD, ROLE, ID FROM USERS WHERE USERNAME = ?", (username,))
            result = self.cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]): 
                return result[1], result[2]  
            return None, None

    # ======== Método de Verificação de Usuário ADMIN ========
    def create_default_admin(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", ('admin',))
            admin_exists = cursor.fetchone()

        if not admin_exists:
            hashed_password = bcrypt.hashpw('masterkey'.encode('utf-8'), bcrypt.gensalt())
            try:
                cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE) VALUES (?, ?, ?)",
                               ('admin', hashed_password, 'admin'))
                conn.commit()
                print("Usuário admin padrão criado com sucesso!")
            except sqlite3.IntegrityError as e:
                print(f"Erro ao criar usuário admin: {e}")
