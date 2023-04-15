import discord
from discord.ext import commands, tasks
import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import os
import requests





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
          " Dockbot V0.0.1 pre-release 3",
          "Pourquoi lisez vous ca ?"]





@bot.tree.command()
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

@bot.command()
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


@bot.command(name='changeprefix', help='Change the prefix of the bot')
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, new_prefix):
    bot.command_prefix = new_prefix

    bot.command_prefix = new_prefix
    await ctx.send(f'Prefix changed to: {new_prefix}')


@bot.tree.command(name="movies")
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

@bot.tree.command(name="joke")
async def joke(interaction: discord.Interaction):
    jokes = [ "Pourquoi les poules ont-elles des plumes ? Parce qu'elles n'ont pas de sous-vêtements !",
        "Comment appelle-t-on un canard qui n'a pas de place pour se poser ? Un dindon !",
        "Pourquoi les poissons ne jouent-ils pas aux échecs ? Parce qu'ils préfèrent la dam-nation !",
        "Pourquoi les vaches ne vont pas à la plage ? Parce qu'elles ne savent pas nager !",
        "Pourquoi les lions ne vont pas à l'école ? Parce qu'ils sont déjà des rois !",]
    response = random.choice(jokes)
    await interaction.response.send_message(response)






@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey{interaction.user.mention}! This is slash command!",
    ephemeral=True)


@bot.tree.command(name="cmd_help")
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







@bot.tree.command(name="calculate")
async def calculate(interaction: discord.Interaction,*,expression: str):
    try:
        result = eval(expression)
        await interaction.response.send_message(f"Le résultat est: {result}")
    except:
        await interaction.response.send_message("Expression mathématique incorrecte.")



@bot.event
async def on_member_join(ctx, member):
    channel = member.guild.get_channel(993964162151624724)
    server = ctx.guild
    Person = server.member_count
    embed = discord.Embed(title="Ho ! Un nouveau membre !",
                          description=f"🎉 Hey bienvenue a toi Nimgame403 on est maintenant a {Person}  membre !",
                          color=0x3389e6)
    embed.add_field(name="Bienvenue à ", value=f"{member.mention}", inline=True)
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text="By Sitylist94")
    await ctx.send(embed=embed)



@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(993964243382714399)
    await channel.send(f"En cette belle journée nous déplorons la perte d'un membre bien aimé,: {member.mention})")






@bot.tree.command()
@commands.has_permissions(manage_roles=True)
@app_commands.describe(member="Qui voulez vous mute ?")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    mutedRole = await getMutedRole(interaction)
    embed = discord.Embed(title="Unmute", description=f"{member} a été unmute ", color=0xff0000)
    embed.set_author(name="Dockbot",
                     icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(url="https://tse1.mm.bing.net/th?id=OIP.fGQzN2wC8XGf2y0cZe4YBQHaHa&pid=Api&P=0")
    embed.set_footer(text="made by Sitylist94")
    await member.remove_roles(mutedRole)
    await interaction.response.send_message(embed=embed)


# définir le rôle qui peut créer des tickets
ticket_role = 'Tickets'

# créer un salon de catégorie pour les tickets
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

# vérifier si l'utilisateur est autorisé à créer un ticket
async def check_ticket_permission(ctx):
    role = discord.utils.get(ctx.guild.roles, name=ticket_role)
    if role in ctx.author.roles:
        return True
    else:
        await ctx.send(f'Désolé, vous n\'êtes pas autorisé à créer un ticket. Veuillez contacter un modérateur.')
        return False

# créer un ticket sur demande










@bot.tree.command(name="warn")
async def warn(interaction: discord.Interaction, member: discord.Member):
    # Enregistrer l'avertissement dans une base de données ou un fichier
    await interaction.response.send_message(f'{member.mention} a été averti')

@bot.tree.command(name="pardonwarn")
async def pardonwarn(interaction: discord.Interaction, member: discord.Member):
    # Retirer l'avertissement de la base de données ou du fichier
    await interaction.response.send_message(f'{member.mention} a été pardonné')

@bot.tree.command()
@commands.has_permissions(administrator=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role_name: str):
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await interaction.response.send_message(f"Le rôle {role_name} a été ajouté à {member.name} !") # Envoyer un message de confirmation.
    else:
        await interaction.response.send_message(f"Le rôle {role_name} n'existe pas dans ce serveur.") # Envoyer un message d'erreur si le rôle n'existe pas.


@bot.command()
async def tickets(ctx):
    guild = ctx.guild
    author = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    category = discord.utils.get(guild.categories, name='Tickets')
    if category is None:
        category = await guild.create_category(name='Tickets')

    channel = await category.create_text_channel(name=f'ticket-{author.display_name}', overwrites=overwrites)

    embed = discord.Embed(title="Ticket créé !",
                          description=f"Un salon de ticket a été créé pour vous, {author.mention}. Cliquez sur le bouton pour accéder au ticket.",
                          color=discord.Color.green())
    button = discord.ui.Button(label="Ouvrir le ticket", url=channel.mention, style=discord.ButtonStyle.URL)
    view = discord.ui.View()
    view.add_item(button)

    await ctx.send(embed=embed, view=view)












@bot.tree.command()
async def logo(interaction:discord.Interaction):
    await interaction.response.send_message("https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f" {thing_to_say} ")


# @bot.tree.command()
# @app_commands.describe(nombre = "Combien de messages voulez vous suprimez ?")
# async def clear(interaction: discord.Interaction, nombre: str):
#     await interaction.response.send_message(limit=amount)






@bot.command(name="translate")
async def translate(ctx, lang, *, text):
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    params = {
        "q": text,
        "target": lang
    }
    response = requests.post(url, params=params).json()
    translation = response["data"]["translations"][0]["translatedText"]

    await ctx.send(f"La traduction de '{text}' en {lang} est : {translation}")



@bot.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'mon ping est de {bot.latency}')















def isOwner(ctx):
    return ctx.message.author.id == 946704652798402581



@bot.tree.command()
@commands.check(isOwner)
async def private(interaction: discord.Interaction):
    await interaction.response.send_message("Cette commande peut seulement etre effectuées par le propriétaire du bot !", ephemeral=True)


@bot.tree.command()
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfPerson = server.member_count
    serverName = server.name
    serverDescription = server.description
    embed = discord.Embed(title="Informations sur le serveur", color=0xcd2323)
    embed.set_author(name="DockBot",
                     icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/996452655796858970/1074410407294402690/server-1064007844-PhotoRoom.png-PhotoRoom.png")
    embed.add_field(name="Le serveur :", value=str(serverName), inline=True)
    embed.add_field(name="Nombres de membres", value=str(numberOfPerson) + " personnes", inline=False)
    embed.add_field(name="Description du serveur :", value=str(serverDescription), inline=True)
    embed.add_field(name="Nombres de salons écrits:", value=str(numberOfTextChannels) + " Salons écrit", inline=False)
    embed.add_field(name="Nombres de salons vocaux ", value=str(numberOfVoiceChannels) + " salons vocaux", inline=True)
    embed.set_footer(text="By Sitylist94")


    await interaction.response.send_message(embed=embed)


@bot.command()
async def start(ctx, secondes=5):
    changeStatus.change_interval(seconds=secondes)


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


def good_channel(ctx):
    return ctx.message.channel.id == 724977575696400435











@tasks.loop(seconds=5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


@bot.tree.command()
@commands.has_permissions(administrator=True)
async def mute(interaction: discord.Interaction, member: discord.Member, time: int):
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    embed = discord.Embed(title="Mute", description=f"{member} a été mute pour {time} minutes ", color=0xff0000)
    embed.set_author(name="Dockbot",
                     icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
    embed.set_thumbnail(url="https://tse2.mm.bing.net/th?id=OIP.uxkFQJEzg_ZAORzeAupCfwHaGn&pid=Api&P=0%22")
    embed.set_footer(text="made by Sitylist94")
    await interaction.response.send_message(embed=embed)
    await member.add_roles(mute_role)

    await asyncio.sleep(time * 60)

@bot.command(name="meme")
async def meme(ctx):
    try:
        response = requests.get("https://api.imgflip.com/get_memes").json()
        memes = response["data"]["memes"]
        random_meme = random.choice(memes)
        url = random_meme["url"]
        await ctx.send(url)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


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


@bot.tree.command()
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


@bot.tree.command()
async def number(interaction: discord.Interaction, num: int):
    x = random.randint(0, num)
    embed = discord.Embed(title="Nombre aléatoire", description="Trouve un nombre aléatoire ", color=0xd91212)
    embed.set_author(name="Dockbot")
    embed.set_thumbnail(url="https://tse4.mm.bing.net/th?id=OIP.pFzi6bMyJLmmMQ9ydb9thwHaE8&pid=Api&P=0")
    embed.add_field(name="Le nombre est : " + str(x), value="", inline=True)
    embed.set_footer(text="By Sitylist94")
    await interaction.response.send_message(embed=embed)









@bot.command()
async def poll(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.send('Il faut au moins deux options pour faire un sondage.')
        return

    message = await ctx.send(f'Sondage: {question}\n' + '\n'.join(f'{index}: {option}' for index, option in enumerate(options)))
    for emoji, option in zip(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'][:len(options)], options):
        await message.add_reaction(emoji)
    await ctx.message.delete()

@bot.command()
async def reminder(ctx, time, *, task):
    await ctx.send(f"Je vais vous rappeler {task} dans {time} minutes")
    await asyncio.sleep(int(time))
    await ctx.send(f"Rappel : {task}")

quotes = [
    "Avec de la persévérance, tout est possible.",
    "L'échec est la première étape vers le succès.",
    "N'ayez pas peur de prendre des risques. Les plus grands réalisateurs ont échoué avant de réussir.",
    "Si vous pouvez rêver, vous pouvez le faire.",
    "Le succès n'est pas définitif, l'échec n'est pas fatal : c'est le courage de continuer qui compte.",
    "Croire en soi, c'est déjà être à mi-chemin du succès."
]

@bot.command(name='roll')
async def roll(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'Le résultat du lancement de dés est : {dice}')








bot.run(TOKEN)
# Dockbot V0.0.1 pre-release 3
