from datetime import datetime
import random

datetimeFormat = "%d/%m/%Y %H:%M:%S"

def generateRandomDiscordColor():
    return random.randint(0, 0xFFFFFF)


def getProjectUrlFromKey(jiraProjectUrl: str, projectKey: str):
    return f"{jiraProjectUrl}/projects/{projectKey}"