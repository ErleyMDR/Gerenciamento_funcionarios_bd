import tkinter as tk
import sqlite3
import bcrypt
from tkinter import messagebox, ttk
from BackEnd import Database



class Admin:
    def __init__(self):
        from Main import db_path
        self.db = Database(db_path)
        self.root = tk.Tk()
        self.root.title("Tela de Administração")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        
        frame_menu = tk.Frame(self.root, bg="#273b7a")
        frame_menu.pack(side="left", fill="y") 

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  

        # Frame para exibir a tabela no topo
        table_frame = tk.Frame(main_frame, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabela de Funcionários
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nome", "CPF", "Email", "Salário", "Cargo", "Departamento"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salário", text="Salário")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Departamento", text="Departamento")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame para os botões no meio
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=20)

        # Coluna de Adicionar
        button_user = tk.Button(buttons_frame, text="Adicionar Funcionário", command=self.open_add_user_window, bg="#339194", fg="white", width=25)
        button_user.grid(row=0, column=0, padx=5, pady=5)

        button_department = tk.Button(buttons_frame, text="Adicionar Departamento", command=self.open_add_department_window, bg="#339194", fg="white", width=25)
        button_department.grid(row=1, column=0, padx=5, pady=5)

        button_project = tk.Button(buttons_frame, text="Adicionar Projeto", command=self.open_add_project_window, bg="#339194", fg="white", width=25)
        button_project.grid(row=2, column=0, padx=5, pady=5)

        button_task = tk.Button(buttons_frame, text="Adicionar Tarefa", command=self.open_add_task_window, bg="#339194", fg="white", width=25)
        button_task.grid(row=3, column=0, padx=5, pady=5)

        # Coluna de Visualizar
        button_view_func = tk.Button(buttons_frame, text="Visualizar Funcionários", command=self.view_employees, bg="#f10c49", fg="white", width=25)
        button_view_func.grid(row=0, column=1, padx=5, pady=5)
        
        button_view_departments = tk.Button(buttons_frame, text="Visualizar Departamentos", command=self.view_departments, bg="#f10c49", fg="white", width=25)
        button_view_departments.grid(row=1, column=1, padx=5, pady=5)

        button_view_projects = tk.Button(buttons_frame, text="Visualizar Projetos", command=self.view_projects, bg="#f10c49", fg="white", width=25)
        button_view_projects.grid(row=2, column=1, padx=5, pady=5)
        
        button_view_tasks = tk.Button(buttons_frame, text="Visualizar Tarefas", command=self.view_tasks, bg="#f10c49", fg="white", width=25)
        button_view_tasks.grid(row=3, column=1, padx=5, pady=5)

        # Coluna de Deletar
        button_delete_employee = tk.Button(buttons_frame, text="Deletar Funcionário", command=self.delete_employee, bg="#f44336", fg="white", width=25)
        button_delete_employee.grid(row=0, column=2, padx=5, pady=5)

        button_delete_department = tk.Button(buttons_frame, text="Deletar Departamento", command=self.delete_department, bg="#f44336", fg="white", width=25)
        button_delete_department.grid(row=1, column=2, padx=5, pady=5)

        button_delete_project = tk.Button(buttons_frame, text="Deletar Projeto", command=self.delete_project, bg="#f44336", fg="white", width=25)
        button_delete_project.grid(row=2, column=2, padx=5, pady=5)

        button_delete_task = tk.Button(buttons_frame, text="Deletar Tarefa", command=self.delete_task, bg="#f44336", fg="white", width=25)
        button_delete_task.grid(row=3, column=2, padx=5, pady=5)


        # Botão de Logout no canto inferior esquerdo
        button_logout = tk.Button(main_frame, text="Logout", command=self.logout, bg="#f44336", fg="white", width=25)
        button_logout.pack(side=tk.LEFT, anchor=tk.SW, pady=20)

        # Carregar dados ao iniciar
        self.load_employees()

        # Executar a janela
        self.root.mainloop()

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        employees = self.db.get_employees()
        for emp in employees:
            self.tree.insert("", "end", values=emp)

    def refresh_data(self):
        self.load_employees()

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
            return

        employee_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirmar Deleção", f"Você tem certeza que deseja deletar:  {employee_id}?")

        if confirm:
            try:
                self.db.delete_employee(employee_id)
                self.refresh_data()
                messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar funcionário: {e}")
                
    def delete_department(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
            return

        department_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirmar Deleção", f"Você tem certeza que deseja deletar:  {department_id}?")

        if confirm:
            try:
                self.db.delete_department(department_id)
                self.refresh_data()
                messagebox.showinfo("Sucesso", "Deletado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar : {e}")

    def delete_project(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
            return

        project_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirmar Deleção", f"Você tem certeza que deseja deletar:  {project_id}?")

        if confirm:
            try:
                self.db.delete_project(project_id)
                self.refresh_data()
                messagebox.showinfo("Sucesso", "Deletado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar : {e}")
    
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
            return

        task_id = self.tree.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirmar Deleção", f"Você tem certeza que deseja deletar:  {task_id}?")

        if confirm:
            try:
                self.db.delete_task(task_id)
                self.refresh_data()
                messagebox.showinfo("Sucesso", "Deletado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar : {e}")
                
    

    def open_add_user_window(self):
        AddUserWindow(self.db, self)
        
    def open_add_employee_window(self):
        AddEmployeeWindow(self.db,)

    def open_add_department_window(self):
        AddDepartmentWindow(self.db, self)

    def open_add_project_window(self):
        AddProjectWindow(self.db, self)

    def open_add_task_window(self):
        AddTaskWindow(self.db, self)

    def view_departments(self):
        departments = self.db.get_departments()
        self.display_data(departments, ["ID", "Nome"])
        
    def view_employees(self):
        funcionarios = self.db.get_employees()
        self.display_data(funcionarios, ["ID","Nome","CPF","Email","Salário","Cargo","Departamento"])

    def view_tasks(self):
        tasks = self.db.get_tasks()
        self.display_data(tasks, ["ID", "Nome", "Descrição"])

    def view_projects(self):
        projects = self.db.get_projects()
        self.display_data(projects, ["ID", "Nome", "Cliente"])

    def display_data(self, data, columns):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)

        for item in data:
            self.tree.insert("", "end", values=item)

    def logout(self):
        self.root.destroy()
        from FrontEnd import Frontend
        Frontend().run()

# Janelas de CRUD

class AddEmployeeWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Funcionário")
        self.window.geometry("400x400")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Funcionário
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CPF:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_cpf = tk.Entry(form_frame, width=30)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Email:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, width=30)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Salário:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_salario = tk.Entry(form_frame, width=30)
        self.entry_salario.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cargo:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_cargo = tk.Entry(form_frame, width=30)
        self.entry_cargo.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Departamento:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_departamento = tk.Entry(form_frame, width=30)
        self.entry_departamento.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Botão para salvar funcionário
        button_add = tk.Button(form_frame, text="Adicionar", command=self.add_employee, bg="#4CAF50", fg="white")
        button_add.grid(row=6, columnspan=2, pady=20)

    def add_employee(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        salario = self.entry_salario.get()
        cargo = self.entry_cargo.get()
        departamento = self.entry_departamento.get()

        try:
            self.db.add_employee(nome, cpf, email, salario, cargo, departamento)
            self.admin.refresh_data()
            self.window.destroy()
            messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar funcionário: {e}")


class AddUserWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Cadastrar Usuário e Funcionário")
        self.window.geometry("400x500") 
        self.window.configure(bg="#f0f0f0")

        # Formulário de Usuário e Funcionário
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        # Campos de Usuário
        tk.Label(form_frame, text="Usuário:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_username = tk.Entry(form_frame, width=30)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Senha:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_password = tk.Entry(form_frame, show="*", width=30)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Papel:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_role = tk.Entry(form_frame, width=30)
        self.entry_role.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Campos de Funcionário
        tk.Label(form_frame, text="Nome:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CPF:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_cpf = tk.Entry(form_frame, width=30)
        self.entry_cpf.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Email:", bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_email = tk.Entry(form_frame, width=30)
        self.entry_email.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Salário:", bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=10, sticky='e')
        self.entry_salario = tk.Entry(form_frame, width=30)
        self.entry_salario.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cargo:", bg="#f0f0f0").grid(row=7, column=0, padx=10, pady=10, sticky='e')
        self.entry_cargo = tk.Entry(form_frame, width=30)
        self.entry_cargo.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Departamento ID :", bg="#f0f0f0").grid(row=8, column=0, padx=10, pady=10, sticky='e')
        self.entry_id_dep = tk.Entry(form_frame, width=30)
        self.entry_id_dep.grid(row=8, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add_user = tk.Button(self.window, text="Cadastrar", command=self.add_user, bg="#4CAF50", fg="white", width=20)
        button_add_user.pack(pady=20)
        

    def add_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        role = self.entry_role.get()
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        email = self.entry_email.get()
        salario = self.entry_salario.get()
        cargo = self.entry_cargo.get()
        id_dep = self.entry_id_dep.get()

        # Validação de campos
        if not (username and password and role and nome and cpf and email and salario and cargo):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        if role not in ['admin', 'user']:
            messagebox.showerror("Erro", "Papel deve ser 'admin' ou 'user'.")
            return

        try:
            salario = float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número.")
            return

        id_dep = id_dep if id_dep else None

        try:
            # Adicionar usuário
            user_id = self.db.add_user(username, hashed_password, role)
            # Adicionar pessoal
            id_pessoal = self.db.add_pessoal(nome, cpf, telefone=None, data_nascimento=None)
            # Adicionar funcionário, associando ao usuário e pessoal
            self.db.add_employee(id_pessoal, email, salario, cargo, id_dep, user_id)
            messagebox.showinfo("Sucesso", "Usuário e Funcionário adicionados com sucesso!")
            self.window.destroy()
            self.admin.refresh_data()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário ou funcionário: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")


class AddDepartmentWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Departamento")
        self.window.geometry("400x200")
        self.window.configure(bg="#f0f0f0")

        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome do Departamento:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        button_add = tk.Button(form_frame, text="Adicionar", command=self.add_department, bg="#4CAF50", fg="white")
        button_add.grid(row=1, columnspan=2, pady=20)

    def add_department(self):
        nome = self.entry_nome.get()
        try:
            self.db.add_department(nome)
            self.admin.refresh_data()
            self.window.destroy()
            messagebox.showinfo("Sucesso", "Departamento adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar departamento: {e}")


class AddProjectWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Projeto")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f0f0")

        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome do Projeto:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cliente:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_cliente = tk.Entry(form_frame, width=30)
        self.entry_cliente.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        button_add = tk.Button(form_frame, text="Adicionar", command=self.add_project, bg="#4CAF50", fg="white")
        button_add.grid(row=2, columnspan=2, pady=20)

    def add_project(self):
        nome = self.entry_nome.get()
        cliente = self.entry_cliente.get()
        try:
            self.db.add_project(nome, cliente)
            self.admin.refresh_data()
            self.window.destroy()
            messagebox.showinfo("Sucesso", "Projeto adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar projeto: {e}")


class AddTaskWindow:
    def __init__(self, db, admin):
        self.db = db
        self.admin = admin
        self.window = tk.Toplevel()
        self.window.title("Adicionar Tarefa")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f0f0")

        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Nome da Tarefa:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nome = tk.Entry(form_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Descrição:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_descricao = tk.Entry(form_frame, width=30)
        self.entry_descricao.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        button_add = tk.Button(form_frame, text="Adicionar", command=self.add_task, bg="#4CAF50", fg="white")
        button_add.grid(row=2, columnspan=2, pady=20)

    def add_task(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        try:
            self.db.add_task(nome, descricao)
            self.admin.refresh_data()
            self.window.destroy()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {e}")


if __name__ == "__main__":
    Admin()
