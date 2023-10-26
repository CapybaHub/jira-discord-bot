from dotenv import load_dotenv

from DiscordMessagesHandler import DiscordMessagesHandler

# Load .env file
load_dotenv()

import os

JIRA_PROJECT_URL = str(os.getenv("JIRA_PROJECT_URL"))
JIRA_USER_EMAIL = str(os.getenv("JIRA_USER_EMAIL"))
JIRA_API_TOKEN = str(os.getenv("JIRA_API_TOKEN"))
DISCORD_API_TOKEN = str(os.getenv("DISCORD_API_TOKEN"))

commandPrefixes = ["!"]

def getAvailableCommands(MessageHandler: DiscordMessagesHandler):
    base_commands = {
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
        "boards": {
            "description": "Lista os quadros da conta",
            "params": [],
            "example": "!projects",
            "function": MessageHandler.listBoards,
            "aliases": ["projects", "quadros"],
        },
        # "tasks": {
        #     "description": "Lista as tasks de um projeto",
        #     "params": ["projectKey"],
        #     "example": "!tasks PROJ",
        #     "function": MessageHandler.listTasks,
        # },
        "sprints": {
            "description": "Lista as sprints de um projeto",
            "params": ["id-do-quadro"],
            "example": "!sprints 2",
            "function": MessageHandler.listSprints,
        },
        "current-sprint": {
            "description": "Busca informações da sprint atual de um projeto",
            "params": ["id-do-quadro"],
            "example": "!current-sprint 2",
            "function": MessageHandler.getCurrentSprintInfo,
            "aliases": ["sprint-atual", 'sa'],
        },
        "sprint-report": {
            "description": "Busca informações de uma sprint",
            "params": ["id-da-sprint"],
            "example": "!sprint 2",
            "function": MessageHandler.getSprintReport,
            "aliases": ["sprint", 'sr'],
        },
    }
    
    commands_with_aliases = {}
    
    for command in base_commands:
        commands_with_aliases[command] = base_commands[command]
        
        if "aliases" in base_commands[command]:
            for alias in base_commands[command]["aliases"]:
                commands_with_aliases[alias] = base_commands[command]

    return  commands_with_aliases
