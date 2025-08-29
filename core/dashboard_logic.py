import pandas as pd
import os

# Define o caminho base para a pasta de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def safe_read_excel(filename):
	"""Lê um arquivo Excel de forma segura, retornando um DataFrame vazio se não existir."""
	path = os.path.join(DATA_DIR, filename)
	if os.path.exists(path):
		try:
			return pd.read_excel(path)
		except Exception as e:
			print(f"Erro ao ler o arquivo {filename}: {e}")
			return pd.DataFrame()
	return pd.DataFrame()

# --- FUNÇÕES PARA KPIs (JÁ EXISTENTES E FUNCIONAIS) ---
def get_kpi_data():
	df_imoveis = safe_read_excel('imoveis_data.xlsx')
	df_contratos = safe_read_excel('contratos.xlsx')
	df_usuarios = safe_read_excel('database_usuarios.xlsx')

	if not df_contratos.empty and 'Valor do Aluguel' in df_contratos.columns:
		receita_media = df_contratos['Valor do Aluguel'].mean()
		receita_media_str = f"R$ {receita_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
	else:
		receita_media_str = "N/A"

	kpi_data = {
		"receita_media": receita_media_str,
		"rentabilidade": "36,2%", # Manter como placeholder
		"num_imoveis": len(df_imoveis),
		"num_clientes": len(df_usuarios),
		"num_contratos": len(df_contratos)
	}
	return kpi_data

# --- NOVAS FUNÇÕES PARA OS GRÁFICOS ---

def get_tipos_contrato_data():
	"""Lê o arquivo de contratos e retorna a contagem de cada tipo de contrato."""
	df_contratos = safe_read_excel('contratos.xlsx')
	if not df_contratos.empty and 'Tipo de Contrato' in df_contratos.columns:
		return df_contratos['Tipo de Contrato'].value_counts()
	return pd.Series({"Exemplo": 1}) # Dado padrão se não encontrar

def get_area_atuacao_data():
	"""Lê o arquivo de imóveis e retorna a contagem por Zona."""
	df_imoveis = safe_read_excel('imoveis_data.xlsx')
	if not df_imoveis.empty and 'Zona' in df_imoveis.columns:
		return df_imoveis['Zona'].value_counts()
	return pd.Series({"Exemplo": 1})

def get_vacancia_data():
	"""
	Cria um gráfico de atividade de novos contratos por mês.
	Uma análise de vacância real seria mais complexa, mas esta é uma ótima aproximação.
	"""
	df_contratos = safe_read_excel('contratos.xlsx')
	if not df_contratos.empty and 'Data de Início' in df_contratos.columns:
		# Garante que a coluna de data esteja no formato correto
		df_contratos['Data de Início'] = pd.to_datetime(df_contratos['Data de Início'], errors='coerce')
		# Remove linhas onde a data não pôde ser convertida
		df_contratos.dropna(subset=['Data de Início'], inplace=True)
		# Agrupa por mês e conta o número de contratos iniciados
		contratos_por_mes = df_contratos['Data de Início'].dt.strftime('%b').value_counts()
		# Ordena os meses
		meses_ordenados = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		return contratos_por_mes.reindex(meses_ordenados, fill_value=0)
	return pd.Series({"Exemplo": 1})

def get_inadimplencia_data():
	"""
	Mantido com dados de exemplo, pois a lógica real requer dados de pagamentos.
	"""
	data = {'Comercial': 85, 'Residencial': 40, 'Long Stay': 30, 'Outros': 15}
	return pd.Series(data)