import discord
from discord import Embed
from discord.ext import commands, tasks
import random
import time
import youtube_dl
import asyncio

bot = commands.Bot(command_prefix="!", description="Bot de Sitylist94", intents=discord.Intents.all())
musics = {}
ytdl = youtube_dl.YoutubeDL()

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


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)




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
async def mute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !")


@bot.command()
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")

@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)



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
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()


def isOwner(ctx):
    return ctx.message.author.id == TON_IDENTIFIANT


@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette commande peut seulement etre effectuées par le propriétaire du bot !")


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     await message.channel.send(f"> {message.content}\n{message.author}")
#     await bot.process_commands(message)
#
#
# @bot.event
# async def on_message_delete(message):
#     await message.channel.send(f"Le message de {message.author} a été supprimé \n> {message.content}")
#
#
# @bot.event
# async def on_message_edit(before, after):
#     await before.channel.send(
#         f"{before.author} a édité son message :\nAvant -> {before.content}\nAprès -> {after.content}")


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


# @bot.event
# async def on_typing(channel, user, when):
#     await channel.send(f"{user.name} a commencé à écrire dans ce channel le {when}.")


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


# @bot.command()
# async def ban(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
#     #await ctx.guild.ban(user, reason = reason)
#     embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", url = "https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber", color=0xfa8072)
#     embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber")
#     embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
#     embed.add_field(name = "Membre banni", value = user.name, inline = True)
#     embed.add_field(name = "Raison", value = reason, inline = True)
#     embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
#     embed.set_footer(text = random.choice(funFact))
#
#     await ctx.send(embed = embed)
#

































"""
https://www.youtube.com/channel/UChDVo_Uqomuk7KnMVp-Lhhw?view_as=subscriber
"""


"""
https://discordemoji.com/assets/emoji/BanneHammer.png
"""


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
bot.run("TON_TOKEN")
