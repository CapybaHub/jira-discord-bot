from dotenv import load_dotenv

# Load .env file
load_dotenv()

import os

JIRA_PROJECT_URL = str(os.getenv("JIRA_PROJECT_URL"))
JIRA_USER_EMAIL = str(os.getenv("JIRA_USER_EMAIL"))
JIRA_API_TOKEN = str(os.getenv("JIRA_API_TOKEN"))
DISCORD_API_TOKEN = str(os.getenv("DISCORD_API_TOKEN"))

commandPrefixes = ["!"]


def getAvailableCommands(MessageHandler):
    return {
        "oi": {
            "description": "Saudação",
            "params": [],
            "example": "!oi",
            "function": MessageHandler.sayHello,
        },
        "issue": {
            "description": "Busca uma issue no Jira",
            "params": ["issueIdOrKey"],
            "example": "!issue PROJ-123",
            "function": MessageHandler.getIssueInfo,
        },
        "projects": {
            "description": "Lista os projetos da conta",
            "params": [],
            "example": "!projects",
            "function": MessageHandler.listProjects,
        },
    }
