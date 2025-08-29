

import customtkinter as ctk

from .frames.dashboard_frame import DashboardFrame
from .frames.profile_frame import ProfileFrame
from .frames.settings_frame import SettingsFrame
from .frames.add_data_frame import AddDataFrame
from .frames.clients_frame import ClientsFrame
from .frames.detalhamento_geo_frame import DetalhamentoGeoFrame
from .frames.registro_imoveis_frame import RegistroImoveisFrame
from .frames.fluxo_caixa_frame import FluxoCaixaFrame
from .frames.contratos_frame import ContratosFrame
from .frames.itbi_frame import ItbiFrame
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
		self.sidebar_frame.grid_rowconfigure(10, weight=1)


		self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="A4G\nDashboard", font=("IBM Plex Sans Condensed", 30, "bold"), text_color="white")
		self.logo_label.grid(row=0, column=0, padx=20, pady=20)


		self.button_frame_map = {
			"Home": DashboardFrame,
			"Detalhamento Geo Imóvel": DetalhamentoGeoFrame,
			"Registro de Imóveis": RegistroImoveisFrame,
			"Fluxo de Caixa": FluxoCaixaFrame,
			"Contratos": ContratosFrame,
			"ITBI": ItbiFrame,
			"Adicionar Dados": AddDataFrame,
			"Clientes": ClientsFrame,
			"Meu Perfil": ProfileFrame,
			"Configurações": SettingsFrame,
			"Suporte": SupportFrame,
			"Sair": LogoutFrame
		}


		button_order = ["Home", "Detalhamento Geo Imóvel", "Registro de Imóveis", "Fluxo de Caixa", "Contratos", "ITBI", "Adicionar Dados", "Clientes", "Meu Perfil", "Configurações", "Suporte", "Sair"]


		button_row = 1
		for button_text in button_order:
			frame_class = self.button_frame_map[button_text]

			callback = lambda fc=frame_class: self.show_frame(fc)
			button = ctk.CTkButton(self.sidebar_frame, text=button_text, command=callback, fg_color="transparent", text_color="white", hover_color="#a60000", anchor="w")
			button.grid(row=button_row, column=0, padx=20, pady=10, sticky="ew")
			button_row += 1


		self.content_frame = ctk.CTkFrame(self, fg_color="#F2F2F2")
		self.content_frame.grid(row=0, column=1, sticky="nsew")
		self.content_frame.grid_rowconfigure(0, weight=1)
		self.content_frame.grid_columnconfigure(0, weight=1)



		self.frames = {}


		self.show_frame(DashboardFrame)

	def show_frame(self, frame_class):
		"""
		Mostra o frame. Se for a primeira vez, ele o cria.
		Senão, apenas o traz para a frente.
		"""


		if frame_class not in self.frames:

			frame = frame_class(self.content_frame, app=self)
			self.frames[frame_class] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		

		frame = self.frames[frame_class]
		frame.tkraise()

	def show_frame_by_name(self, frame_name):
		"""Mostra o frame com base no nome do botão."""
		if frame_name in self.button_frame_map:
			self.show_frame(self.button_frame_map[frame_name])