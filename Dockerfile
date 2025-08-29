FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y \
	python3-tk \
	tcl-tls \
	libx11-6 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "seu_script.py"]