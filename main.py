import discord
from DiscordMessagesHandler import DiscordMessagesHandler
import traceback
import JiraManager
from settings import (
    DISCORD_API_TOKEN,
    JIRA_API_TOKEN,
    JIRA_PROJECT_URL,
    JIRA_USER_EMAIL,
    commandPrefixes,
    getAvailableCommands,
)

jiraAPI = JiraManager.Client(JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)

client = discord.Client(intents=discord.Intents.all())

MessagesHandler = DiscordMessagesHandler(jiraAPI=jiraAPI, discordClient=client)

availableCommands = getAvailableCommands(MessagesHandler)

from simple_http_server import route, server
    

@route("/")
def index():
    return {"status": "201"}


from simple_http_server import route, server
    

@route("/")
def index():
    return {"status": "201"}


@client.event
async def on_ready():
    jiraAPI.get_projects()

    print(f"Logado com sucesso como {client.user}")

    print('SERVER START')
    server.start(port=80)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    try:
        await handleReceivedMessage(message)
    except Exception as e:
        print(e)
        traceback.print_exc()
        await message.channel.send("Ocorreu um erro ao executar o comando.")


async def handleReceivedMessage(message):
    messageContent = message.content.split()

    if len(messageContent) < 1:
        return

    possibleCommand = messageContent[0]

    for commandPrefix in commandPrefixes:
        print(possibleCommand, commandPrefix, possibleCommand.startswith(commandPrefix))
        if possibleCommand.startswith(commandPrefix):
            command = possibleCommand[len(commandPrefix) :]
            if command in availableCommands:
                print("Comando encontrado:", command)
                print("Available", availableCommands[command])
                print("Message", messageContent)

                return await availableCommands[command]["function"](
                    availableCommands[command], message
                )

print("Starting...")
client.run(DISCORD_API_TOKEN)
