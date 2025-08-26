import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database_usuarios.xlsx')

def criar_novo_registro(nome, sobrenome, cpf, email, senha):
	"""
	Recebe os dados do novo usuário, valida e salva em um arquivo Excel.
	"""
	if not all([nome, sobrenome, cpf, email, senha]):
		print("Erro: Todos os campos devem ser preenchidos!")
		return {"status": "erro", "mensagem": "Todos os campos são obrigatórios."}

	novo_usuario = {
		"Nome": [nome],
		"Sobrenome": [sobrenome],
		"CPF": [cpf],
		"Email": [email],
		"Senha": [senha]
	}
	novo_df = pd.DataFrame(novo_usuario)

	try:
		if os.path.exists(DATA_PATH):
			df_existente = pd.read_excel(DATA_PATH)
			df_final = pd.concat([df_existente, novo_df], ignore_index=True)
		else:
			df_final = novo_df

		df_final.to_excel(DATA_PATH, index=False)

		print("\n--- Registro salvo no Excel com Sucesso! ---")
		print(f"Caminho do arquivo: {DATA_PATH}")
		
		return {"status": "sucesso", "mensagem": "Usuário registrado com sucesso!"}

	except Exception as e:
		print(f"Ocorreu um erro ao salvar no Excel: {e}")
		return {"status": "erro", "mensagem": f"Erro ao salvar dados: {e}"}
	
def autenticar_usuario(email, senha):
	"""
	Verifica se um usuário com o email e senha fornecidos existe no arquivo Excel.
	"""
	if not os.path.exists(DATA_PATH):
		return False

	df = pd.read_excel(DATA_PATH)
	
	usuario_encontrado = df[df['Email'] == email]

	if not usuario_encontrado.empty:
		dados_usuario = usuario_encontrado.iloc[0]
		if dados_usuario['Senha'] == senha:
			return True
			
	return False

def get_user_data(email):
	"""
	Busca e retorna os dados de um usuário específico pelo email.
	"""
	if not os.path.exists(DATA_PATH):
		return None

	df = pd.read_excel(DATA_PATH)
	usuario_encontrado = df[df['Email'] == email]

	if not usuario_encontrado.empty:
		return usuario_encontrado.iloc[0].to_dict()
	
	return None

def update_user_data(email, new_data):
	"""
	Atualiza os dados de um usuário no arquivo Excel.
	"""
	if not os.path.exists(DATA_PATH):
		return {"status": "erro", "mensagem": "Arquivo de dados não encontrado."}

	df = pd.read_excel(DATA_PATH)
	
	user_index = df[df['Email'] == email].index

	if not user_index.empty:
		for key, value in new_data.items():
			df.loc[user_index, key] = value
		
		df.to_excel(DATA_PATH, index=False)
		return {"status": "sucesso", "mensagem": "Dados atualizados com sucesso!"}

	return {"status": "erro", "mensagem": "Usuário não encontrado para atualização."}	

def get_all_clients():
	"""
	Lê o arquivo de usuários e retorna todos os dados como um DataFrame.
	"""
	return safe_read_excel('database_usuarios.xlsx')

def delete_clients_by_cpf(cpfs_to_delete):
	"""
	Deleta um ou mais clientes do arquivo Excel com base em uma lista de CPFs.
	"""
	if not os.path.exists(DATA_PATH):
		return {"status": "erro", "mensagem": "Arquivo de dados não encontrado."}
	
	if not cpfs_to_delete:
		return {"status": "info", "mensagem": "Nenhum cliente selecionado."}

	df = pd.read_excel(DATA_PATH)
	
	rows_before = len(df)
	
	df = df[~df['CPF'].isin(cpfs_to_delete)]
	
	rows_after = len(df)

	df.to_excel(DATA_PATH, index=False)
	
	deleted_count = rows_before - rows_after
	return {"status": "sucesso", "mensagem": f"{deleted_count} cliente(s) deletado(s) com sucesso!"}

def get_all_imoveis():
	"""
	Lê o arquivo de imóveis e retorna todos os dados como um DataFrame.
	"""
	return safe_read_excel('imoveis_data.xlsx')

def add_new_imovel(imovel_data):
	"""
	Adiciona um novo registro de imóvel ao arquivo imoveis_data.xlsx.
	'imovel_data' deve ser um dicionário com os dados do imóvel.
	"""
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

def delete_imoveis_by_endereco(enderecos_to_delete):
	"""
	Deleta um ou mais imóveis do arquivo Excel com base em uma lista de endereços.
	"""
	path = os.path.join(DATA_DIR, 'imoveis_data.xlsx')
	if not os.path.exists(path):
		return {"status": "erro", "mensagem": "Arquivo de dados de imóveis não encontrado."}
	
	if not enderecos_to_delete:
		return {"status": "info", "mensagem": "Nenhum imóvel selecionado."}

	df = pd.read_excel(path)
	rows_before = len(df)
	
	df = df[df['Endereço'].isin(enderecos_to_delete)]
	
	rows_after = len(df)
	df.to_excel(path, index=False)
	
	deleted_count = rows_before - rows_after
	return {"status": "sucesso", "mensagem": f"{deleted_count} imóvel(is) deletado(s) com sucesso!"}

def update_imovel_data(original_endereco, new_data):
	"""
	Atualiza os dados de um imóvel específico, identificado pelo endereço original.
	"""
	path = os.path.join(DATA_DIR, 'imoveis_data.xlsx')
	if not os.path.exists(path):
		return {"status": "erro", "mensagem": "Arquivo de dados de imóveis não encontrado."}

	df = pd.read_excel(path)
	
	imovel_index = df[df['Endereço'] == original_endereco].index

	if not imovel_index.empty:
		idx = imovel_index[0]
		
		for key, value in new_data.items():
			if value:
				df.loc[idx, key] = value
		
		df.to_excel(path, index=False)
		return {"status": "sucesso", "mensagem": "Imóvel atualizado com sucesso!"}

	return {"status": "erro", "mensagem": "Imóvel não encontrado para atualização."}

def filter_imoveis(filters):
	"""
	Filtra o DataFrame de imóveis com base em um dicionário de filtros.
	"""
	df = safe_read_excel('imoveis_data.xlsx')
	if df.empty:
		return df

	for column, value in filters.items():
		if value:
			df = df[df[column].str.contains(value, case=False, na=False)]
	
	return df