import customtkinter as ctk
from PIL import Image
import os
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

        sidebar_container = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="transparent")
        sidebar_container.grid(row=0, column=0, sticky="nsw")
        sidebar_container.grid_rowconfigure(0, weight=1)
        
        self.main_sidebar_frame = ctk.CTkFrame(sidebar_container, corner_radius=0, fg_color="transparent")
        self.main_sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_sidebar_frame.grid_columnconfigure(1, weight=1) # Permite que a área de texto se expanda

        # Faixa de ícones vermelha
        self.icon_strip_frame = ctk.CTkFrame(self.main_sidebar_frame, width=60, corner_radius=0, fg_color="#c40000")
        self.icon_strip_frame.grid(row=0, column=0, sticky="ns")
        
        # Área de texto cinza claro
        self.text_sidebar_frame = ctk.CTkFrame(self.main_sidebar_frame, corner_radius=0, fg_color="#EAEAEA")
        self.text_sidebar_frame.grid(row=0, column=1, sticky="nsew")
        
        # Sidebar do CRUD (permanece a mesma, vermelha e única)
        self.crud_sidebar_frame = ctk.CTkFrame(sidebar_container, corner_radius=0, fg_color="#c40000")
        self.crud_sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Área de Conteúdo
        self.content_frame = ctk.CTkFrame(self, fg_color="#F2F2F2")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.load_icons()

        self.main_sidebar_buttons = []
        self.crud_sidebar_buttons = []

        self.populate_main_sidebar()
        self.populate_crud_sidebar()
        self.show_main_view()

    def load_icons(self):
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icons")
        self.icons = {}
        icon_files = {
            "home": "home.png", "crud": "crud_icon.png", "add_data": "add_data_icon.png",
            "clients": "profile_icon.png", "profile": "profile_icon.png", "settings": "settings_icon.png",
            "logout": "logout_icon.png", "support": "support_icon.png"
        }

        for name, filename in icon_files.items():
            path = os.path.join(assets_path, filename)
            try:
                # --- MUDANÇA: Ícones da sidebar principal agora têm cores diferentes ---
                dark_icon = ctk.CTkImage(Image.open(path).convert("RGBA"), size=(24, 24))
                white_icon = ctk.CTkImage(Image.open(path).convert("RGBA"), size=(24, 24)) # Para o CRUD
                self.icons[name] = {'dark': dark_icon, 'white': white_icon}
            except FileNotFoundError:
                print(f"AVISO: Ícone '{filename}' não encontrado em '{assets_path}'.")
                self.icons[name] = None

    def show_frame(self, frame_class):
        if frame_class not in self.frames:
            frame = frame_class(self.content_frame, app=self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.frames[frame_class].tkraise()
    
    # --- MUDANÇA: Lógica de seleção atualizada para o novo estilo ---
    def select_button(self, selected_button, button_list, is_main_sidebar=True):
        for button in button_list:
            if is_main_sidebar:
                button.configure(fg_color="transparent", text_color="#5E5E5E")
            else: # Estilo do CRUD sidebar
                button.configure(fg_color="transparent")
        
        if is_main_sidebar:
            selected_button.configure(fg_color="#D3D3D3", text_color="#1C1C1C") # Cor de fundo e texto do item selecionado
        else:
            selected_button.configure(fg_color="#5E5E5E")


    def create_sidebar_button(self, parent, text, icon, frame_class, button_list, row, is_main=True, command=None):
        if is_main:
            button = ctk.CTkButton(parent, text=text, image=icon['dark'] if icon else None, compound="left", font=("Poppins", 16),
                                   fg_color="transparent", text_color="#5E5E5E", hover_color="#C0C0C0", anchor="w",
                                   height=40, border_spacing=10)
            button_list.append(button)
            if command:
                # Se um comando personalizado for fornecido, use-o
                button.configure(command=lambda b=button: self.select_and_show(b, frame_class, button_list, is_main_sidebar=True, custom_command=command))
            else:
                # Caso contrário, use a lógica padrão para mostrar um frame
                button.configure(command=lambda b=button, fc=frame_class: self.select_and_show(b, fc, button_list, is_main_sidebar=True))
            button.grid(row=row, column=0, padx=15, pady=8, sticky="ew")
        else: # Estilo CRUD
            button = ctk.CTkButton(parent, text=text, image=icon['white'] if icon else None, compound="left", font=("Poppins", 14),
                                   fg_color="transparent", text_color="white", hover_color="#a60000", anchor="w")
            button_list.append(button)
            button.configure(command=lambda b=button, fc=frame_class: self.select_and_show(b, fc, button_list, is_main_sidebar=False))
            button.grid(row=row, column=0, padx=20, pady=10, sticky="ew")

    def select_and_show(self, button, frame_class, button_list, is_main_sidebar, custom_command=None):
        self.select_button(button, button_list, is_main_sidebar)
        if custom_command:
            custom_command() # Executa o comando personalizado
        elif frame_class:
            self.show_frame(frame_class)

    # --- MUDANÇA: Populando a nova sidebar de duas partes ---
    def populate_main_sidebar(self):
        # Configuração do grid para empurrar itens para baixo
        self.text_sidebar_frame.grid_rowconfigure(5, weight=1)
        self.icon_strip_frame.grid_rowconfigure(5, weight=1)

        # Logo na área de texto
        logo_frame = ctk.CTkFrame(self.text_sidebar_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        logo_label_a4g = ctk.CTkLabel(logo_frame, text="A4G", font=("Poppins", 30, "bold"), text_color="#c40000")
        logo_label_a4g.pack(side="left")
        logo_label_dash = ctk.CTkLabel(logo_frame, text="Dashboard", font=("Poppins", 18), text_color="#5E5E5E")
        logo_label_dash.pack(side="left", padx=5)
        
        # Botões
        self.create_sidebar_button(self.text_sidebar_frame, "Home", self.icons.get("home"), DashboardFrame, self.main_sidebar_buttons, 1, is_main=True)
        
        # Botões
        self.create_sidebar_button(self.text_sidebar_frame, "Home", self.icons.get("home"), DashboardFrame, self.main_sidebar_buttons, 1, is_main=True)
        
        # Botão CRUD - Usando a função auxiliar create_sidebar_button com comando personalizado
        self.create_sidebar_button(self.text_sidebar_frame, "CRUD", self.icons.get("crud"), None, self.main_sidebar_buttons, 2, is_main=True, command=self.show_crud_view)
        
        self.create_sidebar_button(self.text_sidebar_frame, "Adicionar dados", self.icons.get("add_data"), AddDataFrame, self.main_sidebar_buttons, 3, is_main=True)
        
        self.create_sidebar_button(self.text_sidebar_frame, "Adicionar dados", self.icons.get("add_data"), AddDataFrame, self.main_sidebar_buttons, 3, is_main=True)
        # O design não mostra "Clientes" na home, mas vou manter caso seja necessário. Se não for, pode remover.
        self.create_sidebar_button(self.text_sidebar_frame, "Clientes", self.icons.get("clients"), ClientsFrame, self.main_sidebar_buttons, 4, is_main=True)
        
        # Botões inferiores
        self.create_sidebar_button(self.text_sidebar_frame, "Meu perfil", self.icons.get("profile"), ProfileFrame, self.main_sidebar_buttons, 6, is_main=True)
        self.create_sidebar_button(self.text_sidebar_frame, "Configurações", self.icons.get("settings"), SettingsFrame, self.main_sidebar_buttons, 7, is_main=True)
        self.create_sidebar_button(self.text_sidebar_frame, "Sair", self.icons.get("logout"), LogoutFrame, self.main_sidebar_buttons, 8, is_main=True)
        self.create_sidebar_button(self.text_sidebar_frame, "Suporte", self.icons.get("support"), SupportFrame, self.main_sidebar_buttons, 9, is_main=True)


    def populate_crud_sidebar(self):
        parent = self.crud_sidebar_frame
        parent.grid_rowconfigure(8, weight=1)
        logo = ctk.CTkLabel(parent, text="A4G\nDashboard", font=("IBM Plex Sans Condensed", 30, "bold"), text_color="white")
        logo.grid(row=0, column=0, padx=20, pady=20)
        
        back_button = ctk.CTkButton(parent, text="< Voltar para Home", command=self.show_main_view, fg_color="#a60000",
                                    text_color="white", hover_color="#8f0000", anchor="w", font=("Poppins", 14))
        back_button.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Usando a função auxiliar com is_main=False
        self.create_sidebar_button(parent, "Detalhamento Geo Imóvel", self.icons.get("crud"), DetalhamentoGeoFrame, self.crud_sidebar_buttons, 2, is_main=False)
        self.create_sidebar_button(parent, "Registro de Imóveis", self.icons.get("add_data"), RegistroImoveisFrame, self.crud_sidebar_buttons, 3, is_main=False)
        self.create_sidebar_button(parent, "Fluxo de caixa", self.icons.get("crud"), FluxoCaixaFrame, self.crud_sidebar_buttons, 4, is_main=False)
        self.create_sidebar_button(parent, "Contratos", self.icons.get("crud"), ContratosFrame, self.crud_sidebar_buttons, 5, is_main=False)
        self.create_sidebar_button(parent, "ITBI", self.icons.get("crud"), ItbiFrame, self.crud_sidebar_buttons, 6, is_main=False)

    def show_main_view(self):
        self.main_sidebar_frame.tkraise()
        # Seleciona o botão "Home" ao voltar para a view principal
        if self.main_sidebar_buttons:
            self.select_and_show(self.main_sidebar_buttons[0], DashboardFrame, self.main_sidebar_buttons, is_main_sidebar=True)

    def show_crud_view(self):
        self.crud_sidebar_frame.tkraise()
        # Seleciona o primeiro item do CRUD ao entrar nesta view
        if self.crud_sidebar_buttons:
            self.select_and_show(self.crud_sidebar_buttons[0], DetalhamentoGeoFrame, self.crud_sidebar_buttons, is_main_sidebar=False)