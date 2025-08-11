import customtkinter as ctk

class LogoutFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        ctk.CTkLabel(self, text="Sair", font=("Poppins", 24, "bold")).pack(pady=20, padx=20, anchor="w")
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=100, pady=20)

        info_text = ("Essa ação finalizará todas as atividades em andamento e retornará você ao ambiente inicial.\n\nDeseja prosseguir?")
        ctk.CTkLabel(container, text=info_text, font=("Poppins", 16), justify="center", wraplength=500).pack(pady=40)

        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=10)
		
        ctk.CTkButton(button_frame, text="Sair", width=150, height=40, command=self.app.destroy).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancelar", fg_color="gray", command=lambda: self.app.show_frame_by_name("Home")).pack(side="left", padx=5)