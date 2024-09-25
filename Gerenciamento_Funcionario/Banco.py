import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("C:\\Users\\Lucas\\Desktop\\Gerenciamento_Func-main-caio\\gerenciamento_funcionarios.db")

# Criar um cursor
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS PESSOAL (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT NOT NULL,
        CPF TEXT NOT NULL UNIQUE,
        TELEFONE TEXT,
        DATA_NASCIMENTO TEXT
    );
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ENDERECO (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_FUNC INTEGER NOT NULL,
    RUA TEXT NOT NULL,
    CIDADE TEXT NOT NULL,
    ESTADO TEXT NOT NULL,
    CEP TEXT NOT NULL,
    FOREIGN KEY (ID_FUNC) REFERENCES FUNC(ID)
);
        """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DEPARTAMENTO (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT NOT NULL UNIQUE
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FUNC (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_NOME INTEGER NOT NULL,
        EMAIL TEXT NOT NULL ,
        SALARIO REAL NOT NULL,
        CARGO TEXT NOT NULL,
        ID_DEP INTEGER NOT NULL,
        USER_ID INTEGER NOT NULL ,
        FOREIGN KEY (ID_NOME) REFERENCES PESSOAL(ID),
        FOREIGN KEY (ID_DEP) REFERENCES DEPARTAMENTO(ID),
        FOREIGN KEY (USER_ID) REFERENCES USERS(ID)
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL ,
        PASSWORD TEXT NOT NULL,
        ROLE TEXT NOT NULL CHECK(ROLE IN ('admin', 'user'))
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PROJETO (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT NOT NULL,
        CLIENTE TEXT NOT NULL,
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TAREFAS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TAREFA TEXT NOT NULL,
        IDFUNC INTEGER NOT NULL,
        FOREIGN KEY (IDFUNC) REFERENCES FUNC(ID)
    );
""")



# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()


