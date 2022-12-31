import discord
from discord.ext import commands, tasks
import asyncio
import random
bot = commands.Bot(command_prefix="!", description="Bot de Sitylist94", intents=discord.Intents.all())
status = ["!help",
        "A votre service",
        "L'eau mouille",
        "Le feu brule",
        "Lorsque vous volez, vous ne touchez pas le sol",
        "Winter is coming",
        "Mon créateur est Sitylist94",
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
    print("Le bot est prêt ! ")
    changeStatus.start()

@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")


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
async def clear(ctx, nombre : int):
  await ctx.channel.purge(limit = nombre + 1)

@bot.command()
async def start(ctx, secondes=5):
    changeStatus.change_interval(seconds=secondes)


@tasks.loop(seconds=5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)



@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", url = "https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber", color=0xfa8072)
    embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = random.choice(funFact))

    await ctx.send(embed = embed)


@bot.command()
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    userName = userName.replace("_", " ")
    # bannedUsers = await ctx.guild.bans()
    # for i in bannedUsers:
    #     if i.user.name == userName and i.user.discriminator == userId:
    #         await ctx.guild.unban(i.user, reason = reason)
    #         await ctx.send(f"{user} à été unban.")
    #         return
    await ctx.guild.unban(user, reason = reason)
    await ctx.send(f"{user} à été unban.")


    def isOwner(ctx):
        return ctx.message.author.id == 946704652798402581

    @bot.command()
    @commands.check(isOwner)
    async def private(ctx):
        await ctx.send("Cette commande peut seulement etre effectuées par le propriétaire du bot !")

    @bot.event
    async def on_reaction_add(reaction, user):
        await reaction.message.add_reaction(reaction.emoji)

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
        await ctx.guild.kick(user, reason=reason)
        embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !",
                              url="https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber",
                              color=0xfa8072)
        embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/BanneHammer.png")
        embed.add_field(name="Membre kick", value=user.name, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
        embed.set_footer(text=random.choice(funFact))

    @bot.command()
    async def clear(ctx, nombre: int):
        messages = await ctx.channel.histo & ry(limit=nombre + 1).flatten()
        for message in messages:
            await message.delete()


@bot.command()
async def quoi(ctx):
    await ctx.send("FEUR !")


@bot.command()
async def cuisiner(ctx):
    await ctx.send("Envoyez le plat que vous voulez cuisiner")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    try:
        recette = await bot.wait_for("message", timeout=10, check=checkMessage)
    except:
        await ctx.send("Veuillez réitérer la commande.")
        return
    message = await ctx.send(
        f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (
                str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=10, check=checkEmoji)
        if reaction.emoji == "✅":
            await ctx.send("La recette a démarré.")
        else:
            await ctx.send("La recette a bien été annulé.")
    except:
        await ctx.send("La recette a bien été annulé.")


"""
!cuisiner -> sitylist
frites : coucou
sitylist : pates
"""

"""
✅❌
"""


@bot.command()
async def roulette(ctx):
    await ctx.send("La roulette commencera dans 10 secondes. Envoyez \"moi\" dans ce channel pour y participer.")

    players = []

    def check(message):
        return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"

    try:
        while True:
            participation = await bot.wait_for('message', timeout=10, check=check)
            players.append(participation.author)
            print("Nouveau participant : ")
            print(participation)
            await ctx.send(f"**{participation.author.name}** participe au tirage ! Le tirage commence dans 10 secondes")
    except:  # Timeout
        print("Demarrage du tirrage")

    gagner = ["ban", "kick", "role personnel", "mute", "gage"]

    await ctx.send("Le tirage va commencer dans 3...")
    await asyncio.sleep(1)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    loser = random.choice(players)
    price = random.choice(gagner)
    await ctx.send(f"La personne qui a gagnée un {price} est...")
    await asyncio.sleep(1)
    await ctx.send("**" + loser.name + "**" + " !")

def isOwner(ctx):
    return ctx.message.author.id == ID


@bot.event
async def on_message(message):
    if message.content.lower() == "quoi":
        await message.channel.send("feur")

@bot.command()
async def number(ctx, num: int):
    x = random.randint(0, num)
    await ctx.send(f"Votre nombre est {x}")

@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette commande peut seulement etre effectuées par le propriétaire du bot !")

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

"""
funFact = ["L'eau mouille", 
            "Le feu brule", 
            "Lorsque vous volez, vous ne touchez pas le sol", 
            "Winter is coming", "Mon créateur est Titouan", 
            "Il n'est pas possible d'aller dans l'espace en restant sur terre", 
            "La terre est ronde",
            "La moitié de 2 est 1",
            "7 est un nombre heureux",
            "Les allemands viennent d'allemagne",
            "Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
            "J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
            "Le plus grand complot de l'humanité est",
            "Pourquoi lisez vous ca ?"]
"""

bot.run("TOKEN")
