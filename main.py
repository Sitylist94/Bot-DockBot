import discord
from discord.ext import commands
import random
import time

bot = commands.Bot(command_prefix="!", description="Bot de Sitylist94", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Le bot est prêt !")

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
    async def ban(ctx, user: discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

    @bot.command()
    async def unban(ctx, user, *reason):
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason=reason)
                await ctx.send(f"{user} à été unban.")
                return
        # Ici on sait que lutilisateur na pas ete trouvé
        await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

    @bot.command()
    async def kick(ctx, user: discord.User, *reason):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} à été kick.")

    @bot.command()
    async def clear(ctx, nombre: int):
        messages = await ctx.channel.histo&ry(limit=nombre + 1).flatten()
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
        recette = await bot.wait_for("message", timeout = 10, check = checkMessage)
    except:
        await ctx.send("Veuillez réitérer la commande.")
        return
    message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
    await message.add_reaction("✅")
    await message.add_reaction("❌")


    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
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
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")


def isOwner(ctx):
    return ctx.message.author.id == TON_IDENTIFIANT
@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette commande peut seulement etre effectuées par le propriétaire du bot !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await message.channel.send(f"> {message.content}\n{message.author}")
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    await message.channel.send(f"Le message de {message.author} a été supprimé \n> {message.content}")

@bot.event
async def on_message_edit(before, after):
    await before.channel.send(f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(714786510238384532)
    await channel.send(f"Acceuillons a bras ouvert {member.mention} ! Bienvenue dans ce magnifique serveur :)")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(714786510238384532)
    await channel.send(f"En cette belle journée nous déplorons la perte d'un membre bien aimé, {member.mention}.")

@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.add_reaction(reaction.emoji)

@bot.event
async def on_typing(channel, user, when):
    await channel.send(f"{user.name} a commencé à écrire dans ce channel le {when}.")


bot.run("TON TOKEN")
