import customtkinter as ctk
from .frames.dashboard_frame import DashboardFrame
from .frames.profile_frame import ProfileFrame
from .frames.settings_frame import SettingsFrame
from .frames.add_data_frame import AddDataFrame
from .frames.clients_frame import ClientsFrame

from .frames.detalhamento_geo_frame import DetalhamentoGeoFrame
from .frames.support_frame import SupportFrame
from .frames.logout_frame import LogoutFrame

class MainApplication(ctk.CTk):
	def __init__(self, user_email: str):
		super().__init__()
		self.title("A4G - Sistema de Gestão de Imóveis")
		self.geometry("1280x720")
		self.current_user_email = user_email

		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#c40000")
		self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
		self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="A4G\nDashboard", font=("IBM Plex Sans Condensed", 30, "bold"), text_color="white")
		self.logo_label.grid(row=0, column=0, padx=20, pady=20)

		self.button_frame_map = {
			"Home": DashboardFrame,
			"CRUD Imóveis": DetalhamentoGeoFrame,
			"Adicionar dados": AddDataFrame,
			"Clientes": ClientsFrame,
			"Meu perfil": ProfileFrame,
			"Configurações": SettingsFrame,
			"Sair": LogoutFrame,
			"Suporte": SupportFrame
		}

		button_order = ["Home", "CRUD Imóveis", "Adicionar dados", "Clientes", "Meu perfil", "Configurações", "Sair", "Suporte"]
		
		
		button_row = 1
		for button_text in button_order:
			frame_class = self.button_frame_map[button_text]
			callback = lambda fc=frame_class: self.show_frame(fc)
			button = ctk.CTkButton(self.sidebar_frame, text=button_text, command=callback, fg_color="transparent", text_color="white", hover_color="#a60000", anchor="w")
			
			if button_text in ["Meu perfil", "Suporte"]:
				button_row += 1

			button.grid(row=button_row, column=0, padx=20, pady=10, sticky="ew")
			button_row += 1

		self.content_frame = ctk.CTkFrame(self, fg_color="#F2F2F2")
		self.content_frame.grid(row=0, column=1, sticky="nsew")

		
		self.frames = {}
		self.current_frame = None

		for F in self.button_frame_map.values():
			frame = F(self.content_frame, app=self)
			self.frames[F] = frame

		self.show_frame(DashboardFrame)

	def show_frame(self, frame_class):
		if self.current_frame:
			self.current_frame.pack_forget()
		self.current_frame = self.frames[frame_class]
		self.current_frame.pack(fill="both", expand=True)

	def show_frame_by_name(self, frame_name):
		for name, frame_class in self.button_frame_map.items():
			if name == frame_name:
				self.show_frame(frame_class)
				break



