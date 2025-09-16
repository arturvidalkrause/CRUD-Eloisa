import pandas as pd
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

USER_DATA_PATH = os.path.join(DATA_DIR, 'database_usuarios.xlsx')

def safe_read_data(filename):
	"""
	Lê um arquivo de dados (Excel ou CSV) de forma segura.
	"""
	path = os.path.join(DATA_DIR, filename)
	if not os.path.exists(path):
		return pd.DataFrame() # Retorna um DataFrame vazio se o arquivo não existe
	
	try:
		if filename.endswith(('.xlsx', '.xls')):
			return pd.read_excel(path)
		elif filename.endswith('.csv'):
			return pd.read_csv(path)
	except Exception as e:
		print(f"Erro ao ler o arquivo {filename}: {e}")
		return pd.DataFrame()
	
	return pd.DataFrame()

def criar_novo_registro(nome, sobrenome, cpf, email, senha):
	novo_usuario = {"Nome": [nome], "Sobrenome": [sobrenome], "CPF": [cpf], "Email": [email], "Senha": [senha]}
	novo_df = pd.DataFrame(novo_usuario)
	try:
		if os.path.exists(USER_DATA_PATH):
			df_existente = pd.read_excel(USER_DATA_PATH)
			df_final = pd.concat([df_existente, novo_df], ignore_index=True)
		else:
			df_final = novo_df
		df_final.to_excel(USER_DATA_PATH, index=False)
		return {"status": "sucesso", "mensagem": "Usuário registrado com sucesso!"}
	except Exception as e:
		return {"status": "erro", "mensagem": f"Erro ao salvar dados: {e}"}

def autenticar_usuario(email, senha):
	if not os.path.exists(USER_DATA_PATH): return False
	df = pd.read_excel(USER_DATA_PATH)
	usuario_encontrado = df[df['Email'] == email]
	if not usuario_encontrado.empty:
		if usuario_encontrado.iloc[0]['Senha'] == senha:
			return True
	return False

def autenticar_email(email):
	if not os.path.exists(USER_DATA_PATH): return False
	df = pd.read_excel(USER_DATA_PATH)
	usuario_encontrado = df[df['Email'] == email]
	return not usuario_encontrado.empty

def atualizar_senha(email, nova_senha):
	if not os.path.exists(USER_DATA_PATH): return {"status": "erro", "mensagem": "Arquivo de dados não encontrado."}
	df = pd.read_excel(USER_DATA_PATH)
	user_index = df[df['Email'] == email].index
	if not user_index.empty:
		df.loc[user_index, 'Senha'] = nova_senha
		df.to_excel(USER_DATA_PATH, index=False)
		return {"status": "sucesso", "mensagem": "Senha atualizada com sucesso!"}
	return {"status": "erro", "mensagem": "Usuário não encontrado."}

def get_user_data(email):
	df = safe_read_data('database_usuarios.xlsx')
	if not df.empty:
		usuario_encontrado = df[df['Email'] == email]
		if not usuario_encontrado.empty:
			return usuario_encontrado.iloc[0].to_dict()
	return None

def update_user_data(email, new_data):
	df = safe_read_data('database_usuarios.xlsx')
	if not df.empty:
		user_index = df[df['Email'] == email].index
		if not user_index.empty:
			for key, value in new_data.items():
				df.loc[user_index, key] = value
			df.to_excel(USER_DATA_PATH, index=False)
			return {"status": "sucesso", "mensagem": "Dados atualizados com sucesso!"}
	return {"status": "erro", "mensagem": "Usuário não encontrado."}

def get_all_clients():
	return safe_read_data('database_usuarios.xlsx')

def delete_clients_by_cpf(cpfs_to_delete):
	if not cpfs_to_delete: return {"status": "info", "mensagem": "Nenhum cliente selecionado."}
	df = safe_read_data('database_usuarios.xlsx')
	rows_before = len(df)
	df = df[~df['CPF'].isin(cpfs_to_delete)]
	rows_after = len(df)
	df.to_excel(USER_DATA_PATH, index=False)
	deleted_count = rows_before - rows_after
	return {"status": "sucesso", "mensagem": f"{deleted_count} cliente(s) deletado(s) com sucesso!"}



def add_new_imovel(imovel_data):
	path = os.path.join(DATA_DIR, 'imoveis_data.xlsx')
	novo_df = pd.DataFrame([imovel_data])
	try:
		if os.path.exists(path):
			df_existente = pd.read_excel(path)
			df_final = pd.concat([df_existente, novo_df], ignore_index=True)
		else:
			df_final = novo_df
		df_final.to_excel(path, index=False)
		return {"status": "sucesso", "mensagem": "Imóvel adicionado com sucesso!"}
	except Exception as e:
		return {"status": "erro", "mensagem": f"Erro ao salvar imóvel: {e}"}

def get_all_imoveis():
	"""
	Lê o arquivo de imóveis, procurando por .csv primeiro, depois .xlsx.
	"""
	df = safe_read_data('imoveis_data.csv')
	if df.empty:
		df = safe_read_data('imoveis_data.xlsx')
	return df

def delete_imoveis_by_endereco(enderecos_to_delete):
	path = os.path.join(DATA_DIR, 'imoveis_data.xlsx')
	if not os.path.exists(path): return {"status": "erro", "mensagem": "Arquivo de dados de imóveis não encontrado."}
	if not enderecos_to_delete: return {"status": "info", "mensagem": "Nenhum imóvel selecionado."}
	df = pd.read_excel(path)
	rows_before = len(df)
	df = df[~df['Endereço'].isin(enderecos_to_delete)]
	rows_after = len(df)
	df.to_excel(path, index=False)
	deleted_count = rows_before - rows_after
	return {"status": "sucesso", "mensagem": f"{deleted_count} imóvel(is) deletado(s) com sucesso!"}

def update_imovel_data(original_endereco, new_data):
	path = os.path.join(DATA_DIR, 'imoveis_data.xlsx')
	if not os.path.exists(path): return {"status": "erro", "mensagem": "Arquivo de dados de imóveis não encontrado."}
	df = pd.read_excel(path)
	imovel_index = df[df['Endereço'] == original_endereco].index
	if not imovel_index.empty:
		idx = imovel_index[0]
		for key, value in new_data.items():
			if value: df.loc[idx, key] = value
		df.to_excel(path, index=False)
		return {"status": "sucesso", "mensagem": "Imóvel atualizado com sucesso!"}
	return {"status": "erro", "mensagem": "Imóvel não encontrado para atualização."}

def filter_imoveis(filters):
	df = safe_read_data('imoveis_data.xlsx')
	if df.empty: return df
	for column, value in filters.items():
		if value:
			df = df[df[column].str.contains(value, case=False, na=False)]
	return df

def add_new_contrato(contrato_data):
	"""
	Adiciona um novo registro de contrato ao arquivo contratos.xlsx.
	'contrato_data' deve ser um dicionário com os dados do contrato.
	"""
	path = os.path.join(DATA_DIR, 'contratos.xlsx')
	
	novo_df = pd.DataFrame([contrato_data])
	
	try:
		if os.path.exists(path):
			df_existente = pd.read_excel(path)
			df_final = pd.concat([df_existente, novo_df], ignore_index=True)
		else:
			df_final = novo_df

		df_final.to_excel(path, index=False)
		return {"status": "sucesso", "mensagem": "Contrato adicionado com sucesso!"}

	except Exception as e:
		return {"status": "erro", "mensagem": f"Erro ao salvar contrato: {e}"}


def get_all_contratos():
	"""
	Lê o arquivo de contratos e retorna todos os dados como um DataFrame.
	"""
	return safe_read_data('contratos.xlsx')