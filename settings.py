import os
from os.path import exists
from dotenv import load_dotenv
import pickle

# Load .env file
load_dotenv()

JIRA_PROJECT_URL = str(os.getenv("JIRA_PROJECT_URL"))
JIRA_USER_EMAIL = str(os.getenv("JIRA_USER_EMAIL"))
JIRA_API_TOKEN = str(os.getenv("JIRA_API_TOKEN"))
DISCORD_API_TOKEN = str(os.getenv("DISCORD_API_TOKEN"))
ALLOWED_CHANNEL_IDS = str(os.getenv("ALLOWED_CHANNEL_IDS")).split(',')

commandPrefix = "!"

# Funções utilitárias para utilizar o Pickle
def load_pickle(default, filename):
    # Caso o arquivo existir, retorna o objeto dentro dele
    if exists(f"{filename}.pickle"):
        with open(f"{filename}.pickle", "rb") as f:
            return pickle.load(f)
    # Caso contrário, cria o arquivo e retorna o valor padrão para esta variável
    else:
        with open(f"{filename}.pickle", "wb") as f:
            pickle.dump(default, f)
            return default


def save_pickle(obj, filename):
    with open(f"./{filename}.pickle", "wb") as f:
        pickle.dump(obj, f)
