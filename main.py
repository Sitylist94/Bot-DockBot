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

@bot.command
async def Ytb(ctx):
	await ctx.send("En travaux.....")

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

async def getMutedRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "Muted":
			return role

	return await createMutedRole(ctx)

@bot.command()
async def bonjour(ctx):
	serverName = ctx.guild.server.name
	await ctx.send(f"Bonjour jeune *padawan* ! Savais tu que tu te trouvais dans le serveur *{serverName}*, c'est d'ailleurs un super serveur puisque **JE** suis dedans.")

@bot.command()
async def coucou(ctx):
	await ctx.send("Coucou !")

@bot.command()
async def role(ctx, *,nom):
	roleMembre = ""
	roles = ctx.guild.roles
	for role in roles:
		if role.name == nom:
			roleMembre = role
	if roleMembre == "":
		roleMembre = await ctx.guild.create_role(name = nom, reason = "Un membre a fait la commande role.")
	await ctx.message.author.add_roles(roleMembre, reason = "commande")


@bot.command()
async def quoi(ctx):
	await ctx.send("Coubay !!!")

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
		return ctx.message.author.id == IDENTIFIANT



@bot.command()
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


@coucou.error
async def coucou_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("La commande coucou prend en parametre un nombre.")
		await ctx.send("Veuillez réessayer.")

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.check(good_channel)
async def clear(ctx, nombre: int):
	messages = await ctx.channel.history(limit=nombre + 1).flatten()
	for message in messages:
		await message.delete()


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


@bot.command()
async def Help(ctx):
	embed = discord.Embed(title="Help", description="Rechercher une commande", color=0xff1f1f)
	embed.set_author(name="Dockbot", icon_url="https://cdn.discordapp.com/attachments/996452655796858970/1058807579855290518/th_4.jpg")
	embed.add_field(name="ban ", value="Bannir un membre", inline=True)
	embed.add_field(name="clear", value="effacer un/plusieurs messages", inline=False)
	embed.add_field(name="coucou ", value="Dire coucou :D", inline=False)
	embed.add_field(name="eject  ", value="Ejecter une personne ", inline=False)
	embed.add_field(name="logo  ", value="logo du bot", inline=False)
	embed.add_field(name="number  ", value="Obtenir un nombre aléatoire ", inline=True)
	embed.add_field(name="ping  ", value="Latence du bot", inline=True)
	embed.add_field(name="unmute ", value="Démute une personne", inline=True)
	embed.set_footer(text="By Sitylist94")

	await ctx.send(embed=embed)

bot.run("Token")

# Dockbot V0.0.1
