import nextcord as n, random, datetime, json as j, math, requests as r, time as t
from nextcord.ext import commands
from nextcord import SlashOption
from MeowerBot import Bot

intents = n.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="Sb4bot.", intents=intents)
bot2 = Bot()

@bot.slash_command(name="help", description="shows all available commands")
async def help(interaction: n.Interaction):
	helplist = []
	helplist.append("List of commands:")
	helplist.append("/help: Shows this text.")
	helplist.append("/echo: Displays what you sent as an argument.")
	helplist.append("/minesweeper <bombs> <width> <length>: Generates a random minesweeper puzzle with the specs you sent as arguments.")
	helplist.append("/lvl: Tells you your level and how much xp you have.")
	await interaction.response.send_message("\n".join(helplist))

@bot.slash_command(name="minesweeper", description="generates a random minesweeper puzzle")
async def minesweeper(interaction: n.Interaction, bombs: int = SlashOption(required=True, description="How many bombs are in the minesweeper puzzle."), width: int = SlashOption(required=True, description="Width of the minesweeper puzzle."), length: int = SlashOption(required=True, description="Length (or height) of the minesweeper puzzle.")):
	grid = []

	if bombs >= (width * length - 9) or width < 1 or length < 1:
		await interaction.response.send_message("too many bombs for the specified length and width")
		return "stopped"

	grid = [[0 for i in range(width)] for i in range(length)]

	while bombs > 0:
		row = random.randint(0, length - 1)
		column = random.randint(0, width - 1)
		if grid[row][column] != "💣":
			grid[row][column] = "💣"
			bombs -= 1

	for i in range(length * width):
		row = i // width
		column = i % width
		if grid[row][column] == "💣":
			continue

		if row > 0 and column > 0:
			if grid[row - 1][column - 1] == "💣":
				grid[row][column] += 1

		if row > 0:
			if grid[row - 1][column] == "💣":
				grid[row][column] += 1

		if row > 0 and column < width - 1:
			if grid[row - 1][column + 1] == "💣":
				grid[row][column] += 1

		if column > 0:
			if grid[row][column - 1] == "💣":
				grid[row][column] += 1

		if column < width - 1:
			if grid[row][column + 1] == "💣":
				grid[row][column] += 1

		if row < length - 1 and column > 0:
			if grid[row + 1][column - 1] == "💣":
				grid[row][column] += 1

		if row < length - 1:
			if grid[row + 1][column] == "💣":
				grid[row][column] += 1
	
		if row < length - 1 and column < width - 1:
			if grid[row + 1][column + 1] == "💣":
				grid[row][column] += 1

	for i in range(length * width):
		row = i // width
		column = i % width
		if grid[row][column] == 0:
			grid[row][column] = "||0️⃣||"
		elif grid[row][column] == 1:
			grid[row][column] = "||1️⃣||"
		elif grid[row][column] == 2:
			grid[row][column] = "||2️⃣||"
		elif grid[row][column] == 3:
			grid[row][column] = "||3️⃣||"
		elif grid[row][column] == 4:
			grid[row][column] = "||4️⃣||"
		elif grid[row][column] == 5:
			grid[row][column] = "||5️⃣||"
		elif grid[row][column] == 6:
			grid[row][column] = "||6️⃣||"
		elif grid[row][column] == 7:
			grid[row][column] = "||7️⃣||"
		elif grid[row][column] == 8:
			grid[row][column] = "||8️⃣||"
		elif grid[row][column] == "💣":
			grid[row][column] = "||💣||"

	msg = ""
	for i in range(length):
		msg += f"{str(''.join(grid[i]))}\n"

	await interaction.response.send_message("\n" + msg)

@bot.slash_command(name="echo", description="says what you say")
async def echo(interaction: n.Interaction, message: str = SlashOption(required=True, description="Message to repeat.")):
    await interaction.response.send_message(f"You said {message}!")

@bot.slash_command(name="ban", description="bans a member from the server", default_member_permissions=0)
async def ban(interaction: n.Interaction, user: n.Member = SlashOption(required=True, description="User to ban."), reason: str | None = SlashOption(required=False, description="Reason for the ban.")):
	try:
		await n.Member.ban(user, delete_message_seconds=60, reason=reason)
		await interaction.response.send_message(f"Banned {str(user)} for {reason}.")
	except:
		await interaction.response.send_message("cannot ban that user")

@bot.slash_command(name="unban", description="unbans a member from the server", default_member_permissions=0)
async def unban(interaction: n.Interaction, user: n.Member = SlashOption(required=True, description="User to unban."), reason: str | None = SlashOption(required=False, description="Reason for the unban.")):
	try:
		await n.Member.unban(user, reason=reason)
		await interaction.response.send_message(f"Unbanned {str(user)} for {reason}.")
	except:
		await interaction.response.send_message("user is not banned")

@bot.slash_command(name="kick", description="kicks a member from the server", default_member_permissions=0)
async def kick(interaction: n.Interaction, user: n.Member = SlashOption(required=True), reason: str | None = SlashOption(required=False, description="User to kick.")):
	try:
		await n.Member.kick(user, reason=reason)
		await interaction.response.send_message(f"Kicked {str(user)} for {reason}.")
	except:
		await interaction.response.send_message("cannot kick that user")

@bot.slash_command(name="timeout", description="prevents a member from sending messages", default_member_permissions=8)
async def timeout(interaction: n.Interaction, user: n.Member = SlashOption(required=True, description="User to timeout."), time: str = SlashOption(required=True, description="Timeout duration."), reason: str | None = SlashOption(required=False, description="Reason for the timeout.")):
	if "seconds" in time or "minutes" in time:
		if "seconds" in time:
			time = int(time[:len(time) - 8])
		else:
			time = int(time[:len(time) - 8]) * 60
	elif time == "1 second":
		time = 1
	elif time == "1 minute":
		time = 60
	elif "hours" in time or "weeks" in time:
		if "hours" in time:
			time = int(time[:len(time) - 6]) * 3600
		else:
			time = int(time[:len(time) - 6]) * 604800
	elif time == "1 hour":
		time = 3600
	elif time == "1 week":
		time = 604800
	elif "days" in time:
		time = int(time[:len(time) - 5]) * 86400
	elif time == "1 day":
		time = 86400
	try:
		await n.Member.timeout(user, datetime.timedelta(seconds=time), reason=reason)
		await interaction.response.send_message(f"Put {str(user)} in timeout for {time} seconds for {reason}.")
	except:
		await interaction.response.send_message("cannot timeout that user or error in input")

@bot.slash_command(name="lvl", description="tells you your level and how much xp you have")
async def lvl(interaction: n.Interaction):
	with open("levels.json", "r+") as f:
		f.seek(0)
		data = j.load(f)
		
		lvl = math.floor(math.sqrt(data[interaction.user.name]))
			
		uclass = "Member"
		if lvl >= 5:
			uclass = "Active Member"
		if lvl >= 7:
			uclass = "Fan"
		if lvl >= 9:
			uclass = "Consistent Member"
		if lvl >= 12:
			uclass = "Veteran"
		if lvl >= 15:
			uclass = "Server Addict"
		if lvl >= 20:
			uclass = "Server Cult Member"
		if lvl >= 25:
			uclass = "Server Worshipper"
		
		token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMDQ2MTYxNDk0OTM2MTY2NjAiLCJib3QiOnRydWUsImlhdCI6MTcwODQ2OTgzMH0.YqGz65DT5-O6DS0vQ9rql_9KKxaPVvB1BCDgxySkmDY"
		vote = r.get(f"https://top.gg/api/bots/1204616149493616660/check?userId={interaction.user.id}", headers={"Authorization": token}).json()["voted"]
		add = "\nThank you for voting! 10% boost has been activated for you!" if vote == 1 else "\nDo you want a 10% xp boost?\nThen vote [here](https://top.gg/bot/1204616149493616660/vote)!"
		print(vote)
		await interaction.response.send_message(f"# {interaction.user.name} [{uclass}]\n## Level {lvl}\n### {round(data[interaction.user.name] * 52)}/{(lvl + 1) ** 2 * 52} xp{add}")
		# await interaction.response.send_message("you have not sent a message yet, which is odd")

@bot.event
async def on_message(message: n.Message):
	global author, content, channel, server
	author = message.author
	content = message.content
	channel = message.channel
	server = message.guild.id
	delete = {
		"Sb4bot": 1199528391322370171,
		"fromSb4bot": 1199023494164398170,
		"Fredboat": 1186110546441941025,
		"24/7": 1186380367809216653
	}
	print(f"{author}: {content}")

	if channel.id == delete["Sb4bot"] and not message.author == "Sb4bot#6977":
		await message.delete()
		return
	if channel.id == delete["fromSb4bot"] and (not message.author == "AI Bot#9482" or not message.author == "Dyno#3861"):
		await message.delete()
		return
	if channel.id == delete["Fredboat"] and not message.author == "FredBoat♪♪#7284":
		await message.delete()
		return
	if channel.id == delete["24/7"] and not message.author == "24/7 🔊#6493":
		await message.delete()
		return

	with open("levels.json", "r+") as f:
		global vote
		f.seek(0)
		data = j.load(f)
		if message.author.bot == True:
			return
		t.sleep(4)
		global vote
		token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMDQ2MTYxNDk0OTM2MTY2NjAiLCJib3QiOnRydWUsImlhdCI6MTcwODQ2OTgzMH0.YqGz65DT5-O6DS0vQ9rql_9KKxaPVvB1BCDgxySkmDY"
		vote = r.get(f"https://top.gg/api/bots/1204616149493616660/check?userId={author.id}", headers={"Authorization": token}).json()["voted"]
		boost = 1.1 if vote == 1 else 1
		try:
			old = data[message.author.name]
			lvl = math.floor(math.sqrt(old))
			data[message.author.name] += len(content) / 150 * boost
			f.seek(0)
		except:
			data[message.author.name] = len(content) / 150 * boost
			old = data[message.author.name]
			f.seek(0)
			lvl = math.floor(math.sqrt(old))
		finally:
			newlvl = math.floor(math.sqrt(data[message.author.name]))
			if newlvl > lvl:
				if server == 1186110546001535087:
					if newlvl >= 25:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Worshipper"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a worshipper! You can now manage messages! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 20:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Cult Member"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a member of the cult! You can now send voice messages! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 15:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Addict"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a TheSb4Server addict! You can now create custom invites, create private threads, and send tts messages! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 12:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Veteran"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a veteran! You can now view server insights, mention @everyone, mention @here, mention roles, and be a priority speaker! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 9:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Consistent Member"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a consistent member! You can now create expressions, use external emojis, use external stickers, send voice messages, and manage events! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 7:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Fan"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming a fan! You can now embed links, atatch files, manage threads, use external sounds, and set voice channel statuses! You've also been rewarded with an exclusive chat ;)")
					elif newlvl >= 5:
						await message.author.add_roles(n.utils.get(message.author.guild.roles, name="Active Member"))
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations on becoming an active member! You can now use the server soundboard and create events! You've also been rewarded with an exclusive chat ;)")
					else:
						await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations!")
				else:
					await channel.send(f"<@{message.author.id}> has reached level {newlvl}! Congratulations!")
			j.dump(data, f, indent=4)
			f.truncate()

bot.run("not telling you haha the upload is fake")
