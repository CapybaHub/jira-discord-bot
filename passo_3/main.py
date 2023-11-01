import discord
from DiscordClient import DiscordClient
from JiraClient import JiraClient
from settings import DISCORD_API_TOKEN, load_pickle, save_pickle
from utils import getProjectUrlFromKey, generateRandomDiscordColor

user_selected_board = load_pickle({}, 'user_selected_board')


@DiscordClient.command()
async def boards(context):
    boards = JiraClient.get_all_boards()
    
    boardsData = {}

    for board in boards["values"]:
        boardsData[board["location"]["projectKey"]] = {
            "name": board["name"],
            "image": board["location"]["avatarURI"],
            "key": board["location"]["projectKey"],
            "type": board["type"],
            "id": board["id"],
            "projectName": board["location"]["displayName"],
        }

    for board in boardsData:
        boardEmbed = discord.Embed(
            title=f'({boardsData[board]["key"]}) - {boardsData[board]["name"]}',
            url=getProjectUrlFromKey(
                JiraClient.project_url, boardsData[board]["key"]
            ),
            color=generateRandomDiscordColor(),
        )
        boardEmbed.add_field(
            name="ID do quadro", value=boardsData[board]["id"], inline=False
        )
        boardEmbed.add_field(
            name="Chave do quadro", value=boardsData[board]["key"], inline=False
        )
        boardEmbed.add_field(
            name="Nome do projeto",
            value=boardsData[board]["projectName"],
            inline=False,
        )

        boardsData[board]["embed"] = boardEmbed

    allEmbeds = [boardsData[project]["embed"] for project in boardsData]
    showEmbeds = allEmbeds[:10] # Somente é possível retornar 10 embeds por vez
    
    currentBoard = user_selected_board[context.author.id] if context.author.id in user_selected_board else None
    
    currentBoardText = f"*Atualmente o quadro selecionado é o de ID:* `{currentBoard}` \n \n" if currentBoard else ""

    await context.reply(
        embeds=showEmbeds,
        content=f"**É claro, aqui estão seus quadros do Jira:** \n\n*Contagem de projetos: {len(boardsData)}* \n \n *Para selecionar um quadro, digite:* `{DiscordClient.command_prefix}selectBoard <ID do quadro>` \n \n {currentBoardText}",
    )
    
@DiscordClient.command()
async def selectBoard(context, *boardIDS):
    if len(boardIDS) != 1 or not boardIDS[0].isdigit():
        await context.reply("Ei, você precisa passar (somente) o ID do quadro que deseja selecionar!")
    
    boardID = boardIDS[0]
    
    allBoards = JiraClient.get_all_boards()
    
    boardsIDList = [board["id"] for board in allBoards["values"]]
        
    if not int(boardID) in boardsIDList:
        await context.reply(f"Ei, o ID {boardID} não corresponde a nenhum quadro do seu Jira!")
    
    user_selected_board[context.author.id] = boardID
    save_pickle(user_selected_board, 'user_selected_board')
    await context.reply(f"Quadro selecionado com sucesso!")
    
@DiscordClient.command()
async def currentBoard(context):
    currentBoard = user_selected_board[context.author.id] if context.author.id in user_selected_board else None
    
    if not currentBoard:
        await context.reply("Ei, você ainda não selecionou um quadro! Para selecionar um quadro, digite: `!selectBoard <ID do quadro>`")
    
    await context.reply(f"O quadro selecionado atualmente é o de ID: `{currentBoard}`")

DiscordClient.run(DISCORD_API_TOKEN)