import tkinter as tk
from tkinter import messagebox
from BackEnd import Database
from Admin import Admin
from User import User

class Frontend:
    def __init__(self): 
        self.db = Database("C:\\Users\\Lucas\\Desktop\\Gerenciamento_Func-main-caio\\gerenciamento_funcionarios.db")
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("800x400")
        self.window.configure(bg="#f0f0f0")  # Cor de fundo

        # Frame principal alinhado à esquerda
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50, anchor='nw')

        # Título
        tk.Label(main_frame, text="Sistema de Login", font=("Arial", 24), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=20, sticky='w')

        # Campo de Usuário
        tk.Label(main_frame, text="Usuário:", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_username = tk.Entry(main_frame, font=("Arial", 14), width=30)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Campo de Senha
        tk.Label(main_frame, text="Senha:", font=("Arial", 14), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_password = tk.Entry(main_frame, show="*", font=("Arial", 14), width=30)
        self.entry_password.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Botão de Login
        button_login = tk.Button(main_frame, text="Entrar", command=self.verify_user, bg="#4CAF50", fg="white", font=("Arial", 14), width=20)
        button_login.grid(row=3, column=0, columnspan=2, pady=20, sticky='w')

        # Rodapé
        tk.Label(main_frame, text="Sistema de Gerenciamento", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, columnspan=2, pady=20, sticky='w')

    def verify_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role, user_id = self.db.verify_user(username, password)

        if role:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {username}!")
            self.window.destroy()
            if role == 'admin':
                Admin()
            elif role == 'user':
                User(user_id)
            else:
                messagebox.showerror("Erro", "Papel de usuário desconhecido.")
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def run(self):
        self.window.mainloop()

# Executa a aplicação
if __name__ == "__main__":
    app = Frontend()
    app.run()
