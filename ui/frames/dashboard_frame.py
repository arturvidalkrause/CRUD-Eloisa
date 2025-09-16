import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.dashboard_logic import (get_kpi_data, 
								  get_tipos_contrato_data, 
								  get_vacancia_data, 
								  get_area_atuacao_data, 
								  get_inadimplencia_data)

class MatplotlibChart(ctk.CTkFrame):
    def __init__(self, master, title, chart_type, data):
        super().__init__(master, fg_color="white", corner_radius=8)
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        label_title = ctk.CTkLabel(self, text=title, font=("Poppins", 12), text_color="gray50")
        label_title.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        fig = Figure(figsize=(4, 3), dpi=100, facecolor="white")
        ax = fig.add_subplot(111); ax.set_facecolor("white")
        colors = ['#c40000', '#555555', '#A9A9A9', '#D3D3D3']
        if chart_type == 'pie' and not data.empty:
            wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', startangle=90, colors=colors, pctdistance=0.85, wedgeprops=dict(width=0.4, edgecolor='w'))
            ax.legend(wedges, data.index, loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=8, frameon=False)
        elif chart_type == 'bar' and not data.empty:
            ax.bar(data.index, data.values, color=colors)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            ax.tick_params(axis='x', labelsize=8); ax.tick_params(axis='y', labelsize=8)
        else: ax.text(0.5, 0.5, "Sem dados", horizontalalignment='center', verticalalignment='center')
        fig.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self); canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

class MatplotlibBarChart(ctk.CTkFrame):
	def __init__(self, master, data, title):
		super().__init__(master, fg_color="white", corner_radius=8)
		self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
		label_title = ctk.CTkLabel(self, text=title, font=("Poppins", 12), text_color="gray50")
		label_title.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
		fig = Figure(figsize=(5, 2), dpi=100, facecolor="#FFFFFF")
		ax = fig.add_subplot(111)
		ax.bar(data.index, data.values, color='#c40000')
		ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
		ax.tick_params(axis='x', labelsize=8); ax.tick_params(axis='y', labelsize=8)
		fig.tight_layout()
		canvas = FigureCanvasTkAgg(fig, master=self)
		canvas.draw()
		canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        kpis = get_kpi_data()
        self.create_kpi_card("Receita média das Locações", kpis["receita_media"], 0, 0, colspan=2)
        self.create_kpi_card("Porcentagem de rentabilidade", kpis["rentabilidade"], 0, 2, colspan=2)
        self.create_kpi_card("Número de imóveis", kpis["num_imoveis"], 1, 0)
        self.create_kpi_card("Número de clientes", kpis["num_clientes"], 1, 1)
        self.create_kpi_card("Número de Contratos", kpis["num_contratos"], 1, 2, colspan=2)
        MatplotlibChart(self, "Tipos de contratos", 'pie', get_tipos_contrato_data()).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        MatplotlibChart(self, "Vacância dos imóveis", 'bar', get_vacancia_data()).grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        MatplotlibChart(self, "Área de atuação", 'pie', get_area_atuacao_data()).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        MatplotlibChart(self, "Inadimplência", 'bar', get_inadimplencia_data()).grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
    def create_kpi_card(self, title, value, row, col, colspan=1):
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=8); card.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="nsew"); card.grid_columnconfigure(0, weight=1)
        label_title = ctk.CTkLabel(card, text=title, font=("Poppins", 12), text_color="gray50"); label_title.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        label_value = ctk.CTkLabel(card, text=value, font=("Poppins", 22, "bold"), text_color="black"); label_value.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")