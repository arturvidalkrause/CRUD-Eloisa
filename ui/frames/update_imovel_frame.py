import customtkinter as ctk
from tkinter import messagebox
from core.crud_operations import update_imovel_data

class UpdateImovelFrame(ctk.CTkFrame):
	def __init__(self, master, controller, app):
		super().__init__(master, fg_color="transparent")
		self.controller = controller
		self.app = app
		self.original_endereco = None # Armazena o identificador do imovel que esta sendo editado

		ctk.CTkLabel(self, text="Detalhamento Geo Imóvel | Atualizar", font=("Poppins", 24, "bold")).pack(pady=20, anchor="w")
		
		main_form_frame = ctk.CTkFrame(self, fg_color="transparent")
		main_form_frame.pack(fill="x", expand=True)
		main_form_frame.grid_columnconfigure((0, 1), weight=1)

		left_frame = ctk.CTkFrame(main_form_frame, fg_color="transparent")
		left_frame.grid(row=0, column=0, padx=10, sticky="ew")
		
		self.current_endereco = self.create_form_entry(left_frame, "Endereço", state="disabled")
		self.current_numero = self.create_form_entry(left_frame, "Número", state="disabled")
		self.current_complemento = self.create_form_entry(left_frame, "Complemento", state="disabled")
		self.current_cep = self.create_form_entry(left_frame, "CEP", state="disabled")
		self.current_zona = self.create_form_entry(left_frame, "Zona", state="disabled")

		right_frame = ctk.CTkFrame(main_form_frame, fg_color="transparent")
		right_frame.grid(row=0, column=1, padx=10, sticky="ew")

		self.new_endereco = self.create_form_entry(right_frame, "Endereço - Atualizado")
		self.new_numero = self.create_form_entry(right_frame, "Número - Atualizado")
		self.new_complemento = self.create_form_entry(right_frame, "Complemento - Atualizado")
		self.new_cep = self.create_form_entry(right_frame, "CEP - Atualizado")
		self.new_zona = self.create_form_entry(right_frame, "Zona - Atualizado")

		button_frame = ctk.CTkFrame(self, fg_color="transparent")
		button_frame.pack(pady=40, fill="x")
		ctk.CTkButton(button_frame, text="Atualizar", command=self.update_data).pack(side="left", padx=20)
		ctk.CTkButton(button_frame, text="Cancelar", command=self.cancel, fg_color="gray").pack(side="left")

	def create_form_entry(self, parent, placeholder, state="normal"):
		entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300, height=35, state=state, fg_color=("#EBEBEB" if state=="disabled" else "white"))
		entry.pack(pady=8, fill="x", expand=True)
		return entry

	def populate_form(self, imovel_data):
		"""Recebe os dados do imóvel e preenche os campos do formulário."""
		self.original_endereco = imovel_data.get("Endereço")
		
		entries_current = [self.current_endereco, self.current_numero, self.current_complemento, self.current_cep, self.current_zona]
		entries_new = [self.new_endereco, self.new_numero, self.new_complemento, self.new_cep, self.new_zona]
		for entry in entries_current + entries_new:
			entry.delete(0, 'end')

		self.current_endereco.insert(0, imovel_data.get("Endereço", ""))
		self.current_numero.insert(0, imovel_data.get("Número", ""))
		self.current_complemento.insert(0, imovel_data.get("Complemento", ""))
		self.current_cep.insert(0, imovel_data.get("CEP", ""))
		self.current_zona.insert(0, imovel_data.get("Zona/Re", ""))

		self.new_endereco.insert(0, imovel_data.get("Endereço", ""))
		self.new_numero.insert(0, imovel_data.get("Número", ""))
		self.new_complemento.insert(0, imovel_data.get("Complemento", ""))
		self.new_cep.insert(0, imovel_data.get("CEP", ""))
		self.new_zona.insert(0, imovel_data.get("Zona/Re", ""))

	def update_data(self):
		if not self.original_endereco:
			messagebox.showerror("Erro", "Nenhum imóvel selecionado para atualização.")
			return

		new_data = {
			"Endereço": self.new_endereco.get(),
			"Número": self.new_numero.get(),
			"Complemento": self.new_complemento.get(),
			"CEP": self.new_cep.get(),
			"Zona": self.new_zona.get()
		}
		
		result = update_imovel_data(self.original_endereco, new_data)
		messagebox.showinfo(result["status"].capitalize(), result["mensagem"])
		
		if result["status"] == "sucesso":
			self.controller.show_table_view()

	def cancel(self):
		self.controller.show_table_view()