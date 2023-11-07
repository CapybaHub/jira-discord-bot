import discord
from DiscordClient import DiscordClient
from JiraClient import JiraAPIClient
from settings import DISCORD_API_TOKEN, JIRA_API_TOKEN, JIRA_PROJECT_URL, JIRA_USER_EMAIL, load_pickle, save_pickle
from utils import (
    getFormattedDateFromDatetime,
    getProjectUrlFromKey,
    generateRandomDiscordColor,
)
from simple_http_server import server


JiraClient = JiraAPIClient(
    JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN
)

user_selected_board = load_pickle({}, "user_selected_board")

async def getCurrentBoardID(message: discord.Message):
    currentBoard = (
        user_selected_board[message.author.id]
        if message.author.id in user_selected_board
        else None
    )

    if not currentBoard:
        await message.reply(
            "Ei, você ainda não selecionou um quadro! Para selecionar um quadro, digite: `!selectBoard <ID do quadro>`"
        )
        return None

    return currentBoard


@DiscordClient.command()
async def boards(message: discord.Message):
    boards = JiraClient.get_all_boards()

    for board in boards:
        boardEmbed = discord.Embed(
            title=board.fullName,
            url=getProjectUrlFromKey(JiraClient.project_url, board.key),
            color=generateRandomDiscordColor(),
        )
        boardEmbed.add_field(name="ID do quadro", value=board.id, inline=False)
        boardEmbed.add_field(name="Chave do quadro", value=board.key, inline=False)

        board.embed = boardEmbed

    allEmbeds = [project.embed for project in boards]
    showEmbeds = allEmbeds[:10]  # Somente é possível retornar 10 embeds por vez

    currentBoardID = await getCurrentBoardID(message)

    currentBoardText = (
        f"*Atualmente o quadro selecionado é o de ID:* `{currentBoardID}` \n \n"
        if currentBoardID
        else ""
    )

    await message.reply(
        embeds=showEmbeds,
        content=f"**É claro, aqui estão seus quadros do Jira:** \n\n*Contagem de projetos: {len(boards)}* \n \n *Para selecionar um quadro, digite:* `{DiscordClient.command_prefix}selectBoard <ID do quadro>` \n \n {currentBoardText}",
    )


@DiscordClient.command()
async def selectBoard(message: discord.Message, *boardIDS):
    if len(boardIDS) != 1 or not boardIDS[0].isdigit():
        await message.reply(
            "Ei, você precisa passar (somente) o ID do quadro que deseja selecionar!"
        )

    boardID = boardIDS[0]

    allBoards = JiraClient.get_all_boards()

    boardsIDList = [board.id for board in allBoards]

    if not int(boardID) in boardsIDList:
        await message.reply(
            f"Ei, o ID {boardID} não corresponde a nenhum quadro do seu Jira!"
        )

    user_selected_board[message.author.id] = boardID
    save_pickle(user_selected_board, "user_selected_board")
    await message.reply(f"Quadro selecionado com sucesso!")


@DiscordClient.command()
async def currentBoard(message: discord.Message):
    currentBoardID = await getCurrentBoardID(message)

    if currentBoardID == None:
        return

    await message.reply(f"O quadro selecionado atualmente é o de ID: `{currentBoardID}`")


@DiscordClient.command()
async def currentSprint(message: discord.Message):
    currentBoardID = await getCurrentBoardID(message)

    if currentBoardID == None:
        return

    currentSprint = JiraClient.get_current_sprint(currentBoardID)

    sprintInfoEmbed = discord.Embed(
        title=f"{currentSprint.name}",
        color=generateRandomDiscordColor(),
    )

    sprintInfoEmbed.add_field(name="ID da sprint", value=currentSprint.id, inline=False)
    sprintInfoEmbed.add_field(
        name="Data de início da sprint",
        value=getFormattedDateFromDatetime(currentSprint.startDate),
        inline=False,
    )
    sprintInfoEmbed.add_field(
        name="Data de término da sprint",
        value=getFormattedDateFromDatetime(currentSprint.endDate),
        inline=False,
    )

    await message.reply(
        content=f"**É claro, aqui está sua sprint atual:**\n \n",
        embed=sprintInfoEmbed,
    )

@DiscordClient.command()
async def report(message: discord.Message):
    currentBoardID = await getCurrentBoardID(message)

    if currentBoardID == None:
        return

    sprint = JiraClient.get_current_sprint(currentBoardID)

    sprint_tasks = JiraClient.get_tasks_in_sprint(sprint.id)

    tasks_per_category = {}

    for task in sprint_tasks:
        current_task_category = task.status
        if current_task_category not in tasks_per_category:
            tasks_per_category[current_task_category] = []
        tasks_per_category[current_task_category].append(task)
                
    doneCategoryName = "Concluído" if "Concluído" in tasks_per_category else "Done"
    tasksList = tasks_per_category[doneCategoryName] if doneCategoryName in tasks_per_category else []
    
    conclusionPercentage = round(
        len(tasksList) / len(sprint_tasks) * 100,
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
        name="Iniciada há", value=f"{abs(sprint.getDaysPassed())} dias", inline=True
    )

    sprintEmbed.add_field(name="", value="", inline=False)

    sprintEmbed.add_field(name="Tasks por categoria", value="", inline=False)
    for category in tasks_per_category:
        sprintEmbed.insert_field_at(
            5, name=category, value=len(tasks_per_category[category]), inline=True
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

DiscordClient.run(DISCORD_API_TOKEN)
server.stop()
