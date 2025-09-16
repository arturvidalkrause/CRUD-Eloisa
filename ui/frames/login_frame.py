import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
from core.crud_operations import autenticar_usuario
from ui.main_application import MainApplication

class LoginFrame(ctk.CTkFrame):
	def __init__(self, master, app):
		super().__init__(master)
		self.master = master
		self.app = app

		assets_path = os.path.join(os.path.dirname(__file__), "../..", "assets")
		image_path = os.path.join(assets_path, "images", "background.jpg")

		self.bg_image = ctk.CTkImage(Image.open(image_path), size=(1024, 768))
		self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

		self.bind("<Configure>", self.on_resize)

		font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
		self.font_poppins_regular = ctk.CTkFont(family="Poppins", size=14)
		self.font_poppins_bold = ctk.CTkFont(family="Poppins", size=14, weight="bold")
		self.logo_font = ctk.CTkFont(family="IBM Plex Sans Condensed", size=48, weight="bold")
		
		assets_path = os.path.join(os.path.dirname(__file__), "../..", "assets")
		self.logo_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "home.png")), size=(30, 30))
		self.email_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "email_icon.png")), size=(20, 20))
		self.password_icon = ctk.CTkImage(light_image=Image.open(os.path.join(assets_path, "icons", "password_icon.png")), size=(20, 20))

		login_content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
		login_content_frame.place(relx=0.75, rely=0.5, anchor="center")

		logo_frame = ctk.CTkFrame(login_content_frame, fg_color="transparent")
		logo_frame.pack(pady=(40, 20), padx=100)
		logo_icon_label = ctk.CTkLabel(logo_frame, image=self.logo_icon, text="").pack(side="left", padx=(0, 10))
		logo_text_a = ctk.CTkLabel(logo_frame, text="A", font=self.logo_font, text_color="#000000").pack(side="left")
		logo_text_4g = ctk.CTkLabel(logo_frame, text="4G", font=self.logo_font, text_color="#FF0000").pack(side="left")


		email_entry_frame = ctk.CTkFrame(login_content_frame, fg_color="transparent")
		email_entry_frame.pack(pady=10, padx=30, fill="x")
		email_icon_label = ctk.CTkLabel(email_entry_frame, image=self.email_icon, text="").pack(side="left", padx=(0,10))
		self.email_entry = ctk.CTkEntry(email_entry_frame, placeholder_text="Email", font=self.font_poppins_regular, fg_color="#F0F0F0", border_width=0, height=40)
		self.email_entry.pack(side="left", fill="x", expand=True)


		password_entry_frame = ctk.CTkFrame(login_content_frame, fg_color="transparent")
		password_entry_frame.pack(pady=10, padx=30, fill="x")
		password_icon_label = ctk.CTkLabel(password_entry_frame, image=self.password_icon, text="").pack(side="left", padx=(0,10))
		self.password_entry = ctk.CTkEntry(password_entry_frame, placeholder_text="Senha", show="*", font=self.font_poppins_regular, fg_color="#F0F0F0", border_width=0, height=40)
		self.password_entry.pack(side="left", fill="x", expand=True)


		login_button = ctk.CTkButton(login_content_frame, text="Login", font=self.font_poppins_bold, height=45, corner_radius=25, command=self.login_action)
		login_button.pack(pady=(30, 20), padx=30, fill="x")

		bottom_frame = ctk.CTkFrame(login_content_frame, fg_color="transparent")
		bottom_frame.pack(pady=(0, 30), padx=30, fill="x")
		forgot_password_link = ctk.CTkButton(bottom_frame, text="Esqueci minha senha", font=self.font_poppins_regular, fg_color="transparent", text_color="#555555", hover=False, command=self.forgot_password_action)
		forgot_password_link.pack(side="left")
		register_link = ctk.CTkButton(bottom_frame, text="Registrar", font=self.font_poppins_regular, fg_color="transparent", text_color="#FF0000", hover=False, command=self.register_action)
		register_link.pack(side="right")

	
	def on_resize(self, event):
		self.bg_image.configure(size=(event.width, event.height))
		
	def login_action(self):
		"""
		MUDANÇA AQUI: Simula um login, fecha a janela atual e abre a principal.
		"""
		email = self.email_entry.get()
		password = self.password_entry.get()
		

		if email and password:
			print("Login bem-sucedido!")
			
			self.master.destroy() 
			
			main_app = MainApplication()
			main_app.mainloop()
			
		else:
			messagebox.showerror("Erro de Login", "Por favor, insira email e senha.")

	def forgot_password_action(self):
		print("Link 'Esqueci minha senha' clicado")

	def register_action(self):
		self.master.show_frame("register")
	
	def login_action(self):
		email = self.email_entry.get()
		password = self.password_entry.get()

		if autenticar_usuario(email, password):
			self.master.destroy()
			main_app = MainApplication(user_email=email)
			main_app.mainloop()
		else:
			messagebox.showerror("Erro de Login", "Email ou senha inválidos.")
	
	def forgot_password_action(self):
		print("Link 'Esqueci minha senha' clicado")
		self.master.show_frame("forgotpassword")