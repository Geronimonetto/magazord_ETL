# Use uma imagem base Python mais completa
FROM python:3.13


RUN apt-get update

RUN apt-get install nano -y

RUN apt-get install iputils-ping -y

RUN apt-get install telnet -y

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências para o container
COPY . . 

# Crie o ambiente virtual e instale as dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

