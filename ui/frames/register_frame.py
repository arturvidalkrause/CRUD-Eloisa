import customtkinter as ctk
from PIL import Image
import os
from core.crud_operations import criar_novo_registro
from tkinter import messagebox

class RegisterFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		font_path = os.path.join(os.path.dirname(__file__), "../..", "assets", "fonts")
		self.font_poppins_regular = ctk.CTkFont(family="Poppins", size=14)
		self.font_poppins_bold = ctk.CTkFont(family="Poppins", size=14, weight="bold")
		self.logo_font = ctk.CTkFont(family="IBM Plex Sans Condensed", size=48, weight="bold")

		assets_path = os.path.join(os.path.dirname(__file__), "../..", "assets")
		self.logo_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "logo_icon.png")), size=(30, 30))
		self.user_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "email_icon.png")), size=(20, 20))
		self.password_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "password_icon.png")), size=(20, 20))

		register_content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=15)
		register_content_frame.place(relx=0.5, rely=0.5, anchor="center")

		logo_frame = ctk.CTkFrame(register_content_frame, fg_color="transparent")
		logo_frame.pack(pady=(30, 15), padx=100)
		logo_icon_label = ctk.CTkLabel(logo_frame, image=self.logo_icon, text="").pack(side="left", padx=(0, 10))
		logo_text_a = ctk.CTkLabel(logo_frame, text="A", font=self.logo_font, text_color="#000000").pack(side="left")
		logo_text_4g = ctk.CTkLabel(logo_frame, text="4G", font=self.logo_font, text_color="#FF0000").pack(side="left")
		
		title_label = ctk.CTkLabel(register_content_frame, text="Registrar", font=self.font_poppins_bold, text_color="#555555")
		title_label.pack(pady=(0, 15))

		self.name_entry = self.create_entry(register_content_frame, "Nome", self.user_icon)
		self.lastname_entry = self.create_entry(register_content_frame, "Sobrenome completo", self.user_icon)
		self.cpf_entry = self.create_entry(register_content_frame, "CPF", self.user_icon)
		self.email_entry = self.create_entry(register_content_frame, "Email", self.user_icon)
		self.password_entry = self.create_entry(register_content_frame, "Senha", self.password_icon, show="*")
		self.confirm_password_entry = self.create_entry(register_content_frame, "Confirmar senha", self.password_icon, show="*")

		register_button = ctk.CTkButton(register_content_frame, text="Registrar", font=self.font_poppins_bold,
									 height=45, corner_radius=25, command=self.register_action)
		register_button.pack(pady=20, padx=30, fill="x")

		login_link = ctk.CTkButton(register_content_frame, text="Já tem uma conta? Faça Login", font=self.font_poppins_regular,
								   fg_color="transparent", text_color="#555555", hover=False, command=self.go_to_login)
		login_link.pack(pady=(0, 20))

	def create_entry(self, parent, placeholder, icon, show=None):
		entry_frame = ctk.CTkFrame(parent, fg_color="transparent")
		entry_frame.pack(pady=5, padx=30, fill="x")
		icon_label = ctk.CTkLabel(entry_frame, image=icon, text="").pack(side="left", padx=(0,10))
		entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder, font=self.font_poppins_regular,
							 fg_color="#F0F0F0", border_width=0, height=40, show=show)
		entry.pack(side="left", fill="x", expand=True)
		return entry

	def register_action(self):
		nome = self.name_entry.get()
		sobrenome = self.lastname_entry.get()
		cpf = self.cpf_entry.get()
		email = self.email_entry.get()
		senha = self.password_entry.get()
		confirmar_senha = self.confirm_password_entry.get()

		if senha != confirmar_senha:
			messagebox.showerror("Erro de Senha", "As senhas não coincidem!")
			return

		resultado = criar_novo_registro(nome, sobrenome, cpf, email, senha)

		if resultado["status"] == "sucesso":
			messagebox.showinfo("Sucesso", resultado["mensagem"])
			self.go_to_login() # Volta para a tela de login apos o sucesso
		else:
			messagebox.showerror("Erro de Registro", resultado["mensagem"])

	def go_to_login(self):
		self.master.show_frame("login")