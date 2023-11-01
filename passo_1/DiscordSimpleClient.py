import discord
from discord.ext import commands
from settings import DISCORD_API_TOKEN, commandPrefix


DiscordClient = commands.Bot(intents=discord.Intents.all(), command_prefix=commandPrefix)

@DiscordClient.event
async def on_ready():
    print(f'Logado com sucesso como {DiscordClient.user}')


@DiscordClient.event
async def on_message(message):
    if message.author == DiscordClient.user:
        return
    
    await DiscordClient.process_commands(message)

@DiscordClient.command()
async def oi(context): # Sem receber nenhum parâmetro
    await context.reply(f'Olá {context.author.mention}! 👋')

@DiscordClient.command()
async def salve(context, *possiveisNomes): # Tratando qualquer parâmetro que for passado
    if len(possiveisNomes) == 0:
        await context.reply('Ei, como vou mandar um salve se não sei para quem? 👀')
    elif len(possiveisNomes) == 1:
        await context.channel.send(f'Um salve para {possiveisNomes[0]}!')
    else:
        nomes = list(possiveisNomes)
        ultimoNome = nomes.pop()        
        await context.channel.send(f'Um salve para {", ".join(nomes)} e para {ultimoNome}!')

DiscordClient.run(DISCORD_API_TOKEN)