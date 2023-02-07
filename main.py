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



@bot.command(name="movies")
async def movies(ctx, genre: str):
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
        await ctx.send(response)
    else:
        response = f"Sorry, I don't have information on {genre} movies."
        await ctx.send(response)

@bot.command(name="joke")
async def joke(ctx):
    jokes = [ "Pourquoi les poules ont-elles des plumes ? Parce qu'elles n'ont pas de sous-vêtements !",
        "Comment appelle-t-on un canard qui n'a pas de place pour se poser ? Un dindon !",
        "Pourquoi les poissons ne jouent-ils pas aux échecs ? Parce qu'ils préfèrent la dam-nation !",
        "Pourquoi les vaches ne vont pas à la plage ? Parce qu'elles ne savent pas nager !",
        "Pourquoi les lions ne vont pas à l'école ? Parce qu'ils sont déjà des rois !",]
    response = random.choice(jokes)
    await ctx.send(response)

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(993964162151624724)
    embed = discord.Embed(title="Dockbot", description="Bienvenue", color=0xd30e0e)
    embed.set_thumbnail(url="https://tse3.mm.bing.net/th?id=OIP.2EalQr5cFOyK3aBRv9gZxgHaEK&pid=Api&P=0")
    embed.set_footer(text="By Sitylist94")
    await channel.send(embed=embed)
    await channel.send(f"Acceuillons a bras ouvert {member.mention} ! Bienvenue dans ce magnifique serveur :)")

@bot.command()
async def calculate(ctx,*, expression: str):
    try:
        result = eval(expression)
        await ctx.send(f"Le résultat est: {result}")
    except:
        await ctx.send("Expression mathématique incorrecte.")


@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(993964243382714399)
    embed = discord.Embed(title="Dockbot", description="Au-revoir", color=0xd30e0e)
    embed.set_thumbnail(url="https://tse2.mm.bing.net/th?id=OIP.UHVK4beyOuKhDRXcfyKuSwAAAA&pid=Api&P=0")
    embed.set_footer(text="By Sitylist94")
    await channel.send(embed=embed)
    await channel.send(f"En cette belle journée nous déplorons la perte d'un membre bien aimé,: {member.mention})")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question):
    responses = [
        "C'est certain.",
        "Sans aucun doute.",
        "Il est probable.",
        "Oui - absolument.",
        "Tu peux compter sur ça.",
        "Comme je le vois, oui.",
        "Probablement.",
        "Bonne perspective.",
        "Oui.",
        "Les signes pointent vers oui.",
        "Réponse incertaine, essaye à nouveau.",
        "Pose la question à nouveau plus tard.",
        "Mieux vaut ne pas te dire maintenant.",
        "Je ne peux pas prédire maintenant.",
        "Concentre-toi et pose la question à nouveau.",
        "N'y compte pas.",
        "Ma réponse est non.",
        "Mes sources disent non.",
        "Outlook pas bon.",
        "Très peu probable."
    ]
    await ctx.send(f"Question : {question}\nRéponse : {random.choice(responses)}")

@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.add_reaction(reaction.emoji)


@bot.command()
async def hello(ctx, user: discord.User):
    await ctx.send(f"Bonjour {user.name} !")


@bot.command()
async def dm(ctx, user: discord.User):
    target_user = discord.utils

    target_user = discord.utils.get(bot.get_all_members(), name='Target User')
    private_channel = await target_user.create_dm()
    await target_user.create_dm()
    await private_channel.send('Hello, this is a private message!')


@bot.command(name="traduire")
async def translate(ctx, lang: str, text: str):
    translator = Translator(service_urls=['translate.google.com'])
    result = translator.translate(text, dest=lang)
    await ctx.send(f"Traduction: {result.text}")


@bot.command()
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)


@bot.command()
async def bonjour(ctx):
    serverName = ctx.guild.server.name
    await ctx.send(
        f"Bonjour jeune *padawan* ! Savais tu que tu te trouvais dans le serveur *{serverName}*, c'est d'ailleurs un super serveur puisque **JE** suis dedans.")





@bot.command(name='role')
async def role(ctx, role: discord.Role):
    user = ctx.message.author
    if not ctx.message.author.guild_permissions.manage_roles:
        await ctx.send("Vous n'avez pas la permission de gérer les rôles.")
        return
    if role in user.roles:
        await ctx.send(f'{user.mention} a déjà le rôle {role.name}.')
    else:
        await user.add_roles(role)
        await ctx.send(f'{user.mention} a maintenant le rôle {role.name}.')





@bot.command()
async def hein(ctx):
    await ctx.send("Payay !!!")


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

    def isOwner(ctx):
        return ctx.message.author.id == 946704652798402581


def isOwner(ctx):
    return ctx.message.author.id == 946704652798402581


@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette commande peut seulement etre effectuées par le propriétaire du bot !")


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
        await ctx.send("Oups vous ne pouvez iutilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")


def good_channel(ctx):
    return ctx.message.channel.id == 724977575696400435


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


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


@tasks.loop(seconds=5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)


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




@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, time: int):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(mute_role)
    await ctx.send(f"{member} a été mute pour {time} minutes ")

    await asyncio.sleep(time * 60)

    await member.remove_roles(mute_role)
    await ctx.send(f"{member} a été unmute après {time} minutes.")


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


@bot.command()
@commands.has_permissions(kick_members=True)
async def eject(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
    await ctx.guild.kick(user, reason=reason)
    embed = discord.Embed(title="**Expulsion**", description="Un modérateur a frappé !")
    embed.set_thumbnail(
        url="https://sbedirect.com/4672-home_default/danger-sign-pictogram-for-electric-hazard-blast.jpg")
    embed.add_field(name="Membre expulsé", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.set_footer(text=random.choice(funFact))

    await ctx.send(embed=embed)


@bot.command()
async def exclure(ctx, user: discord.User, *, reason="Aucune raison n'a été donné"):
    await ctx.guild.timeout(user, reason=reason)
    embed = discord.Embed(title="**exclusion**", description="Un modérateur a frappé !")
    embed.set_thumbnail(
        url="https://cdn2.iconfinder.com/data/icons/miscellaneous-245-color-shadow/128/exclusion_cancel_negation_boycott_rejection_embargo_disallowance_inhibition-256.png")
    embed.add_field(name="Membre exclu", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.set_footer(text=random.choice(funFact))

    await ctx.send(embed=embed)


@bot.command()
async def number(ctx, num: int):
    x = random.randint(0, num)
    await ctx.send(f"Votre nombre est {x}")


@bot.command(name='quote')
async def quote(ctx):
    await ctx.send(f'Citation aléatoire: "{random.choice(quotes)}"')


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




bot.run("TOKEN")

# Dockbot V0.0.1
