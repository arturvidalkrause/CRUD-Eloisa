import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import add_new_imovel
from core.itbi_scraper import AutoCompleteITBI

class AddImovelFrame(ctk.CTkFrame):
    def __init__(self, master, controller, app):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.app = app

        ctk.CTkLabel(self, text="Detalhamento Geo Imóvel | Adicionar", font=("Poppins", 24, "bold")).pack(pady=20, anchor="w")

        self.entry_cep = self.create_entry("CEP")
        self.entry_cep.bind("<FocusOut>", self.on_cep_entered)

        self.entry_complemento = self.create_entry("Complemento")
        self.entry_zona = self.create_entry("Zona")
        self.entry_endereco = self.create_entry("Endereço")
        self.entry_numero = self.create_entry("Número")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")

        ctk.CTkButton(button_frame, text="Adicionar", command=self.save_imovel).pack(side="left", padx=(0, 10))
        ctk.CTkButton(button_frame, text="Cancelar", command=self.cancel, fg_color="gray").pack(side="left")

    def create_entry(self, placeholder):
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=400, height=35)
        entry.pack(pady=8, anchor="w")
        return entry

    def on_cep_entered(self, event=None):
        """Quando o CEP é digitado e o campo perde o foco, busca o endereço automaticamente"""
        cep = self.entry_cep.get()
        if len(cep.replace("-", "")) >= 7:
            auto = AutoCompleteITBI(cep)
            data = auto.get_data()
            if data:
                # Preenche os campos com os dados vindos do ViaCEP
                self.entry_endereco.delete(0, "end")
                self.entry_endereco.insert(0, data.get("logradouro", ""))

                self.entry_complemento.delete(0, "end")
                self.entry_complemento.insert(0, data.get("complemento", ""))

                self.entry_zona.delete(0, "end")
                # exemplo: você pode usar bairro como zona
                self.entry_zona.insert(0, data.get("bairro", ""))

                messagebox.showinfo("Sucesso", f"Endereço encontrado: {data.get('logradouro', '')}")
            else:
                messagebox.showerror("Erro", "CEP não encontrado ou inválido")

    def save_imovel(self):
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
        self.controller.show_table_view()