import customtkinter as ctk
class ItbiFrame(ctk.CTkFrame):
	def __init__(self, master, app):
		super().__init__(master, fg_color="transparent")
		self.app = app
		ctk.CTkLabel(self, text="ITBI", font=("Poppins", 24, "bold")).pack(pady=20)