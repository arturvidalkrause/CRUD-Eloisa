import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
import random
import string
from core.crud_operations import autenticar_email, atualizar_senha
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

load_dotenv()

class ForgotPasswordFrame(ctk.CTkFrame):
	def __init__(self, master, app):
		super().__init__(master)
		self.master = master
		self.app = app
		
		self.SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
		self.SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

		assets_path = os.path.join(os.path.dirname(__file__), "../..", "assets")
		image_path = os.path.join(assets_path, "images", "background.jpg")

		self.bg_image = ctk.CTkImage(Image.open(image_path), size=(1024, 768))
		self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		self.bind("<Configure>", self.on_resize)

		# --- Carregar fontes ---
		self.font_poppins_regular = ctk.CTkFont(family="Poppins", size=14)
		self.font_poppins_bold = ctk.CTkFont(family="Poppins", size=14, weight="bold")
		self.logo_font = ctk.CTkFont(family="IBM Plex Sans Condensed", size=48, weight="bold")
		
		# --- Carregar ícones ---
		self.email_icon = ctk.CTkImage(
			light_image=Image.open(os.path.join(assets_path, "icons", "email_icon.png")), size=(20, 20))

		# --- Frame principal para o conteúdo ---
		content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
		content_frame.place(relx=0.5, rely=0.5, anchor="center") # Centralizado

		# --- Logo ---
		logo_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
		logo_frame.pack(pady=(40, 20), padx=100)
		logo_text_a = ctk.CTkLabel(logo_frame, text="A", font=self.logo_font, text_color="#000000")
		logo_text_a.pack(side="left")
		logo_text_4g = ctk.CTkLabel(logo_frame, text="4G", font=self.logo_font, text_color="#FF0000")
		logo_text_4g.pack(side="left")

		# --- Título e Instruções ---
		title = ctk.CTkLabel(content_frame, text="Esqueci minha senha", font=("Poppins", 20, "bold"), text_color="#333333")
		title.pack(pady=(0, 10))

		instructions = ctk.CTkLabel(content_frame, 
									text="Para redefinir sua senha, informe o email cadastrado na sua conta\ne lhe enviaremos um link com as instruções.",
									font=self.font_poppins_regular, text_color="#555555")
		instructions.pack(pady=(0, 20), padx=30)

		# --- Campo de Email ---
		email_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
		email_entry_frame.pack(pady=10, padx=30, fill="x")
		
		email_icon_label = ctk.CTkLabel(email_entry_frame, image=self.email_icon, text="")
		email_icon_label.pack(side="left", padx=(0,10))

		self.email_entry = ctk.CTkEntry(email_entry_frame, placeholder_text="Email", font=self.font_poppins_regular,
								   fg_color="#F0F0F0", border_width=0, height=40)
		self.email_entry.pack(side="left", fill="x", expand=True)

		# --- Botão de Enviar ---
		send_button = ctk.CTkButton(content_frame, text="Enviar", font=self.font_poppins_bold,
								 height=45, corner_radius=25, command=self.send_reset_link)
		send_button.pack(pady=(30, 10), padx=30, fill="x")
		
		# --- Botão de Cancelar ---
		cancel_button = ctk.CTkButton(content_frame, text="Cancelar", font=self.font_poppins_regular,
									  fg_color="transparent", text_color="#1E90FF", hover=False,
									  command=self.cancel)
		cancel_button.pack(pady=(0, 30))
	
	def on_resize(self, event):
		self.bg_image.configure(size=(event.width, event.height))
		
	def send_reset_link(self):
		email = self.email_entry.get()
		if not email:
			messagebox.showwarning("Campo Vazio", "Por favor, informe seu email.")
			return
	
		if not autenticar_email(email):
			messagebox.showerror("Email não encontrado", "Não existe conta associada a este email.")
			return
		
		# Gera uma nova senha aleatória
		new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

		# Tenta enviar o email ANTES de atualizar o banco de dados
		try:
			# Verifica se as chaves foram carregadas do .env
			if not self.SENDGRID_API_KEY or not self.SENDGRID_FROM_EMAIL:
				messagebox.showerror("Erro de Configuração", "As credenciais de envio de email não foram configuradas.")
				return

			# Cria o conteúdo do email
			subject = "Redefinição de Senha - A4G"
			html_content = f"""
			<html>
				<body>
					<h2>Redefinição de Senha</h2>
					<p>Olá,</p>
					<p>Você solicitou uma nova senha para sua conta em nosso sistema.</p>
					<p>Sua nova senha temporária é: <strong>{new_password}</strong></p>
					<p>Por favor, faça login e altere esta senha assim que possível por uma de sua preferência.</p>
					<p>Se você não solicitou esta alteração, por favor, ignore este email.</p>
					<br>
					<p>Atenciosamente,</p>
					<p>Equipe A4G</p>
				</body>
			</html>
			"""
			
			message = Mail(
				from_email=self.SENDGRID_FROM_EMAIL,
				to_emails=email,
				subject=subject,
				html_content=html_content
			)

			# Envia o email
			sg = SendGridAPIClient(self.SENDGRID_API_KEY)
			response = sg.send(message)

			# Se o email for enviado com sucesso, atualiza a senha no banco
			if response.status_code in [200, 202]:
				atualizar_senha(email, new_password)
				messagebox.showinfo("Sucesso!", f"Uma nova senha foi enviada para {email}.")
				self.master.show_frame("login")
			else:
				# Se a API do SendGrid retornar um erro
				messagebox.showerror("Erro de Envio", f"Não foi possível enviar o email. (Código: {response.status_code})")

		except Exception as e:
			messagebox.showerror("Erro Crítico", f"Ocorreu um erro inesperado: {e}")

	def cancel(self):
		self.master.show_frame("login")