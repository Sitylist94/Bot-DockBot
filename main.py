import json
import discord
from discord.ext import commands, tasks
import random
import asyncio
from asyncio import sleep
import discord
from discord.ext import commands
from discord import app_commands
import os
import requests
import datetime
from discord.ui import Select
from discord import Embed, app_commands
from discord.ext import commands
import string
from discord.ext.commands import CommandNotFound
from discord.ui import Button, View
from typing import ValuesView
from typing import Union
from datetime import datetime, timedelta
import urllib.parse
import subprocess


bot = commands.Bot(command_prefix="!", description="Bot en devellepement by Sitylist94", intents=discord.Intents.all())
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
          " Dockbot V0.0.1 pre-release 4",
          "Pourquoi lisez vous ca ?"]

@discord.ui.button(label="Ajouter 1", style=discord.ButtonStyle.green, custom_id="add_button")
async def add_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        gout = button.custom_id
        await self.add_puff(gout, interaction)



@discord.ui.button(label="Retirer 1", style=discord.ButtonStyle.red, custom_id="remove_button")
async def remove_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        gout = button.custom_id
        await self.remove_puff(gout, interaction)


@bot.tree.command(name="userinfo", description="Afiche les informations d'un membre")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    roles = [role.name for role in member.roles]
    embed = discord.Embed(title=f"Informations sur {member.display_name}", description="", color=member.color)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Pseudo", value=member.display_name, inline=True)
    embed.add_field(name="Création du compte", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
    embed.add_field(name="A rejoint le serveur", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Rôles", value=", ".join(roles), inline=True)
    embed.set_thumbnail(url=member.avatar)
    await interaction.response.send_message(embed=embed)








@bot.command(name="create_server", description="Permet de crée un serveur discord ")
@commands.has_permissions(administrator=True)
async def serv(ctx):
    guild = ctx.guild
    staff = await guild.create_category("Staff")
    infos = await guild.create_category("informations")
    general = await guild.create_category("général")
    audios = await guild.create_category("les audios")
    events = await guild.create_category("events")
    afk = await guild.create_category("afk")

    await guild.create_text_channel("├﹝💬﹞général", category=general)

    await guild.create_text_channel("├﹝📢﹞event", category=events)
    await guild.create_voice_channel("├﹝🎤﹞event", category=events)

    await guild.create_text_channel("├﹝📢﹞annonces", category=infos)
    await guild.create_text_channel("├﹝📖﹞règles", category=infos)
    await guild.create_text_channel("├﹝🌀﹞support", category=infos)
    await guild.create_text_channel("├﹝♻﹞recrutement", category=infos)
    await guild.create_text_channel("├﹝✨﹞vos pseudos", category=infos)
    await guild.create_text_channel("├ (🌁) média", category=general)

    await guild.create_voice_channel("├﹝🎤﹞staff", category=staff)

    await guild.create_voice_channel("├﹝🎤﹞afk", category=afk)

    await guild.create_voice_channel("├﹝🎤﹞discussion", category=audios)
    await ctx.send("Le serveur discord est prêt ✅")

@bot.event
async def on_ready():
    print("Le bot est prêt !")
    changeStatus.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)








@bot.command()
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

# bot.remove_command("help")




@bot.tree.command(name="movies", description="Obtenir des films dans une catégories données")
async def movies(interaction: discord.Interaction, genre: str):
    movie_list = {
        "action": ["The Dark Knight", "The Matrix", "John Wick", "Die Hard", "Mad Max"],
        "comedy": ["The Hangover", "Airplane!", "Zombieland", "Shaun of the Dead", "Talladega Nights"],
        "drama": ["The Shawshank Redemption", "The Godfather", "The Godfather: Part II", "The Silence of the Lambs", "Pulp Fiction"],
        "horror": ["The Shining", "Psycho", "The Exorcist", "Get Out", "Halloween"],
        "sci-fi": ["Star Wars", "The Terminator", "Inception", "The Matrix", "Blade Runner"],
    }
    if genre.lower() in movie_list:
        movies = movie_list[genre.lower()]
        response = f"Some {genre} movies: \n" + "\n".join(movies)
        await interaction.response.send_message(response)
    else:
        response = f"Sorry, I don't have information on {genre} movies."
        await interaction.response.send_message(response)

@bot.tree.command(name="sunpheus", description="Affiche des citations sortie de la sage bouche de Sunpheus_")
async def self(interaction: discord.Interaction):
    joke = [ "j'ai une idée, j'aime le pain", "un jour mon grand-père m'a dit qu'il regardait ses mails","je suis le seigneur tout-puissant de la galaxie",
             "je suis iron 3 sur valo (Oe je suis féroce)","poisson de novembre","Fortnite et FIFA c'est éclaté beuh","en vrai","je sais faire des pâtes",
             "Casio ce n'est pas que des calculatrices, ils font aussi des pianos","le bit coin c'est cheap en vrai","il pleut plus dans la région de biarritz qu'en Bretagne",
             "saucisse bien fraiche","le carton","j'aime les faire des photos","salut","mon beau pancréas","la terre c'est marron et comestible"






             ]
    response = random.choice(joke)
    await interaction.response.send_message(response)

@bot.tree.command(name="joke", description="Affiche une citation aléatoire")
async def joke(interaction: discord.Interaction):
    jokes = [ "Pourquoi les poules ont-elles des plumes ? Parce qu'elles n'ont pas de sous-vêtements !",
        "Comment appelle-t-on un canard qui n'a pas de place pour se poser ? Un dindon !",
        "Pourquoi les poissons ne jouent-ils pas aux échecs ? Parce qu'ils préfèrent la dam-nation !",
        "Pourquoi les vaches ne vont pas à la plage ? Parce qu'elles ne savent pas nager !",
        "Pourquoi les lions ne vont pas à l'école ? Parce qu'ils sont déjà des rois !",]
    response = random.choice(jokes)
    await interaction.response.send_message(response)






@bot.tree.command(name="hello", description="Se dire bonjour <3")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey{interaction.user.mention}! Passe une bonne journé!",
    ephemeral=True)


@bot.tree.command(name="cmd_help", description="Affiche la liste des commandes")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="🏠 Accueil", color=0xdf4e4e)
    embed.set_thumbnail(url="https://discord.com/channels/@me/996452655796858970/1091399906008248371")
    embed.add_field(name="Meme ", value="Afficher un meme", inline=False)
    embed.add_field(name="8ball", value="Propose une réponse", inline=True)
    embed.add_field(name="addrole", value="Ajoute le rôle demander ", inline=False)
    embed.add_field(name="ban", value="Bannir un membre", inline=False)
    embed.add_field(name="roll", value="Dit un résultat des dés aléatoire", inline=True)
    embed.add_field(name="addrole", value="Ajouter un rôle", inline=False)
    embed.add_field(name="changeprefix", value="Changer le préfix du bot", inline=True)
    embed.add_field(name="ticket", value="Crée une catégorie ticket", inline=False)
    embed.add_field(name="reminder", value="Crée des rapels", inline=True)
    embed.add_field(name="roll", value="Avoir un lancer de dés aléatoire", inline=False)
    embed.add_field(name=" meme", value="Envoie un meme aléatoire", inline=True)
    embed.add_field(name="kick", value="Eject la personne", inline=False)
    embed.add_field(name="close_ticket", value="Fermer le ticket", inline=False)
    embed.add_field(name="create_ticket", value="Crée un ticket", inline=False)
    embed.add_field(name="createMutedRole", value="Crée un rôle muet ( si cela na pas déjà été fait )", inline=False)
    embed.add_field(name="number", value="Donne un nombre aléatoire dans une rangé donnée", inline=False)
    embed.set_footer(text="By Sitylist94")
    await interaction.response.send_message(embed=embed)



@bot.command()
async def google(ctx, *, query):
    query = urllib.parse.quote_plus(query)
    await ctx.send(f'https://www.google.com/search?q={query}')



@bot.tree.command(name="calculate", description="Calculer une expression mathématique")
async def calculate(interaction: discord.Interaction,*,expression: str):
    try:
        result = eval(expression)
        await interaction.response.send_message(f"Le résultat est: {result}")
    except:
        await interaction.response.send_message("Expression mathématique incorrecte.")







@bot.tree.command(name="unmute", description="Dé-reduire au silence un membre")
@commands.has_permissions(manage_roles=True)
@app_commands.describe(member="Qui voulez vous mute ?")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    mutedRole = await getMutedRole(interaction)
    embed = discord.Embed(title="Unmute", description=f"{member.mention} a été unmute ", color=0xff0000)
    embed.set_author(name="Dockbot",
                     icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(url="https://tse4.mm.bing.net/th?id=OIP.0TyGYnCl_Rl0QtuJ25oIHAHaHk&pid=Api&P=0")
    embed.set_footer(text="made by Sitylist94")
    await member.remove_roles(mutedRole)
    await interaction.response.send_message(embed=embed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def create_ticket(ctx):
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }

    category = discord.utils.get(ctx.guild.categories, name='Tickets')
    if not category:
        category = await ctx.guild.create_category(name='Tickets')

    channel = await category.create_text_channel(name=f'ticket-{ctx.author.display_name}', overwrites=overwrites)
    await ctx.send(f'Votre ticket a été créé : {channel.mention}')

# supprimer un ticket
@bot.command()
@commands.has_permissions(manage_roles=True)
async def close_ticket(ctx):
    if ctx.channel.category.name == 'Tickets':
        await ctx.channel.delete()
        await ctx.send('Votre ticket a été supprimé')


@bot.command(name="clear", description="Supprime un certain nombre de messages dans le canal")
async def clear_messages(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre+1)
    message = await ctx.send(f"{nombre} messages ont été supprimés !")
    await message.delete()


warns = {}

@bot.tree.command(name="warn", description="Avertir un membre ")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    """Donne un warn à un utilisateur."""
    if member.bot:
        await interaction.response.send_message("Vous ne pouvez pas donner un warn à un bot.")
        return
    if member.id not in warns:
        warns[member.id] = 1
    else:
        warns[member.id] += 1
    await interaction.response.send_message(f"{member.mention} a été averti{' pour ' + reason if reason else ''}. Total de warns : {warns[member.id]}")








@bot.tree.command(name="unwarn", description="Enleve l'avertissement d'un membre")
async def unwarn(interaction: discord.Interaction, member: discord.Member, reason: str):
    """Retire un warn à un utilisateur."""
    if member.bot:
        await interaction.response.send_message("Vous ne pouvez pas retirer un warn à un bot.")
        return
    if member.id not in warns or warns[member.id] == 0:
        await interaction.response.send_message(f"{member.mention} n'a pas de warn.")
        return
    warns[member.id] -= 1
    await interaction.response.send_message(f"{member.mention} a eu un warn retiré{' pour ' + reason if reason else ''}. Total de warns : {warns[member.id]}")

@bot.tree.command(name="warncounter", description="Afficher la liste des warns d'un membre")
async def warncounter(interaction: discord.Interaction, member: discord.Member):
    """Affiche le nombre de warns d'un utilisateur."""
    if member is None:
        member = interaction.author
    if member.id not in warns or warns[member.id] == 0:
        await interaction.response.send_message(f"{member.mention} n'a pas de warn.")
        return
    await interaction.response.send_message(f"{member.mention} a {warns[member.id]} warn{'s' if warns[member.id] > 1 else ''}.")

@bot.tree.command(name="addrole", description="Ajouter un rôle du serveur à un membre")
@commands.has_permissions(administrator=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):

    if role:
        await member.add_roles(role)
        await interaction.response.send_message(f"Le rôle {role.mention} a été ajouté à {member.mention} !") # Envoyer un message de confirmation.
    else:
        await interaction.response.send_message(f"Le rôle {role.mention} n'existe pas dans ce serveur.") # Envoyer un message d'erreur si le rôle n'existe pas.

@bot.tree.command(name="removerole", description="Retirer un rôle du serveur à un membre")
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    """Retire un rôle à un utilisateur."""
    if role not in member.roles:
        await interaction.response.send_message(f"{member.mention} n'a pas le rôle {role.mention}.")
    else:
        await member.remove_roles(role)
        await interaction.response.send_message(f"{role.mention} retiré de {member.mention}.")


@bot.tree.command(name="avatar", description="Afficher l'avatar d'un membre ")
async def avatar(interaction: discord.Interaction, user: discord.Member):
    """Affiche l'avatar de l'utilisateur mentionné ou de l'utilisateur qui a exécuté la commande."""
    if user is None:
        user = interaction.author
    embed = discord.Embed(title=f"Avatar de {user}", color=discord.Color.blurple())
    embed.set_image(url=user.avatar)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="rps", description="Jouer à pierre, papier, ciceaux avec le bot ")
async def rps(interaction: discord.Interaction, choix: str):
    """Joue à Pierre, Papier, Ciseaux avec le bot."""
    choix = choix.lower()
    if choix not in ["pierre", "papier", "ciseaux"]:
        await interaction.response.send_message("Désolé, cette option n'existe pas. Veuillez choisir entre pierre, papier ou ciseaux.")
        return
    choix_bot = random.choice(["pierre", "papier", "ciseaux"])
    resultats = {"pierre": {"pierre": "Égalité", "papier": "Vous avez perdu !", "ciseaux": "Vous avez gagné !"},
                 "papier": {"pierre": "Vous avez gagné !", "papier": "Égalité", "ciseaux": "Vous avez perdu !"},
                 "ciseaux": {"pierre": "Vous avez perdu !", "papier": "Vous avez gagné !", "ciseaux": "Égalité"}}
    resultat = resultats[choix][choix_bot]
    embed = discord.Embed(title="Pierre, Papier, Ciseaux", color=discord.Color.blurple())
    embed.add_field(name="Vous avez choisi", value=choix.capitalize(), inline=True)
    embed.add_field(name="Le bot a choisi", value=choix_bot.capitalize(), inline=True)
    embed.add_field(name="Résultat", value=resultat, inline=False)
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="logo", description="Afficher le logo du bot")
async def logo(interaction:discord.Interaction):
    await interaction.response.send_message("https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")


@bot.tree.command(name="say", description="Renvoie votre message")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f" {thing_to_say}")







@bot.tree.command(name="coinflip", description="Affiche Pile ou face aléatoirement")
async def coinflip(interaction: discord.Interaction):
    """Joue à pile ou face."""
    result = random.choice(["pile", "face"])
    await interaction.response.send_message(f"Vous avez obtenue {result} !", ephemeral=True)

@bot.tree.command(name="ping", description="Affiche la latence du bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'mon ping est de {bot.latency}')


def isOwner(ctx):
    return ctx.message.author.id == 946704652798402581


@bot.tree.command(name="private", description="Command utilisable que par le propriétaire du bot")
@commands.check(isOwner)
async def private(interaction: discord.Interaction):
    await interaction.response.send_message("Cette commande peut seulement etre effectuées par le propriétaire du bot !", ephemeral=True)




@bot.tree.command(name="dm", description="Envoyez un message privé à un membre")
@commands.has_permissions(administrator=True)
@app_commands.describe(member="A qui voulez vous envoyez le message privé ?")
@app_commands.describe(message="Entrez le message que vous voulez envoyez !")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    """Envoie un message privé à un utilisateur."""
    try:
        await member.send(message)
        await interaction.response.send_message(f"Message envoyé à {member.mention}.")
    except discord.HTTPException:
        await interaction.response.send_message(f"Impossible d'envoyer un message à {member.mention}.")

@bot.tree.command(name="serverinfo", description="Affiche les informations du serveur")
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    serverDescription = server.description
    embed = discord.Embed(title="Informations sur le serveur", color=0xcd2323)
    embed.set_author(name="DockBot",
    icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(
              url="https://cdn.discordapp.com/attachments/996452655796858970/1074410407294402690/server-1064007844-PhotoRoom.png-PhotoRoom.png")
    embed.add_field(name="Nom", value=server.name)
    embed.add_field(name="ID", value=server.id)
    embed.add_field(name="Membres", value=server.member_count)
    embed.add_field(name="Propriétaire", value=server.owner.mention)
    embed.add_field(name="Rôles", value=len(server.roles))
    embed.add_field(name="Description", value=serverDescription)
    embed.add_field(name="Salons textuels", value=len(server.text_channels))
    embed.add_field(name="Salons vocaux", value=len(server.voice_channels))
    embed.set_footer(text="By Sitylist94")

    await interaction.response.send_message(embed=embed)


@bot.command()
async def start(ctx, secondes=5):
    changeStatus.change_interval(seconds=secondes)
    await ctx.send("Bot Prêt ✅")

@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name='Membre non vérifié'))
    channel = discord.utils.get(member.guild.channels, name='captcha')
    await channel.send(f"Veuillez taper 'captcha' pour être vérifié {member.mention}")




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas :/")

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oups vous ne pouvez utilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")


@bot.event
async def on_member_join(member):
    # Récupérer le canal de discussion général du serveur
    channel = member.guild.system_channel

    if channel is not None:
        # Envoyer un message de bienvenue avec la photo de profil de l'utilisateur
        embed = discord.Embed(title=f"Bienvenue {member.name} !", description="Bienvenue sur notre serveur !", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar.url)  # Utiliser member.avatar.url pour obtenir l'URL de l'avatar
        await channel.send(embed=embed)




@tasks.loop(seconds=5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.tree.command(name="ban", description="Bannit un membre du serveur")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(title="Ban", description="Bannir un membre", color=0x457cd3)
        embed.set_author(name="Sitylist94",
                         icon_url="https://tse1.mm.bing.net/th?id=OIP.DFf4J7NKkBEMgnyoDCQr7AHaHa&pid=Api&P=0")
        embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/BanneHammer.png")
        embed.add_field(name="Membre banni", value=f"{member}", inline=True)
        embed.add_field(name="Raison", value=f"{reason}", inline=True)
        embed.set_footer(text="By Sitylist94")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Ban", description="Bannir un membre", color=0x457cd3)
        embed.set_author(name="Sitylist94",
                         icon_url="https://tse1.mm.bing.net/th?id=OIP.DFf4J7NKkBEMgnyoDCQr7AHaHa&pid=Api&P=0")
        embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/BanneHammer.png")
        embed.add_field(name="Désoler vous n'avez pas les permissions requises pour bannir cette personne !",
                        value="", inline=True)
        embed.set_footer(text="By Sitylist94")
        await interaction.response.send_message(embed=embed)

# dictionnaire de membres avec leur XP actuel
xp = {}

# dictionnaire de membres avec leur niveau actuel
levels = {}

# récompenses pour atteindre chaque niveau
rewards = {
    5: 'Grade 1',
    10: 'Grade 2',
    20: 'Grade 3',
    30: 'Grade 4',
    40: 'Grade 5',
    50: 'Grade 6'
}



@bot.tree.command(name="mute", description="Réduire au silence un membre")
@commands.has_permissions(administrator=True)
async def mute(interaction: discord.Interaction, member: discord.Member, time: int):
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    embed = discord.Embed(title="Mute", description=f"{member.mention} a été mute pour {time} minutes ", color=0xff0000)
    embed.set_author(name="Dockbot",
                     icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(url="https://tse4.mm.bing.net/th?id=OIP.0TyGYnCl_Rl0QtuJ25oIHAHaHk&pid=Api&P=0")
    embed.set_footer(text="made by Sitylist94")
    await interaction.response.send_message(embed=embed)
    await member.add_roles(mute_role)

    await asyncio.sleep(time * 60)

@bot.tree.command(name="meme", description="Afficher un meme aléatoire")
async def meme(interaction: discord.Interaction):
    try:
        response = requests.get("https://api.imgflip.com/get_memes").json()
        memes = response["data"]["memes"]
        random_meme = random.choice(memes)
        url = random_meme["url"]
        await interaction.response.send_message(url)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")


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


@bot.tree.command(name="kick", description="Exclure un membre")
@commands.has_permissions(ban_members = True)
@app_commands.describe(user="Qui voulez vous ejecter")
@app_commands.describe(reason="Pour quel raison voulez vous bannir se membre")
async def kick(interaction: discord.Interaction, user: discord.User, reason: str):
    await interaction.guild.kick(user, reason=reason)
    embed = discord.Embed(title="**Expulsion**", description="Un modérateur a frappé !")
    embed.set_thumbnail(
        url="https://sbedirect.com/4672-home_default/danger-sign-pictogram-for-electric-hazard-blast.jpg")
    embed.add_field(name="Membre expulsé", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.set_thumbnail(url=user.avatar)
    embed.set_footer(text=random.choice(funFact))

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="number", description="Affiche un nombre aléatoire dans une ranger données")
async def number(interaction: discord.Interaction, num: int):
    x = random.randint(0, num)
    embed = discord.Embed(title="Nombre aléatoire", description="Trouve un nombre aléatoire ", color=0xd91212)
    embed.set_author(name="Dockbot")
    embed.set_thumbnail(url="https://tse4.mm.bing.net/th?id=OIP.pFzi6bMyJLmmMQ9ydb9thwHaE8&pid=Api&P=0")
    embed.add_field(name="Le nombre est : " + str(x), value="", inline=True)
    embed.set_footer(text="By Sitylist94")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="prison", description="Met un membre en prison et restreint ses autorisations")
async def prison(interaction: discord.Interaction, member: discord.Member):

    role = discord.utils.get(interaction.guild.roles, name="Prisonnier")
    prison_channel = discord.utils.get(interaction.guild.channels, name="prison")

    # Vérifie si le rôle "Prisonnier" existe, sinon le crée
    if not role:
        role = await interaction.guild.create_role(name="Prisonnier")

    # Vérifie si le salon "prison" existe, sinon le crée
    if not prison_channel:
        prison_channel = await interaction.guild.create_text_channel(name="prison")

    # Ajoute le rôle "Prisonnier" au membre
    await member.add_roles(role)

    # Restreint les autorisations du membre dans tous les salons (sauf celui de prison)
    for channel in interaction.guild.channels:
        await channel.set_permissions(member, send_messages=False)

        await prison_channel.set_permissions(member, send_messages=True)
        await interaction.response.send_message(f"{member.mention} a été mis en prison")



@bot.tree.command(name="liberation", description="Libère un membre de prison")
async def liberation(interaction: discord.Interaction, member: discord.Member):

    role = discord.utils.get(interaction.guild.roles, name="Prisonnier")

    # Vérifie si le membre est en prison
    if role in member.roles:

        # Retire le rôle "Prisonnier" du membre
        await member.remove_roles(role)
        for channel in interaction.guild.channels:
            await channel.set_permissions(member, send_messages=None)
            await interaction.response.send_message(f"{member.mention} a été libéré de prison.")
        else:
            await interaction.response.send_message(f"{member.mention} n'est pas en prison.")




@bot.tree.command(name="rappel", description="Créer un rappel")
async def rappel(interaction: discord.Interaction, temps: str, *, message: str):
    member = discord.Member
    if not temps.isdigit():
        await interaction.response.send_message("Veuillez fournir une durée valide en secondes, minutes ou heures. Par exemple: `!rappel 10s Prendre une pause`")
        return

    temps = int(temps)
    if temps <= 0:
        await interaction.response.send_message("Veuillez fournir une durée positive.")
        return

    if message.strip() == "":
        await interaction.response.send_message("Veuillez fournir un message pour le rappel.")
        return


    await interaction.response.send_message(f"Rappel réglé pour '{message}' dans {temps} secondes.")

    await asyncio.sleep(temps)

    await interaction.response.send_message(f"{member.mention}, voici votre rappel pour '{message}'.")

quotes = [
    "Avec de la persévérance, tout est possible.",
    "L'échec est la première étape vers le succès.",
    "N'ayez pas peur de prendre des risques. Les plus grands réalisateurs ont échoué avant de réussir.",
    "Si vous pouvez rêver, vous pouvez le faire.",
    "Le succès n'est pas définitif, l'échec n'est pas fatal : c'est le courage de continuer qui compte.",
    "Croire en soi, c'est déjà être à mi-chemin du succès."
]

@bot.tree.command(name='roll', description="Affiche un résultat des dés aléatoire")
async def roll(interaction: discord.Interaction):
    dice = random.randint(1,6)
    await interaction.response.send_message(f'Le résultat du lancement de dés est : {dice}')


@bot.tree.command(name="infos", description="Informations du bot")
async def infos(interaction: discord.Interaction):

    logo_url = "https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg"

    # Récupérer la liste des développeurs
    devs = ["Sitylist94", "Sunpheus_"]

    # Lien pour aider le bot
    help_url = "https://dockbot.epizy.com"

    # Lien du code source du bot
    source_url = "https://github.com/Sitylist94/Bot-DockBot"

    # Date et heure du prochain rendez-vous
    rendez_vous = ""

    # Nombre de serveurs sur lesquels le bot a été ajouté
    nb_serveurs = len(bot.guilds)

    # Informations sur les commandes disponibles
    command_list = "\n".join([f"{command.name} : {command.help}" for command in bot.commands])

    # Créer un embed pour afficher les informations
    embed = discord.Embed(title="Informations sur le bot", color=discord.Color.blue())
    embed.set_thumbnail(url=logo_url)
    embed.add_field(name="Développeurs", value=", ".join(devs), inline=False)
    embed.add_field(name="Comment aider ?", value=help_url, inline=False)
    embed.add_field(name="Code source", value=source_url, inline=False)
    embed.add_field(name="Prochain rendez-vous", value=rendez_vous, inline=False)
    embed.add_field(name="Nombre de serveurs", value=nb_serveurs, inline=False)
    embed.add_field(name="Commandes disponibles", value=command_list, inline=False)

    await interaction.response.send_message(embed=embed)





@bot.command()
async def create_embed(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Quel type d'embed voulez-vous créer? ('giveaway', 'annonce', 'bot')")

    embed_type = await bot.wait_for('message', check=check)
    embed_type = embed_type.content.lower()

    if embed_type == 'giveaway':
        await ctx.send("Quel est la récompense pour le giveaway?")
        reward = await bot.wait_for('message', check=check)
        await ctx.send("Combien de temps voulez-vous que le giveaway soit actif?")
        time = await bot.wait_for('message', check=check)
        await ctx.send("Combien de gagnants voulez-vous choisir?")
        winners = await bot.wait_for('message', check=check)

        giveaway_embed = discord.Embed(title="Giveaway", description=f"Récompense : {reward.content}\nGagnants : {winners.content}\nDurée : {time.content}", color=0x00ff00)
        await ctx.send(embed=giveaway_embed)

    elif embed_type == 'annonce':
        await ctx.send("Quel est le message de l'annonce?")
        annonce = await bot.wait_for('message', check=check)

        annonce_embed = discord.Embed(title="Annonce", description=annonce.content, color=0x00ff00)
        await ctx.send(embed=annonce_embed)


bot.run(TOKEN)
# Dockbot V0.0.1 pre-release 4
