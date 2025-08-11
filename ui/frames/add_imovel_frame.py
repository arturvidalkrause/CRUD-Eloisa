import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import add_new_imovel

class AddImovelFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(self, text="Detalhamento Geo Imóvel | Adicionar", font=("Poppins", 24, "bold")).pack(pady=20, anchor="w")
        
        self.entry_endereco = self.create_entry("Endereço")
        self.entry_numero = self.create_entry("Número")
        self.entry_complemento = self.create_entry("Complemento")
        self.entry_cep = self.create_entry("CEP")
        self.entry_zona = self.create_entry("Zona")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")

        ctk.CTkButton(button_frame, text="Adicionar", command=self.save_imovel).pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=self.cancel, fg_color="gray").pack(side="left")

    def create_entry(self, placeholder):
        """Função auxiliar para criar um campo de entrada."""
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=400, height=35)
        entry.pack(pady=8, anchor="w")
        return entry

    def save_imovel(self):
        """Coleta os dados, chama a lógica de salvamento e volta para a tabela."""
        data = {
            "Endereço": self.entry_endereco.get(),
            "Número": self.entry_numero.get(),
            "Complemento": self.entry_complemento.get(),
            "CEP": self.entry_cep.get(),
            "Zona": self.entry_zona.get()
        }
        
        if not data["Endereço"] or not data["Número"]:
            messagebox.showerror("Erro", "Os campos 'Endereço' e 'Número' são obrigatórios.")
            return

        result = add_new_imovel(data)
        messagebox.showinfo(result["status"].capitalize(), result["mensagem"])

        if result["status"] == "sucesso":
            self.controller.show_table_view()

    def cancel(self):
        """Simplesmente volta para a visão da tabela."""
        self.controller.show_table_view()