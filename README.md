# BOT de Discord para Jira

Gerencie sua equipe utilizando o Discord e o Jira, utilizando esta integração. Isso facilita a inserção de novos membros no fluxo de desenvolvimento e na equipe ágil.

# Canal do Discord

Acesse o nosso canal do Discord pelo convite a baixo:
[https://discord.gg/xjEsUWDUa](https://discord.gg/xjEsUWDUa)

# Instalar (Ubuntu)

Para instalar o projeto, você vai precisar do Python na versão 3.10 ou superior.

- `sudo apt-get install python3.10`

Recomendamos também o uso do pacote python-is-python3

- `sudo apt-get install python-is-python3`

### Instalando as dependencias do projeto

1. Acesse a pasta do projeto
2. Crie um ambiente virtual do python:

   1. `python3 -m venv venv`
3. Acesse o ambiente virtual

   1. `source venv/bin/activate`
4. Instale as dependencias do projeto

   1. `python -m pip install -r requirements.txt`

# Rodando o projeto

Rodamos o projeto através de um arquivo principal, chamado `main.py`, e para roda-lo utilize:

`python main.py`

ou

`python3 main.py`

# Variáveis de ambiente

Temos algumas variáveis de ambiente que são utilizadas no nosso código, para isso, precisamos defini-las em um arquivo .env na raiz do projeto.

Utilize o arquivo `env.example` para visualizar quais as variáveis necessárias.