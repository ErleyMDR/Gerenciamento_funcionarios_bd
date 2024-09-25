import os.path
from FrontEnd import Frontend

Base_Dir = os.path.dirname(__file__)
db_path = os.path.join(Base_Dir, "gerenciamento_funcionarios.db")

if __name__ == "__main__":
    app = Frontend()
    app.run()
