import customtkinter as ctk
from PIL import Image
import os
from ui.frames.login_frame import LoginFrame
from ui.frames.register_frame import RegisterFrame 

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("Sistema de Gestão A4G")
		self.geometry("1024x768")
		ctk.set_appearance_mode("light")

		container = ctk.CTkFrame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		assets_path = os.path.join(os.path.dirname(__file__), "assets")
		self.bg_image = ctk.CTkImage(Image.open(os.path.join(assets_path, "images", "background.jpg")), size=(1024, 768))
		self.bg_label = ctk.CTkLabel(container, image=self.bg_image, text="")
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.bind("<Configure>", self.on_resize)
		
		self.frames = {}

		for F in (LoginFrame, RegisterFrame):
			page_name = F.__name__.lower().replace("frame", "") # "login", "register"
			frame = F(master=self)
			self.frames[page_name] = frame
			frame.place(x=0, y=0, relwidth=1, relheight=1)

		self.show_frame("login")

	def on_resize(self, event):
		self.bg_image.configure(size=(event.width, event.height))

	def show_frame(self, page_name):
		"""Traz o frame solicitado para a frente."""
		frame = self.frames[page_name]
		frame.tkraise()


if __name__ == "__main__":
	app = App()
	app.mainloop()