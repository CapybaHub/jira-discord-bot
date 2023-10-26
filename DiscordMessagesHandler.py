import json
import discord
from JiraManager import JiraAPIClient
from datetime import datetime

from utils import generateRandomDiscordColor, getProjectUrlFromKey


async def validateReceivedParamsFromMessage(commandInfo, message):
    print(
        "validateReceivedParamsFromMessage",
        message.content,
        len(message.content.split()),
        len(commandInfo["params"]) + 1,
    )
    if len(message.content.split()) != len(commandInfo["params"]) + 1:
        errorMessage = f"Parâmetros inválidos.\nOs parâmetros esperados são: \n" + "\n".join([f"- {command}" for command in commandInfo['params']]) + f"\nExemplo: {commandInfo['example']}"
        await message.channel.send(errorMessage)

        return Exception(errorMessage)
    return True


async def getParamsFromValidMessage(commandInfo, message):
    isValid = await validateReceivedParamsFromMessage(commandInfo, message)

    if not isValid:
        return

    params = message.content.split()[1:]

    paramsByName = {}

    for param in commandInfo["params"]:
        paramsByName[param] = params.pop(0)

    return paramsByName


def getDatetimeFromIsoFormatWithZ(isoFormat):
    return datetime.fromisoformat(isoFormat.replace("Z", "+00:00"))


def getFormattedDate(date):
    return getDatetimeFromIsoFormatWithZ(date).strftime("%d/%m/%Y %H:%M:%S")


class View(
    discord.ui.View
):  # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(
        label="Click me!", style=discord.ButtonStyle.primary, emoji="😎"
    )  # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button")


class DiscordMessagesHandler:
    jiraAPI = None
    discordClient = None

    def __init__(self, jiraAPI: JiraAPIClient, discordClient: discord.Client):
        self.jiraAPI = jiraAPI
        self.discordClient = discordClient

    async def _getCurrentSprint(self, board_id):
        all_sprints = self.jiraAPI.get_sprint_list(board_id)

        currentSprint = None
        for sprint in all_sprints["values"]:
            print(sprint)
            if sprint["state"] == "active":
                currentSprint = sprint
                break

        if currentSprint:
            return currentSprint
        else:
            return None

    async def sayHello(self, commandInfo, message):
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

    async def getCurrentSprintInfo(self, commandInfo, message: discord.Message):
        params = await getParamsFromValidMessage(commandInfo, message)

        print(params.items(), params['id-do-quadro'])
        current_sprint = await self._getCurrentSprint(int(params["id-do-quadro"]))

        print("current_sprint", current_sprint)

        sprintInfoEmbed = discord.Embed(
            title=f'{current_sprint["name"]}',
            color=generateRandomDiscordColor(),
        )

        sprintInfoEmbed.add_field(
            name="ID da sprint", value=current_sprint["id"], inline=False
        )
        sprintInfoEmbed.add_field(
            name="Data de início da sprint",
            value=getFormattedDate(current_sprint["startDate"]).split()[0],
            inline=False,
        )
        sprintInfoEmbed.add_field(
            name="Data de término da sprint",
            value=getFormattedDate(current_sprint["endDate"]).split()[0],
            inline=False,
        )

        await message.reply(
            content=f"**É claro, aqui está sua sprint atual:**\n \n",
            embed=sprintInfoEmbed,
        )

    async def listBoards(self, commandInfo, message):
        projects = self.jiraAPI.get_board_list()

        projectsData = {}

        for project in projects["values"]:
            projectsData[project["location"]["projectKey"]] = {
                "name": project["name"],
                "image": project["location"]["avatarURI"],
                "key": project["location"]["projectKey"],
                "type": project["type"],
                "id": project["id"],
                "id-do-quadro": project["location"]["id-do-quadro"],
                "projectName": project["location"]["displayName"],
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
            # projectEmbed.set_image(url=projectsData[project]["image"])
            projectEmbed.add_field(
                name="ID do quadro", value=projectsData[project]["id"], inline=False
            )
            projectEmbed.add_field(
                name="Chave do quadro", value=projectsData[project]["key"], inline=False
            )
            projectEmbed.add_field(
                name="Nome do projeto",
                value=projectsData[project]["projectName"],
                inline=False,
            )

            projectsData[project]["embed"] = projectEmbed

        allEmbeds = [projectsData[project]["embed"] for project in projectsData]
        showEmbeds = allEmbeds[:10]

        await message.reply(
            embeds=showEmbeds,
            # view=View.to_components(self=self),
            content=f"**É claro, aqui estão seus quadros do Jira:** \n\n*Contagem de projetos: {len(projectsData)}* \n \n",
        )

    async def listSprints(self, commandInfo, message: discord.Message):
        params = await getParamsFromValidMessage(commandInfo, message)

        sprints = self.jiraAPI.get_sprint_list(params["id-do-quadro"])
        print(sprints)

        sprintEmbeds = []

        for sprint in sprints["values"]:
            sprintEmbed = discord.Embed(
                title=f'{sprint["name"]}',
                color=generateRandomDiscordColor(),
            )

            if sprint["state"] == "active":
                sprintEmbed.title += " (Sprint atual)"

            sprintEmbed.add_field(name="ID da sprint", value=sprint["id"], inline=False)
            sprintEmbed.add_field(
                name="Data de início da sprint",
                value=getFormattedDate(sprint["startDate"]).split()[0],
                inline=False,
            )
            sprintEmbed.add_field(
                name="Data de término da sprint",
                value=getFormattedDate(sprint["endDate"]).split()[0],
                inline=False,
            )

            sprintEmbeds.append(sprintEmbed)

        await message.reply(
            content=f"**É claro, aqui estão suas sprints:** \n\n*Contagem de sprints: {len(sprintEmbeds)}* \n \n",
            embeds=sprintEmbeds,
        )

    async def getSprintReport(self, commandInfo, message: discord.Message):
        params = await getParamsFromValidMessage(commandInfo, message)

        sprint = self.jiraAPI.get_sprint_data(params["id-da-sprint"])
        
        sprint_tasks = self.jiraAPI.get_tasks_in_sprint(params["id-da-sprint"])
        print(sprint, sprint_tasks)
        # sprint_burndown = self.jiraAPI.get_sprint_burndown(params["id-da-sprint"])

        # print(sprint_burndown)

        sprintEmbed = discord.Embed(
            title=f'{sprint["name"]}',
            color=generateRandomDiscordColor(),
        )

        sprintEmbed.add_field(name="ID da sprint", value=sprint["id"], inline=False)
        sprintEmbed.add_field(
            name="Data de início da sprint",
            value=getFormattedDate(sprint["startDate"]).split()[0],
            inline=False,
        )
        sprintEmbed.add_field(
            name="Data de término da sprint",
            value=getFormattedDate(sprint["endDate"]).split()[0],
            inline=False,
        )

        await message.reply(
            content=f"**É claro, aqui está seu relatório de sprint:** \n \n",
            embed=sprintEmbed,
        )