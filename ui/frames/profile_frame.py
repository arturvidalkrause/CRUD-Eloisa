import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import get_user_data, update_user_data

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.main_app = master.master

        ctk.CTkLabel(self, text="Meu Perfil", font=("Poppins", 24, "bold")).pack(pady=20, anchor="w")

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=20)

        self.nome_entry = self.create_form_entry(form_frame, "Nome")
        self.sobrenome_entry = self.create_form_entry(form_frame, "Sobrenome completo")
        self.cpf_entry = self.create_form_entry(form_frame, "CPF (travado)")
        self.endereco_entry = self.create_form_entry(form_frame, "Endereço")
        self.complemento_entry = self.create_form_entry(form_frame, "Complemento")
        self.cidade_entry = self.create_form_entry(form_frame, "Cidade/Estado")
        self.email_entry = self.create_form_entry(form_frame, "Email")
        self.senha_entry = self.create_form_entry(form_frame, "Senha", show="*")
        
        self.cpf_entry.configure(state="disabled", fg_color="#EBEBEB")
        self.email_entry.configure(state="disabled", fg_color="#EBEBEB")

        save_button = ctk.CTkButton(self, text="Salvar alterações", command=self.save_changes)
        save_button.pack(pady=30, padx=20, anchor="e")

        self.load_user_info()

    def create_form_entry(self, parent, label_text, show=None):
        """Função auxiliar para criar um par de Label e Entry."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w")
        label.pack(side="left")
        
        entry = ctk.CTkEntry(frame, height=35, fg_color="white", border_width=1, show=show)
        entry.pack(side="left", fill="x", expand=True)
        return entry

    def load_user_info(self):
        """Carrega os dados do usuário logado e preenche os campos."""
        user_email = self.main_app.current_user_email
        user_data = get_user_data(user_email)

        if user_data:
            self.nome_entry.insert(0, user_data.get("Nome", ""))
            self.sobrenome_entry.insert(0, user_data.get("Sobrenome", ""))
            self.cpf_entry.insert(0, user_data.get("CPF", ""))
            self.email_entry.insert(0, user_data.get("Email", ""))
            self.senha_entry.insert(0, user_data.get("Senha", ""))

    def save_changes(self):
        """Coleta os dados e chama a função de atualização."""
        user_email = self.main_app.current_user_email
        
        new_data = {
            "Nome": self.nome_entry.get(),
            "Sobrenome": self.sobrenome_entry.get(),
            "Senha": self.senha_entry.get()
        }

        result = update_user_data(user_email, new_data)

        if result["status"] == "sucesso":
            messagebox.showinfo("Sucesso", result["mensagem"])
        else:
            messagebox.showerror("Erro", result["mensagem"])