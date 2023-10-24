import random


def generateRandomDiscordColor():
    return random.randint(0, 0xFFFFFF)


def getProjectUrlFromKey(jiraProjectUrl, projectKey):
    return f"{jiraProjectUrl}/projects/{projectKey}"
