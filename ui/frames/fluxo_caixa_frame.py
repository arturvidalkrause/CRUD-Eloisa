

import customtkinter as ctk
from tkinter import ttk
from core.crud_operations import get_all_contratos

class FluxoCaixaFrame(ctk.CTkFrame):
	def __init__(self, master, app):
		super().__init__(master, fg_color="transparent")
		self.app = app
		

		top_frame = ctk.CTkFrame(self, fg_color="transparent")
		top_frame.pack(fill="x", padx=20, pady=10)
		
		ctk.CTkLabel(top_frame, text="Fluxo de Caixa - Contratos Ativos", font=("Poppins", 24, "bold")).pack(side="left")


		table_frame = ctk.CTkFrame(self, fg_color="transparent")
		table_frame.pack(fill="both", expand=True, padx=20, pady=10)

		self.create_table(table_frame)
		self.load_data_into_table()

	def create_table(self, parent_frame):
		"""Cria e estiliza a tabela Treeview para os contratos."""
		style = ttk.Style()
		style.theme_use("default")
		style.configure("Treeview.Heading", font=("Poppins", 12, "bold"), background="#555555", foreground="white", padding=10)
		style.configure("Treeview", rowheight=30, font=("Poppins", 11), background="white", foreground="black")
		style.map("Treeview", background=[('selected', '#c40000')])
		
		columns = ("ID do Imóvel", "ID do Cliente", "Data de Início", "Data de Fim", "Valor do Aluguel", "Tipo de Contrato")
		self.table = ttk.Treeview(parent_frame, columns=columns, show="headings", style="Treeview")

		for col in columns:
			self.table.heading(col, text=col)
			self.table.column(col, width=150, anchor="w")

		self.table.pack(fill="both", expand=True)

	def load_data_into_table(self):
		"""Busca os dados de contratos e os insere na tabela."""
		for item in self.table.get_children():
			self.table.delete(item)

		contratos_df = get_all_contratos()

		if not contratos_df.empty:
			for index, row in contratos_df.iterrows():

				self.table.insert("", "end", values=(
					row.get("ID do Imóvel", ""),
					row.get("ID do Cliente", ""),
					row.get("Data de Início", ""),
					row.get("Data de Fim", ""),
					row.get("Valor do Aluguel", ""),
					row.get("Tipo de Contrato", "")
				))