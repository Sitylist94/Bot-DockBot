import discord
from discord.ext import commands, tasks
import random
import asyncio
import FFmpegOpusAudio

bot = commands.Bot(command_prefix="!", description="Bot en devellepement by Sitylist94", intents=discord.Intents.all())

@bot.event
async def on_ready():
	print("Le bot est prêt !")
	changeStatus.start()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")

@bot.command()
async def ping(ctx):
    await ctx.send(f'mon ping est de {bot.latency}')

@bot.command()
async def logo(ctx):
    await ctx.send(https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg)

@bot.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))

@bot.command()
async def chinesse(ctx, *text):
    chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
    chineseText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = chineseChar[index]
                chineseText.append(transformed)
            else:
                chineseText.append(char)
        chineseText.append(" ")
    await ctx.send("".join(chineseText))

@bot.command()
async def Serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient **{numberOfPerson}** personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
    await ctx.send(message)

@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)

@bot.command()
    async def clear(ctx, amount=5):
				await ctx.channel.purge(limit=amount)
                
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !")
    embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = random.choice(funFact))

    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(eject_members=True)
async def eject(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason = reason)
    embed=discord.Embed(title="**expulsion**", description="Un modérateur a frappé !")
    embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/miscellaneous-245-color-shadow/128/exclusion_cancel_negation_boycott_rejection_embargo_disallowance_inhibition-256.png")
    embed.add_field(name = "Membre expulsé", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = random.choice(funFact))

    await ctx.send(embed = embed)


bot.run("TOKEN")
