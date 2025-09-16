import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def safe_read_data(base_filename):
    csv_path = os.path.join(DATA_DIR, f"{base_filename}.csv")
    xlsx_path = os.path.join(DATA_DIR, f"{base_filename}.xlsx")
    path_to_read = None
    if os.path.exists(csv_path): path_to_read = csv_path
    elif os.path.exists(xlsx_path): path_to_read = xlsx_path
    else: return pd.DataFrame()
    try:
        if path_to_read.endswith('.csv'): return pd.read_csv(path_to_read)
        else: return pd.read_excel(path_to_read)
    except Exception as e:
        print(f"Erro ao ler o arquivo {path_to_read}: {e}")
        return pd.DataFrame()

def get_kpi_data():
    df_imoveis = safe_read_data('imoveis_data')
    df_contratos = safe_read_data('contratos')
    df_usuarios = safe_read_data('database_usuarios')
    if not df_contratos.empty and 'Valor do Aluguel' in df_contratos.columns:
        receita_media = df_contratos['Valor do Aluguel'].mean()
        receita_media_str = f"R$ {receita_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else: receita_media_str = "N/A"
    kpi_data = {"receita_media": receita_media_str, "rentabilidade": "36,2%", "num_imoveis": len(df_imoveis), "num_clientes": len(df_usuarios), "num_contratos": len(df_contratos)}
    return kpi_data

def get_tipos_contrato_data():
    df_contratos = safe_read_data('contratos')
    if not df_contratos.empty and 'Tipo de Contrato' in df_contratos.columns: return df_contratos['Tipo de Contrato'].value_counts()
    return pd.Series({"Exemplo": 1})

def get_area_atuacao_data():
    df_imoveis = safe_read_data('imoveis_data')
    if not df_imoveis.empty and 'Zona' in df_imoveis.columns: return df_imoveis['Zona'].value_counts()
    return pd.Series({"Exemplo": 1})

def get_vacancia_data():
    df_contratos = safe_read_data('contratos')
    if not df_contratos.empty and 'Data de Início' in df_contratos.columns:
        df_contratos['Data de Início'] = pd.to_datetime(df_contratos['Data de Início'], errors='coerce')
        df_contratos.dropna(subset=['Data de Início'], inplace=True)
        contratos_por_mes = df_contratos['Data de Início'].dt.strftime('%b').value_counts()
        meses_pt = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        return contratos_por_mes.reindex(meses_pt, fill_value=0)
    return pd.Series({"Exemplo": 1})

def get_inadimplencia_data():
    data = {'Comercial': 85, 'Residencial': 40, 'Long Stay': 30, 'Outros': 15}
    return pd.Series(data)