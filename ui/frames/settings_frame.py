import customtkinter as ctk

class SettingsFrame(ctk.CTkFrame):
	def __init__(self, master, app): # Recebe o app
		super().__init__(master, fg_color="transparent")
		self.app = app
		ctk.CTkLabel(self, text="Configurações", font=("Poppins", 24, "bold")).pack(pady=20, padx=20, anchor="w")

		options_frame = ctk.CTkFrame(self, fg_color="transparent")
		options_frame.pack(fill="x", padx=40, pady=10)
		options_frame.grid_columnconfigure(1, weight=1)

		ctk.CTkLabel(options_frame, text="Exportar base de dados:   ", font=("Poppins", 14)).grid(row=3, column=0, sticky="w", pady=(15, 0))
		export_db_frame = ctk.CTkFrame(options_frame, fg_color="transparent"); export_db_frame.grid(row=3, column=1, sticky="w", pady=(15, 0))

		ctk.CTkButton(export_db_frame, text=".xlsx", fg_color="#2B8C5A").pack(side="left", padx=(0, 5))
		ctk.CTkButton(export_db_frame, text=".xls", fg_color="#86B828").pack(side="left", padx=(0, 5))
		ctk.CTkButton(export_db_frame, text=".csv", fg_color="#1F77B4").pack(side="left", padx=(0, 5))

		ctk.CTkLabel(options_frame, text="Exportar dashboard:", font=("Poppins", 14)).grid(row=4, column=0, sticky="w", pady=(15, 0))
		ctk.CTkButton(options_frame, text=".pbix", fg_color="#F2C811", text_color="black").grid(row=4, column=1, sticky="w", pady=(15, 0))

		ctk.CTkButton(self, text="Aplicar", height=40).pack(pady=40, padx=40, anchor="e")