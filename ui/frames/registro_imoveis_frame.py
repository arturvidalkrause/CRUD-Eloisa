import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import add_new_imovel
from core.itbi_scraper import AutoCompleteITBI  # <-- importar a classe

class RegistroImoveisFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        ctk.CTkLabel(self, text="Registro de Imóveis", font=("Poppins", 24, "bold")).pack(pady=20, padx=20, anchor="w")

        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20)

        self.entries = {}

        campos = [
            "Endereço", "Número", "Complemento", "CEP", "Bairro", "Cidade", "Estado",
            "Tipo de Imóvel (Apartamento, Casa...)", "Status (Disponível, Alugado...)",
            "Quartos", "Banheiros", "Vagas Garagem", "Área (m²)",
            "Valor do Aluguel", "Valor do Condomínio", "Valor do IPTU"
        ]

        for campo in campos:
            frame_linha = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            frame_linha.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(frame_linha, text=f"{campo}:", width=200, anchor="w", font=("Poppins", 14))
            label.pack(side="left")
            
            entry = ctk.CTkEntry(frame_linha, height=35, fg_color="white", border_width=1)
            entry.pack(side="left", fill="x", expand=True)
            self.entries[campo] = entry

        self.entries["CEP"].bind("<FocusOut>", self.buscar_por_cep)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x", anchor="e")

        ctk.CTkButton(button_frame, text="Registrar Imóvel", height=40, command=self.registrar_imovel).pack(side="right", padx=(10, 0))
        ctk.CTkButton(button_frame, text="Limpar Campos", height=40, command=self.limpar_campos, fg_color="gray").pack(side="right")

    def buscar_por_cep(self, event=None):
        cep = self.entries["CEP"].get().replace("-", "").strip()
        if len(cep) == 8:
            auto = AutoCompleteITBI(cep)
            data = auto.get_data()
            if data:
                self.entries["Endereço"].delete(0, "end")
                self.entries["Endereço"].insert(0, data.get("logradouro", ""))

                self.entries["Bairro"].delete(0, "end")
                self.entries["Bairro"].insert(0, data.get("bairro", ""))

                self.entries["Cidade"].delete(0, "end")
                self.entries["Cidade"].insert(0, data.get("localidade", ""))

                self.entries["Estado"].delete(0, "end")
                self.entries["Estado"].insert(0, data.get("uf", ""))

                if data.get("complemento"):
                    self.entries["Complemento"].delete(0, "end")
                    self.entries["Complemento"].insert(0, data.get("complemento", ""))

            else:
                messagebox.showerror("Erro", "CEP inválido ou não encontrado.")

    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')

    def registrar_imovel(self):
        data = {campo: entry.get() for campo, entry in self.entries.items()}

        if not data["Endereço"] or not data["Valor do Aluguel"]:
            messagebox.showerror("Erro de Validação", "Os campos 'Endereço' e 'Valor do Aluguel' são obrigatórios.")
            return

        resultado = add_new_imovel(data)

        if resultado["status"] == "sucesso":
            messagebox.showinfo("Sucesso", resultado["mensagem"])
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", resultado["mensagem"])
