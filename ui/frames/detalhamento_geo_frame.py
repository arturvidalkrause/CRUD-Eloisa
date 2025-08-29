import customtkinter as ctk
from tkinter import ttk, messagebox
from core.crud_operations import get_all_imoveis, delete_imoveis_by_endereco, update_imovel_data
from .add_imovel_frame import AddImovelFrame
from .filter_imovel_frame import FilterImovelFrame
from .update_imovel_frame import UpdateImovelFrame

class DetalhamentoGeoFrame(ctk.CTkFrame):
	def __init__(self, master, app):
		super().__init__(master, fg_color="transparent")
		self.app = app
		
		self.main_view = ctk.CTkFrame(self, fg_color="transparent")
		self.main_view.pack(fill="both", expand=True)

		self.table_view = ctk.CTkFrame(self.main_view, fg_color="transparent")
		
		top_frame = ctk.CTkFrame(self.table_view, fg_color="transparent")
		top_frame.pack(fill="x", padx=20, pady=(10, 5))
		ctk.CTkLabel(top_frame, text="Detalhamento Geo Imóvel", font=("Poppins", 24, "bold")).pack(side="left")
		ctk.CTkButton(top_frame, text="Limpar Filtro", command=self.show_table_view, fg_color="gray").pack(side="right", padx=(5, 0))
		ctk.CTkButton(top_frame, text="Adicionar", command=self.show_add_form).pack(side="right", padx=(0, 5))
		ctk.CTkButton(top_frame, text="Filtro", command=self.show_filter_form).pack(side="right", padx=(0, 5))
		
		table_frame = ctk.CTkFrame(self.table_view, fg_color="transparent")
		table_frame.pack(fill="both", expand=True, padx=20, pady=5)
		self.create_table(table_frame)
		
		bottom_frame = ctk.CTkFrame(self.table_view, fg_color="transparent")
		bottom_frame.pack(fill="x", padx=20, pady=10)
		
		self.delete_button = ctk.CTkButton(bottom_frame, text="Deletar Registros", command=self.delete_selected_imoveis)
		self.delete_button.pack(side="left")
		
		self.edit_button = ctk.CTkButton(bottom_frame, text="Editar Selecionado", command=self.open_edit_form, state="disabled")
		self.edit_button.pack(side="left", padx=10)
		
		ctk.CTkLabel(bottom_frame, text="< 1 2 3 >  Configurações avançadas", text_color="#1E90FF").pack(side="right")
		
		
		self.add_view = AddImovelFrame(self.main_view, controller=self, app=self.app)
		self.filter_view = FilterImovelFrame(self.main_view, controller=self, app=self.app)
		self.update_view = UpdateImovelFrame(self.main_view, controller=self, app=self.app)

		self.show_table_view()
	
	def show_view(self, view_to_show):
		for view in [self.table_view, self.add_view, self.filter_view, self.update_view]: view.pack_forget()
		view_to_show.pack(fill="both", expand=True, padx=20)
	def show_table_view(self):
		self.load_data_into_table()
		self.show_view(self.table_view)
	def show_add_form(self): self.show_view(self.add_view)
	def show_filter_form(self): self.show_view(self.filter_view)

	def show_update_form(self, imovel_data):
		"""Preenche o formulário com os dados e depois o exibe."""
		self.update_view.populate_form(imovel_data)
		self.show_view(self.update_view)
	
	def on_table_select(self, event):
		"""Ativa/desativa o botão de editar baseado na seleção."""
		selected_items = self.table.selection()
		if len(selected_items) == 1:
			self.edit_button.configure(state="normal")
		else:
			self.edit_button.configure(state="disabled")

	def open_edit_form(self):
		"""Pega os dados da linha selecionada e abre o formulário de edição."""
		selected_item = self.table.selection()[0]
		item_values = self.table.item(selected_item, "values")
		
		imovel_data = {
			"Endereço": item_values[0],
			"Número": item_values[1],
			"Complemento": item_values[2],
			"CEP": item_values[3],
			"Zona/Re": item_values[4]
		}
		self.show_update_form(imovel_data)

	def create_table(self, parent_frame):
		style = ttk.Style(); style.theme_use("default")
		style.configure("Treeview.Heading", font=("Poppins", 12, "bold"), background="#555555", foreground="white", padding=10)
		style.configure("Treeview", rowheight=30, font=("Poppins", 11), background="white", foreground="black")
		style.map("Treeview", background=[('selected', '#c40000')])
		columns = ("Endereço", "Número", "Complemento", "CEP", "Zona/Re", "Opções")
		self.table = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="extended")
		
		self.table.bind("<<TreeviewSelect>>", self.on_table_select)
		
		for col in columns: self.table.heading(col, text=col)
		self.table.column("Endereço", width=300, anchor="w"); self.table.column("Número", width=80, anchor="center")
		self.table.column("Complemento", width=120, anchor="center"); self.table.column("CEP", width=100, anchor="center")
		self.table.column("Zona/Re", width=120, anchor="w"); self.table.column("Opções", width=80, anchor="center")
		self.table.pack(fill="both", expand=True)

	def load_data_into_table(self, dataframe=None):
		for item in self.table.get_children(): self.table.delete(item)

		if dataframe is None:
			dataframe = get_all_imoveis()

		if not dataframe.empty:
			for index, row in dataframe.iterrows():
				self.table.insert("", "end", values=(
					row.get("Endereço", ""), row.get("Número", ""), row.get("Complemento", ""),
					row.get("CEP", ""), row.get("Zona", ""), "● ● ●"
				))
	
	def apply_table_filter(self, filters):
		"""Recebe os filtros, busca os dados e atualiza a tabela."""
		filtered_data = filter_imoveis(filters)
		self.load_data_into_table(filtered_data)
		self.show_view(self.table_view)

	def delete_selected_imoveis(self):
		selected_items = self.table.selection()
		if not selected_items:
			messagebox.showinfo("Nenhuma seleção", "Por favor, selecione um ou mais imóveis para deletar.")
			return
		enderecos_to_delete = [self.table.item(item, "values")[0] for item in selected_items]
		confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja deletar {len(enderecos_to_delete)} imóvel(is)?\nEsta ação não pode ser desfeita.")
		if confirm:
			result = delete_imoveis_by_endereco(enderecos_to_delete)
			messagebox.showinfo(result["status"].capitalize(), result["mensagem"])
			self.load_data_into_table()