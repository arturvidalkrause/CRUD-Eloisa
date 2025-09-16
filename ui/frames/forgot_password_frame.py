import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox

class ForgotPasswordFrame(ctk.CTkFrame):
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
        print(f"Lógica de redefinição de senha para o email: {email}")
        messagebox.showinfo("Verifique seu Email", f"Se houver uma conta associada a {email}, um link de redefinição de senha foi enviado.")
        self.master.show_frame("login")

    def cancel(self):
        self.master.show_frame("login")