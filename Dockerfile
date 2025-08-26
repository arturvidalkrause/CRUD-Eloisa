# Dockerfile

# 1. Imagem Base
# Usamos uma imagem Python baseada em Debian (Bullseye) que contém mais
# ferramentas de sistema do que a versão 'slim' ou 'alpine', o que facilita
# a instalação de dependências para GUI.
FROM python:3.10-bullseye

# 2. Instalação de Dependências do Sistema
# CustomTkinter (e Tkinter em geral) precisa de bibliotecas do sistema para
# renderizar a interface gráfica. Aqui instalamos o Tcl/Tk e bibliotecas do X11,
# que permitem que a GUI do contêiner se comunique com o servidor X da sua máquina host.
RUN apt-get update && apt-get install -y \
	python3-tk \
	tcl-tls \
	libx11-6 \
	&& rm -rf /var/lib/apt/lists/*

# 3. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Copia e instala as dependências Python
# Copiamos primeiro o requirements.txt para aproveitar o cache do Docker.
# Se este arquivo não mudar, o Docker não reinstalará as bibliotecas a cada build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código do projeto
COPY . .

# 6. Comando para executar a aplicação
# Substitua "seu_script.py" pelo nome do seu arquivo Python principal.
CMD ["python", "seu_script.py"]