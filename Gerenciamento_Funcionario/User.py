import sqlite3
import tkcalendar
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from BackEnd import Database

class User:
    def __init__(self, user_id):
        from Main import db_path
        self.db = Database(db_path)
        self.user_id = user_id  # ID do usuário para associar à tabela FUNC

        self.root = tk.Tk()
        self.root.title("Painel do Usuário")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor='nw')

        # Frame para Informações Pessoais e Tarefas do Funcionário
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)

        personal_info_frame = tk.LabelFrame(top_frame, text="Informações Pessoais", bg="#f0f0f0", padx=10, pady=10)
        personal_info_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)

        tarefas_frame = tk.LabelFrame(top_frame, text="Suas Tarefas", bg="#f0f0f0", padx=10, pady=10)
        tarefas_frame.grid(row=0, column=1, sticky='nw', padx=10, pady=10)

        # Labels e Entries para Informações Pessoais
        tk.Label(personal_info_frame, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_nome = tk.Entry(personal_info_frame, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_info_frame, text="CPF:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_cpf = tk.Entry(personal_info_frame, width=30)
        self.entry_cpf.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_info_frame, text="Telefone:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_telefone = tk.Entry(personal_info_frame, width=30)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(personal_info_frame, text="Data de Nascimento:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_data_nasc = DateEntry(personal_info_frame, width=27, background='darkblue',
                                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_data_nasc.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Botão de Atualizar Informações Pessoais
        button_update_personal = tk.Button(personal_info_frame, text="Atualizar Informações", command=self.update_personal_info, bg="#4CAF50", fg="white", width=20)
        button_update_personal.grid(row=4, column=0, columnspan=2, pady=10)

        # Tabela de exibição das tarefas
        self.tarefas_tree = ttk.Treeview(tarefas_frame, columns=("ID", "Tarefa"), show="headings")
        self.tarefas_tree.heading("ID", text="ID")
        self.tarefas_tree.heading("Tarefa", text="Tarefa")
        self.tarefas_tree.pack(fill=tk.BOTH, expand=True)

        # Frame para exibir endereços
        endereco_frame = tk.LabelFrame(main_frame, text="Seus Endereços", bg="#f0f0f0", padx=10, pady=10)
        endereco_frame.grid(row=1, column=0, sticky='nw', padx=10, pady=10, columnspan=2)

        self.endereco_tree = ttk.Treeview(endereco_frame, columns=("ID", "Rua", "Cidade", "Estado", "CEP"), show="headings")
        self.endereco_tree.heading("ID", text="ID")
        self.endereco_tree.heading("Rua", text="Rua")
        self.endereco_tree.heading("Cidade", text="Cidade")
        self.endereco_tree.heading("Estado", text="Estado")
        self.endereco_tree.heading("CEP", text="CEP")
        self.endereco_tree.pack(fill=tk.BOTH, expand=True)

        # Botões para operações de CRUD de Endereço
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.grid(row=3, column=0, sticky='nw', padx=10, pady=10)

        button_endereco = tk.Button(buttons_frame, text="Adicionar Endereço", command=self.open_add_endereco_window, bg="#2196F3", fg="white", width=20)
        button_endereco.grid(row=0, column=0, padx=5, pady=5)

        button_update_endereco = tk.Button(buttons_frame, text="Atualizar Endereço", command=self.update_endereco, bg="#2196F3", fg="white", width=20)
        button_update_endereco.grid(row=0, column=1, padx=5, pady=5)

        button_delete_endereco = tk.Button(buttons_frame, text="Deletar Endereço", command=self.delete_endereco, bg="#F44336", fg="white", width=20)
        button_delete_endereco.grid(row=0, column=2, padx=5, pady=5)

        # Botão de Logout
        button_logout = tk.Button(main_frame, text="Logout", command=self.logout, bg="#f44336", fg="white", width=25)
        button_logout.grid(row=4, column=0, pady=20, sticky='w', columnspan=2)

        # Carregar dados ao iniciar
        self.load_personal_info()
        self.load_enderecos()
        self.load_tasks()

        # Executar a janela
        self.root.mainloop()

    # Métodos para CRUD de Informações Pessoais

    def load_personal_info(self):
        id_func = self.get_id_func()
        if id_func:
            pessoal = self.db.get_pessoal_by_id(id_func)
            if pessoal:
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, pessoal[1])
                self.entry_cpf.delete(0, tk.END)
                self.entry_cpf.insert(0, pessoal[2])
                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, pessoal[3] if pessoal[3] else "")
                self.entry_data_nasc.set_date(pessoal[4] if pessoal[4] else "")
        else:
            messagebox.showerror("Erro", "Funcionário associado ao usuário não encontrado.")

    def update_personal_info(self):
        id_func = self.get_id_func()
        if not id_func:
            messagebox.showerror("Erro", "Funcionário associado ao usuário não encontrado.")
            return

        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        telefone = self.entry_telefone.get()
        data_nasc = self.entry_data_nasc.get_date().strftime('%Y-%m-%d')

        # Validação de campos
        if not (nome and cpf):
            messagebox.showerror("Erro", "Por favor, preencha os campos obrigatórios (Nome e CPF).")
            return

        try:
            self.db.update_pessoal(id_func, nome, cpf, telefone, data_nasc)
            messagebox.showinfo("Sucesso", "Informações pessoais atualizadas com sucesso!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao atualizar informações pessoais: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    # Métodos para CRUD de Endereço

    def open_add_endereco_window(self):
        AddEnderecoWindow(self.db, self)

    def load_enderecos(self):
        for row in self.endereco_tree.get_children():
            self.endereco_tree.delete(row)
        id_func = self.get_id_func()
        if id_func:
            enderecos = self.db.get_enderecos_by_user(id_func)
            for endereco in enderecos:
                self.endereco_tree.insert("", "end", values=endereco)
        else:
            messagebox.showerror("Erro", "Funcionário associado ao usuário não encontrado.")

    def get_id_func(self):
        with self.db.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT FUNC.ID
                FROM FUNC
                WHERE FUNC.USER_ID = ?
            """, (self.user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def add_endereco(self, rua, cidade, estado, cep):
        id_func = self.get_id_func()
        if not id_func:
            messagebox.showerror("Erro", "Funcionário associado ao usuário não encontrado.")
            return
        try:
            self.db.add_endereco(id_func, rua, cidade, estado, cep)
            messagebox.showinfo("Sucesso", "Endereço adicionado com sucesso!")
            self.load_enderecos()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao adicionar endereço: {e}")

    def update_endereco(self):
        selected_item = self.endereco_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um endereço para atualizar.")
            return
        endereco_values = self.endereco_tree.item(selected_item, 'values')
        UpdateEnderecoWindow(self.db, self, endereco_values)

    def delete_endereco(self):
        selected_item = self.endereco_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um endereço para deletar.")
            return
        endereco_values = self.endereco_tree.item(selected_item, 'values')
        confirm = messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar o endereço ID {endereco_values[0]}?")
        if confirm:
            try:
                self.db.delete_endereco(endereco_values[0])
                messagebox.showinfo("Sucesso", "Endereço deletado com sucesso!")
                self.load_enderecos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar endereço: {e}")

    # Métodos para CRUD de Tarefas

    def load_tasks(self):
        for row in self.tarefas_tree.get_children():
            self.tarefas_tree.delete(row)
        id_func = self.get_id_func()
        if id_func:
            tarefas = self.db.get_tasks_by_user(id_func)
            for tarefa in tarefas:
                self.tarefas_tree.insert("", "end", values=tarefa)
        else:
            messagebox.showerror("Erro", "Funcionário associado ao usuário não encontrado.")

    # Logout

    def logout(self):
        self.root.destroy()
        from FrontEnd import Frontend
        Frontend().run()

# Janelas de CRUD de Endereço

class AddEnderecoWindow:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.window = tk.Toplevel()
        self.window.title("Adicionar Endereço")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Endereço
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Rua:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_rua = tk.Entry(form_frame, width=30)
        self.entry_rua.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cidade:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_cidade = tk.Entry(form_frame, width=30)
        self.entry_cidade.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Estado:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_estado = tk.Entry(form_frame, width=30)
        self.entry_estado.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CEP:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_cep = tk.Entry(form_frame, width=30)
        self.entry_cep.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Botão de Adicionar
        button_add = tk.Button(self.window, text="Adicionar", command=self.add_endereco, bg="#4CAF50", fg="white", width=20)
        button_add.pack(pady=20)

    def add_endereco(self):
        rua = self.entry_rua.get()
        cidade = self.entry_cidade.get()
        estado = self.entry_estado.get()
        cep = self.entry_cep.get()

        # Validação de campos
        if not (rua and cidade and estado and cep):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            self.user.add_endereco(rua, cidade, estado, cep)
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

class UpdateEnderecoWindow:
    def __init__(self, db, user, endereco_values):
        self.db = db
        self.user = user
        self.endereco_id = endereco_values[0]

        self.window = tk.Toplevel()
        self.window.title("Atualizar Endereço")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f0f0")

        # Formulário de Atualização de Endereço
        form_frame = tk.Frame(self.window, bg="#f0f0f0")
        form_frame.pack(pady=20, padx=20)

        tk.Label(form_frame, text="Rua:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_rua = tk.Entry(form_frame, width=30)
        self.entry_rua.insert(0, endereco_values[1])
        self.entry_rua.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Cidade:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_cidade = tk.Entry(form_frame, width=30)
        self.entry_cidade.insert(0, endereco_values[2])
        self.entry_cidade.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="Estado:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_estado = tk.Entry(form_frame, width=30)
        self.entry_estado.insert(0, endereco_values[3])
        self.entry_estado.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Label(form_frame, text="CEP:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_cep = tk.Entry(form_frame, width=30)
        self.entry_cep.insert(0, endereco_values[4])
        self.entry_cep.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Botão de Atualizar
        button_update = tk.Button(self.window, text="Atualizar", command=self.update_endereco, bg="#FFC107", fg="white", width=20)
        button_update.pack(pady=20)

    def update_endereco(self):
        rua = self.entry_rua.get()
        cidade = self.entry_cidade.get()
        estado = self.entry_estado.get()
        cep = self.entry_cep.get()

        # Validação de campos
        if not (rua and cidade and estado and cep):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            self.db.update_endereco(self.endereco_id, rua, cidade, estado, cep)
            messagebox.showinfo("Sucesso", "Endereço atualizado com sucesso!")
            self.user.load_enderecos()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

# Executar a interface do usuário
if __name__ == "__main__":
    pass
