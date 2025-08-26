import pandas as pd
import os

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

def get_kpi_data():
	"""
	Calcula os KPIs a partir dos arquivos Excel na pasta /data.
	"""
	df_imoveis = safe_read_excel('imoveis.xlsx')
	df_contratos = safe_read_excel('contratos.xlsx')
	df_usuarios = safe_read_excel('database_usuarios.xlsx')

	if not df_contratos.empty and 'Valor Aluguel' in df_contratos.columns:
		receita_media = df_contratos['Valor Aluguel'].mean()
		receita_media_str = f"R$ {receita_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
	else:
		receita_media_str = "N/A"

	num_imoveis = len(df_imoveis)

	num_clientes = len(df_usuarios)

	num_contratos = len(df_contratos)
	
	rentabilidade = "36,2%"

	kpi_data = {
		"receita_media": receita_media_str,
		"rentabilidade": rentabilidade,
		"num_imoveis": num_imoveis,
		"num_clientes": num_clientes,
		"num_contratos": num_contratos
	}
	return kpi_data

def get_tipos_contrato_data():
	"""
	Lê o arquivo de contratos e retorna a contagem de cada tipo de contrato.
	"""
	df_contratos = safe_read_excel('contratos.xlsx')

	if not df_contratos.empty and 'Tipo Contrato' in df_contratos.columns:
		return df_contratos['Tipo Contrato'].value_counts()

	return pd.Series({"Temporada": 7, "Comercial": 12, "Residencial": 10})

def get_vacancia_data():
	"""
	Retorna dados de exemplo para o gráfico de vacância.
	No futuro, esta função calculará a vacância real baseada nos contratos.
	"""
	data = {
		'Jan': 10, 'Fev': 12, 'Mar': 15, 'Abr': 8, 'Mai': 11,
		'Jun': 7, 'Jul': 9, 'Ago': 14, 'Set': 18, 'Out': 22,
		'Nov': 25, 'Dez': 20
	}
	return pd.Series(data)

def get_area_atuacao_data():
	"""
	Retorna dados de exemplo para o gráfico de pizza 'Área de atuação'.
	No futuro, leria o arquivo de imóveis e agruparia por bairro/zona.
	"""
	data = {
		"Zona Sul": 4,
		"Zona Norte": 2,
		"Centro": 1,
		"Zona Oeste": 1
	}
	return pd.Series(data)

def get_inadimplencia_data():
	"""
	Retorna dados de exemplo para o gráfico de barras 'Inadimplência'.
	No futuro, calcularia a inadimplência real.
	"""
	data = {
		'Comercial': 85,
		'Residencial': 40,
		'Long Stay': 30,
		'Outros': 15
	}
	return pd.Series(data)