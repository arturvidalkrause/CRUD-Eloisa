# Sistema de Gestão de Imóveis A4G

Este é um sistema de desktop desenvolvido em Python para a gestão de dados de imóveis, contratos e clientes, permitindo operações de CRUD (Criar, Ler, Atualizar, Deletar) de forma visual e intuitiva.

## Descrição

O projeto utiliza a biblioteca **CustomTkinter** para criar uma interface gráfica moderna e responsiva, e **Pandas** para a manipulação e persistência dos dados em arquivos Excel, servindo como um banco de dados local. A aplicação conta com um sistema de autenticação de usuários, um dashboard com indicadores e gráficos, e módulos para gerenciamento de clientes e imóveis.

## Funcionalidades Implementadas

* **Sistema de Autenticação:** Telas de Login e Registro com validação de credenciais salvas em um arquivo Excel.
* **Dashboard Interativo:** Exibição de KPIs (Key Performance Indicators) e gráficos (pizza e barras) gerados com Matplotlib a partir dos dados do sistema.
* **Gestão de Perfil:** O usuário logado pode visualizar e atualizar suas informações de cadastro.
* **CRUD de Clientes:** Visualização de clientes em tabela e funcionalidade de exclusão em massa.
* **CRUD de Imóveis:**
    * Visualização de imóveis em tabela.
    * Formulário para adicionar novos imóveis.
    * Formulário para atualizar imóveis existentes.
    * Funcionalidade de exclusão em massa.
* **Importação de Dados:** Tela para carregar arquivos de dados (.xlsx, .csv) para dentro do sistema.
* **Configurações da Aplicação:** Opção para alternar entre os temas Claro (Light) e Escuro (Dark) em tempo real.

## Tecnologias Utilizadas

* **Python**
* **CustomTkinter:** Para a construção da interface gráfica.
* **Pandas:** Para manipulação e armazenamento de dados em arquivos Excel.
* **Matplotlib:** Para a criação e exibição de gráficos no Dashboard.

## Estrutura de Arquivos de Dados

O sistema espera encontrar os seguintes arquivos (que podem ser carregados pela tela "Adicionar dados") na pasta `app/data/`:

* `database_usuarios.xlsx`: Armazena os dados de login dos usuários.
* `imoveis_data.xlsx`: Armazena os dados dos imóveis.
* `contratos.xlsx`: Armazena os dados dos contratos para os KPIs e gráficos.

## Como Instalar e Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [git@github.com:arturvidalkrause/CRUD-Eloisa.git](git@github.com:arturvidalkrause/CRUD-Eloisa.git)
    cd APP
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Instale as dependências:**
    Certifique-se de que o arquivo `requirements.txt` está na pasta raiz e execute:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python app/main.py
    ```

## Uso

Ao iniciar a aplicação, você será apresentado à tela de login.
1.  Caso não tenha um usuário, utilize a tela de **Registro** para criar um. As informações serão salvas em `app/data/database_usuarios.xlsx`.
2.  Faça **Login** com as credenciais criadas.
3.  Navegue pelas diferentes seções do sistema utilizando a barra de menu lateral.