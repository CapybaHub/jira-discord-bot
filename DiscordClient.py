import discord
from discord.ext import commands
from utils import generateRandomDiscordColor
from settings import commandPrefix

from simple_http_server import server
    
DiscordClient = commands.Bot(
    intents=discord.Intents.all(), command_prefix=commandPrefix
)


@DiscordClient.event
async def on_ready():
    print(f"Logado com sucesso como {DiscordClient.user}")
    await server.start_async(prefer_coroutine=True)


@DiscordClient.event
async def on_message(message):
    if message.author == DiscordClient.user:
        return

    await DiscordClient.process_commands(message)


@DiscordClient.command()
async def oi(context):  # Sem receber nenhum parâmetro
    await context.reply(f"Olá {context.author.mention}! 👋")


@DiscordClient.command()
async def salve(
    context, *possiveisNomes
):  # Tratando qualquer parâmetro que for passado
    if len(possiveisNomes) == 0:
        await context.reply("Ei, como vou mandar um salve se não sei para quem? 👀")
    elif len(possiveisNomes) == 1:
        await context.channel.send(f"Um salve para {possiveisNomes[0]}!")
    else:
        nomes = list(possiveisNomes)
        ultimoNome = nomes.pop()
        await context.channel.send(
            f'Um salve para {", ".join(nomes)} e para {ultimoNome}!'
        )


@DiscordClient.command()
async def commands(context):
    commandsEmbed = discord.Embed(
        title="Comandos disponíveis",
        color=generateRandomDiscordColor(),
    )
    
    allCommands = list(DiscordClient.commands)

    for command in allCommands:
        if command.name == "help":
            continue
        
        help = command.help if "help" in command.__dict__  and  command.help is not None else "Sem exemplo."
            
        commandsEmbed.add_field(name=command.name, value=help, inline=False)

    await context.send(embed=commandsEmbed)

