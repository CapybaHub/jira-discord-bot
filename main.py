import discord
import traceback
from DiscordMessagesHandler import DiscordMessagesHandler
from JiraManager import JiraAPIClient
from settings import (
    DISCORD_API_TOKEN,
    JIRA_API_TOKEN,
    JIRA_PROJECT_URL,
    JIRA_USER_EMAIL,
    commandPrefixes,
)
from CommandsManager import getBOTCommands

jiraAPI = JiraAPIClient(JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)

client = discord.Client(intents=discord.Intents.all())

MessagesHandler = DiscordMessagesHandler(jiraAPI=jiraAPI, discordClient=client)

availableCommands = getBOTCommands(MessagesHandler)

@client.event
async def on_ready():
    print(f"Logado com sucesso como {client.user}")


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
