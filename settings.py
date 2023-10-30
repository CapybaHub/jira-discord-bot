from dotenv import load_dotenv

# Load .env file
load_dotenv()

import os

JIRA_PROJECT_URL = str(os.getenv("JIRA_PROJECT_URL"))
JIRA_USER_EMAIL = str(os.getenv("JIRA_USER_EMAIL"))
JIRA_API_TOKEN = str(os.getenv("JIRA_API_TOKEN"))
DISCORD_API_TOKEN = str(os.getenv("DISCORD_API_TOKEN"))

commandPrefixes = ["!"]

availableCommands =  {
        "commands": {
            "description": "Lista os comandos disponíveis",
            "params": [],
            "example": "!commands",
            "aliases": ["comandos", "ajuda"],
        },
        "oi": {
            "description": "Saudação",
            "params": [],
            "example": "!oi",
        },
        "issue": {
            "description": "Busca uma task no Jira",
            "params": ["task-key"],
            "example": "!issue PROJ-123",
            "aliases": ["i", "t", "task"],
        },
        "boards": {
            "description": "Lista os quadros da conta",
            "params": [],
            "example": "!boards",
            "aliases": ["projects", "quadros"],
        },
        "sprints": {
            "description": "Lista as sprints de um quadro",
            "params": ["id-do-quadro"],
            "example": "!sprints 2",
            "aliases": ["s"],
        },
        "current-sprint": {
            "description": "Busca informações da sprint atual de um projeto",
            "params": ["id-do-quadro"],
            "example": "!current-sprint 2",
            "aliases": ["sprint-atual", "sa"],
        },
        "sprint-report": {
            "description": "Busca informações de uma sprint",
            "params": ["id-da-sprint"],
            "example": "!sprint 2",
            "aliases": ["sprint", "sr"],
        },
}
