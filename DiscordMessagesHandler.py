import json
import discord

from utils import generateRandomDiscordColor, getProjectUrlFromKey


async def validateReceivedParamsFromMessage(commandInfo, message):
    print("validateReceivedParamsFromMessage", message, message.content)
    if len(message.content.split()) != len(commandInfo["params"]) + 1:
        await message.channel.send(
            f"Parâmetros inválidos. Exemplo: {commandInfo['example']}"
        )
        return False
    return True


class DiscordMessagesHandler:
    jiraAPI = None
    discordClient = None

    def __init__(self, jiraAPI, discordClient):
        self.jiraAPI = jiraAPI
        self.discordClient = discordClient

    async def sayHello(self, message):
        await message.channel.send(f"Olá {message.author.mention}!")

    async def getIssueInfo(self, commandInfo, message):
        # print(message, message.content, commandInfo)
        isValid = await validateReceivedParamsFromMessage(commandInfo, message)

        if not isValid:
            return

        params = message.content.split()[1:]
        functionParams = {
            key for key in commandInfo["params"] for param in params.pop(0)
        }
        print(functionParams)
        issueIdOrKey = message.content.split()[1]
        issue = self.jiraAPI.getIssue(issueIdOrKey)
        print(issue)

    async def listProjects(self, commandInfo, message):
        projects = self.jiraAPI.get_projects()

        projectsData = {}

        for project in projects["values"]:
            projectsData[project["key"]] = {
                "name": project["name"],
                "image": project["avatarUrls"]["48x48"],
                "key": project["key"],
                "type": project["projectTypeKey"],
                "id": project["id"],
                "isPrivate": project["isPrivate"],
                "url": project["self"],
            }

        for project in projectsData:
            projectEmbed = discord.Embed(
                title=f'({projectsData[project]["key"]}) - {projectsData[project]["name"]}',
                url=getProjectUrlFromKey(
                    self.jiraAPI.project_url, projectsData[project]["key"]
                ),
                color=generateRandomDiscordColor(),
            )
            projectEmbed.set_thumbnail(url=projectsData[project]["image"])
            projectEmbed.set_image(url=projectsData[project]["image"])
            projectEmbed.add_field(
                name="Tipo", value=projectsData[project]["type"], inline=True
            )
            projectEmbed.add_field(
                name="Privacidade",
                value="Privado" if projectsData[project]["isPrivate"] else "Público",
                inline=True,
            )
            projectEmbed.add_field(name="ID", value=projectsData[project]["id"])

            projectsData[project]["embed"] = projectEmbed

        allEmbeds = [projectsData[project]["embed"] for project in projectsData]
        showEmbeds = allEmbeds[:10]
        remainingEmbeds = allEmbeds[10:]

        await message.reply(
            embeds=showEmbeds,
            content=f"**É claro, aqui estão seus projetos:** \n\n*Contagem de projetos: {len(projectsData)}* \n \n",
        )

    async def listTasks(self, commandInfo, message):
        print(commandInfo)
        tasks = self.jiraAPI.get_tasks(commandInfo)
        print(tasks)

        tasksData = {}

    async def listBoards(self, commandInfo, message):
        print(commandInfo)
        tasks = self.jiraAPI.get_board_list(commandInfo)
        print(tasks)

        tasksData = {}

    async def listSprints(self, commandInfo, message):
        print(commandInfo)
        sprints = self.jiraAPI.get_sprint_list(commandInfo)
        print(sprints)

        await message.reply(
            content=f"**É claro, aqui estão suas sprints:** \n\n*Contagem de sprints: {len(sprints)}* \n \n",
        )
