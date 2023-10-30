import discord
from JiraClasses import Sprint
from JiraManager import JiraAPIClient

from settings import availableCommands, commandPrefixes

from utils import (
    generateRandomDiscordColor,
    getFormattedDateAndTimeFromISO,
    getFormattedDateFromDatetime,
    getProjectUrlFromKey,
)

async def validateReceivedParamsFromMessage(commandInfo, message):
    if len(message.content.split()) != len(commandInfo["params"]) + 1:
        errorMessage = (
            f"Parâmetros inválidos.\nOs parâmetros esperados são: \n"
            + "\n".join([f"- {command}" for command in commandInfo["params"]])
            + f"\nExemplo: {commandInfo['example']}"
        )
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
            if sprint["state"] == "active":
                currentSprint = sprint
                break

        if currentSprint:
            return Sprint(currentSprint)
        else:
            return None
        
    async def listAvailableCommands(self, commandInfo, message):        
        commandsEmbed = discord.Embed(
            title="Comandos disponíveis",
            color=generateRandomDiscordColor(),
        )

        for command in availableCommands:
            if "aliases" in availableCommands[command]:
                aliasesListWithPrefix = [
                    f"{commandPrefixes[0]}{alias}"
                    for alias in availableCommands[command]["aliases"]
                    if availableCommands[command]["aliases"]
                ]
            else:
                aliasesListWithPrefix = []    
            
            commandAliases = f"Atalhos: {', '.join(aliasesListWithPrefix)}\n" if aliasesListWithPrefix else "" 
            commandExamples = f"*Exemplo:* {availableCommands[command]['example']}\n" if "example" in availableCommands[command] else ""
            commandsEmbed.add_field(
                name=f"**{commandPrefixes[0]}{command}**",
                value=f"{availableCommands[command]['description']}\n\n{commandAliases}{commandExamples}",
                inline=False,
            )

        await message.reply(
            embed=commandsEmbed,
            content=f"**É claro, aqui estão seus comandos disponíveis:** \n \n",
        )

    async def sayHello(self, commandInfo, message):
        await message.channel.send(f"Olá {message.author.mention}!")

    async def getIssueInfo(self, commandInfo, message):
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

        current_sprint = await self._getCurrentSprint(int(params["id-do-quadro"]))

        sprintInfoEmbed = discord.Embed(
            title=f"{current_sprint.name}",
            color=generateRandomDiscordColor(),
        )

        sprintInfoEmbed.add_field(
            name="ID da sprint", value=current_sprint.id, inline=False
        )
        sprintInfoEmbed.add_field(
            name="Data de início da sprint",
            value=getFormattedDateFromDatetime(current_sprint.startDate),
            inline=False,
        )
        sprintInfoEmbed.add_field(
            name="Data de término da sprint",
            value=getFormattedDateFromDatetime(current_sprint.endDate),
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
            content=f"**É claro, aqui estão seus quadros do Jira:** \n\n*Contagem de projetos: {len(projectsData)}* \n \n",
        )

    async def listSprints(self, commandInfo, message: discord.Message):
        params = await getParamsFromValidMessage(commandInfo, message)

        sprints = self.jiraAPI.get_sprint_list(params["id-do-quadro"])

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
                value=getFormattedDateAndTimeFromISO(sprint["startDate"]).split()[0],
                inline=False,
            )
            sprintEmbed.add_field(
                name="Data de término da sprint",
                value=getFormattedDateAndTimeFromISO(sprint["endDate"]).split()[0],
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

        tasks_per_category = {}

        for task in sprint_tasks.issues:
            current_task_category = task.getCurrentStatus()
            if current_task_category not in tasks_per_category:
                tasks_per_category[current_task_category] = []
            tasks_per_category[current_task_category].append(task)

        conclusionPercentage = round(
            len(tasks_per_category["Concluído"]) / len(sprint_tasks.issues) * 100,
            2,
        )

        sprintEmbed = discord.Embed(
            title=sprint.name,
            color=generateRandomDiscordColor(),
        )

        sprintEmbed.add_field(name="ID", value=sprint.id, inline=True)
        sprintEmbed.add_field(
            name="Duração", value=f"{sprint.getSprintDuration()} dias", inline=True
        )
        sprintEmbed.add_field(
            name="Iniciado há", value=f"{sprint.getDaysPassed()} dias", inline=True
        )

        sprintEmbed.add_field(name="", value="", inline=False)

        sprintEmbed.add_field(name="Tasks por categoria", value="", inline=False)
        for category in tasks_per_category:
            sprintEmbed.add_field(
                name=category, value=len(tasks_per_category[category]), inline=True
            )

        sprintEmbed.add_field(name="", value="", inline=False)
        sprintEmbed.add_field(name="Status da sprint", value="", inline=False)
        sprintEmbed.add_field(
            name="Porcentagem de conclusão",
            value=f"{conclusionPercentage}%",
            inline=True,
        )

        sprintEmbed.add_field(
            name="Dias restantes",
            value=f"{sprint.getDaysRemaining()} dias",
            inline=True,
        )

        await message.reply(
            content=f"**É claro, aqui está seu relatório de sprint:** \n \n",
            embed=sprintEmbed,
        )
