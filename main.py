import discord
from discord.ext import commands, tasks
import random
import asyncio

bot = commands.Bot(command_prefix="!", description="Bot en devellepement by Sitylist94", intents=discord.Intents.all())

status = ["!help",
          "A votre service",
          "L'eau mouille",
          "Le feu brule",
          "Lorsque vous volez, vous ne touchez pas le sol",
          "Winter is coming",
          "Mon créateur est Titouan",
          "Il n'est pas possible d'aller dans l'espace en restant sur terre",
          "La terre est ronde",
          "La moitié de 2 est 1",
          "7 est un nombre heureux",
          "Les allemands viennent d'allemagne",
          "Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
          "J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
          "Le plus grand complot de l'humanité est",
          "Pourquoi lisez vous ca ?"]


@bot.event
async def on_ready():
    print("Le bot est prêt !")
    changeStatus.start()


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
                                            permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)



@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")


@bot.command()
async def ping(ctx):
    await ctx.send(f'mon ping est de {bot.latency}')


@bot.command()
async def logo(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")

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
    async def serverinfos(ctx):
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient **{numberOfPerson}** personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
        await ctx.send(message)

@bot.command()
async def start(ctx, secondes=5):
        changeStatus.change_interval(seconds=secondes)

@tasks.loop(seconds=5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)

    @bot.command()
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason=reason)
    embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !")
    embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/BanneHammer.png")
    embed.add_field(name="Membre banni", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.set_footer(text=random.choice(funFact))

    await ctx.send(embed=embed)

funFact = ["L'eau mouille",
            "Le feu brule",
            "Lorsque vous volez, vous ne touchez pas le sol",
            "Winter is coming", "Mon créateur est Sitylist94",
            "Il n'est pas possible d'aller dans l'espace en restant sur terre",
            "La terre est ronde",
            "La moitié de 2 est 1",
            "7 est un nombre heureux",
            "Les allemands viennent d'allemagne",
            "Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
            "J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
            "Le plus grand complot de l'humanité est",
            "Pourquoi lisez vous ca ?"]

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
    await ctx.guild.kick(user, reason=reason)
    embed = discord.Embed(title="**expulsion**", description="Un modérateur a frappé !")
    embed.set_thumbnail(
        url="https://sbedirect.com/4672-home_default/danger-sign-pictogram-for-electric-hazard-blast.jpg")
    embed.add_field(name="Membre expulsé", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.set_footer(text=random.choice(funFact))

    await ctx.send(embed=embed)


@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")


@bot.command()
async def number(ctx, num: int):
    x = random.randint(0, num)
    await ctx.send(f"Votre nombre est {x}")

bot.run("TOKEN")

# Dockbot V0.0.1
