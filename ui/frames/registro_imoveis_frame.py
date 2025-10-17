import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import add_new_imovel

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


		button_frame = ctk.CTkFrame(self, fg_color="transparent")
		button_frame.pack(pady=20, padx=20, fill="x", anchor="e")

		ctk.CTkButton(button_frame, text="Registrar Imóvel", height=40, command=self.registrar_imovel).pack(side="right", padx=(10, 0))
		ctk.CTkButton(button_frame, text="Limpar Campos", height=40, command=self.limpar_campos, fg_color="gray").pack(side="right")

	def limpar_campos(self):
		"""Limpa todos os campos do formulário."""
		for entry in self.entries.values():
			entry.delete(0, 'end')

	def registrar_imovel(self):
		"""Coleta os dados, salva no Excel e limpa o formulário."""
		data = {}
		for campo, entry in self.entries.items():

			data[campo] = entry.get()


		if not data["Endereço"] or not data["Valor do Aluguel"]:
			messagebox.showerror("Erro de Validação", "Os campos 'Endereço' e 'Valor do Aluguel' são obrigatórios.")
			return

		resultado = add_new_imovel(data)

		if resultado["status"] == "sucesso":
			messagebox.showinfo("Sucesso", resultado["mensagem"])
			self.limpar_campos()
		else:
			messagebox.showerror("Erro", resultado["mensagem"])