import customtkinter as ctk

class SupportFrame(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="transparent")
		
		ctk.CTkLabel(self, text="Suporte", font=("Poppins", 24, "bold")).pack(pady=20, padx=20, anchor="w")

		container = ctk.CTkFrame(self, fg_color="transparent")
		container.pack(fill="both", expand=True, padx=100, pady=20)

		info_text = "Envie uma mensagem para o nosso suporte com sua dúvida, crítica ou sugestão!"
		ctk.CTkLabel(container, text=info_text, font=("Poppins", 16)).pack(pady=10, fill="x")

		textbox = ctk.CTkTextbox(container, height=200, font=("Poppins", 12), border_width=1)
		textbox.pack(fill="both", expand=True, pady=10)

		button_frame = ctk.CTkFrame(container, fg_color="transparent")
		button_frame.pack(pady=10)
		ctk.CTkButton(button_frame, text="Enviar", width=150, height=40).pack(side="left", padx=5)
		ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray").pack(side="left", padx=5)