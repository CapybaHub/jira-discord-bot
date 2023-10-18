
async def validateReceivedParamsFromMessage(commandInfo, message):
    print("validateReceivedParamsFromMessage", message, message.content)
    if len(message.content.split()) != len(commandInfo["params"]) + 1:
        await message.channel.send(
            f"Parâmetros inválidos. Exemplo: {commandInfo['example']}"
        )
        return False
    return True


class DiscordMessagesHandler:
    def __init__(self, jiraAPI, discordClient):
        self.jiraAPI = jiraAPI
        self.discordClient = discordClient

    async def sayHello(self, message):
        await message.channel.send(f"Olá {message.author.mention}!")


    async def getIssueInfo(self,commandInfo, message):
        # print(message, message.content, commandInfo)
        isValid = await validateReceivedParamsFromMessage(commandInfo, message)

        if not isValid:
            return
        
        
        params = message.content.split()[1:]
        functionParams = {key for key in commandInfo['params'] for param in params.pop(0)}
        print(functionParams) 
        issueIdOrKey = message.content.split()[1]
        issue = await self.jiraAPI.getIssue(issueIdOrKey)
        print(issue)
        
    async def listProjects(self, commandInfo, message):
        projects = await self.jiraAPI.get_projects()
        print(projects)
        await message.channel.send(f"Olá {message.author.mention}!")
        for project in projects:
            await message.channel.send(f"Projeto: {project['name']}")