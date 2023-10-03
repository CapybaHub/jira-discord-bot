import discord
import requests

JIRA_PROJECT_URL = "https://jiradiscord.atlassian.net"
JIRA_USER_EMAIL = ""
JIRA_API_TOKEN = ""
DISCORD_API_TOKEN = ""


class JiraAPIManager:
    def __init__(self, url, email, token):
        self.url = url + "/rest/api/3"
        self.userAuth = email + ":" + token
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def getIssue(self, issueIdOrKey):
        url = self.url + "/issue/" + issueIdOrKey
        response = await requests.request(
            "GET", url, headers=self.headers, auth=(self.userAuth)
        )
        return response.json()


jiraAPI = JiraAPIManager(JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"Logado com sucesso como {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    handleReceivedMessage(message)


async def sayHello(message):
    await message.channel.send(f"Olá {message.author.mention}!")


async def getIssueInfo(commandInfo, message):
    isValid = await validateReceivedParamsFromMessage(commandInfo, message)
    
    if not isValid:
        return
    
    issueIdOrKey = message.content.split()[1]
    issue = await jiraAPI.getIssue(issueIdOrKey)
    print(issue)
    


commandPrefixes = ["!"]
availableCommands = {
    "oi": {
        "description": "Saudação",
        "params": [],
        "example": "!oi",
        "function": sayHello,
    },
    "issue": {
        "description": "Busca uma issue no Jira",
        "params": ["issueIdOrKey"],
        "example": "!issue PROJ-123",
        "function": getIssueInfo,
    },
}


def handleReceivedMessage(message):
    messageContent = message.content.split()

    if len(messageContent) < 1:
        return

    possibleCommand = messageContent[0]

    for commandPrefix in commandPrefixes:
        print(possibleCommand, commandPrefix, possibleCommand.startswith(commandPrefix))
        if possibleCommand.startswith(commandPrefix):
            command = possibleCommand[len(commandPrefix) :]
            if command in availableCommands:
                print("Comando encontrado:", command, availableCommands[command])
                return availableCommands[command]["function"](
                    availableCommands[command], messageContent
                )


async def validateReceivedParamsFromMessage(commandInfo, message):
    if len(message.content.split()) != commandInfo["params"] + 1:
        await message.channel.send(
                f"Parâmetros inválidos. Exemplo: {commandInfo['example']}"
            )
        return False 
    return True


client.run(DISCORD_API_TOKEN)
