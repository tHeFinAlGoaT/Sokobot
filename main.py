import discord
from discord.ext import commands
import random


TOKEN = "supersecrettokenthatiwillnotbesharing"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Name: {bot.user.name}")
    print(f"ID: {bot.user.id}")

 
@bot.command()
async def sokobot(ctx):

    # Define the board and channel
    global board, star_x, star_y, flushed_x, flushed_y, x_x, x_y

    #used to generate random positions for the emojis
    def random_position():
        x = random.randint(1, 7)
        y = random.randint(1, 4)
        return x, y

    channel = ctx.channel

    # Create the 9x6 board
    board = []

    for i in range(9):
        board.append([])
        for j in range(6):
            board[i].append("⬜️")



    # Place the star, player (flushed), and x emoji
    star_x, star_y = random_position()
    board[star_x][star_y] = "⭐️"

    flushed_x, flushed_y = random_position()
    board[flushed_x][flushed_y] = ":flushed:"

    x_x, x_y = random_position()
    board[x_x][x_y] = "❌"

    # String the board (it is currently a list of lists)
    str_board = "\n".join(["".join(row) for row in board])

    # Create the embed
    embed = discord.Embed(
        colour=discord.Colour.dark_teal(),
        title="Sokobot",
        description=str_board
    )

    # Send the embed
    message = await channel.send(embed=embed)

    # React with controls
    await message.add_reaction("⬅️")
    await message.add_reaction("⬆️")
    await message.add_reaction("⬇️")
    await message.add_reaction("➡️")




#moving function (on reaction add)
@bot.event
async def on_reaction_add(reaction, user):

    global board, star_x, star_y, flushed_x, flushed_y, x_x, x_y

    # Define message and channel
    message = reaction.message
    channel = message.channel

    # If the user is the bot, return
    if user == bot.user:
        return

    # Move the player or return
    if reaction.emoji == "➡️":
        board[flushed_x][flushed_y] = "⬜️"
        flushed_y += 1
    elif reaction.emoji == "⬅️":
        board[flushed_x][flushed_y] = "⬜️"
        flushed_y -= 1
    elif reaction.emoji == "⬆️":
        board[flushed_x][flushed_y] = "⬜️"
        flushed_x -= 1
    elif reaction.emoji == "⬇️":
        board[flushed_x][flushed_y] = "⬜️"
        flushed_x += 1
    else:
        return
    
    # If the player is on the star, move the star
    if board[flushed_x][flushed_y] == board[star_x][star_y]:
        if reaction.emoji == "➡️":
            star_y += 1
        elif reaction.emoji == "⬅️":
            star_y -= 1
        elif reaction.emoji == "⬆️":
            star_x -= 1
        elif reaction.emoji == "⬇️":
            star_x += 1

    # If the star is on the x, player wins. Messages are deleted and a win message is sent
    if board[star_x][star_y] == board[x_x][x_y]:
        await message.delete()
        await channel.send("You Won GGS ez!")
    
    # Update the board
    board[star_x][star_y] = "⭐️"
    board[flushed_x][flushed_y] = ":flushed:"

    # String the board (it is currently a list of lists)
    str_board = "\n".join(["".join(row) for row in board])

    # Create the embed
    embed = discord.Embed(
        colour=discord.Colour.dark_teal(),
        title="Sokobot",
        description=str_board
    )

    # Edit the embed (update the board)
    channel = reaction.message.channel
    message = await reaction.message.edit(embed=embed)



    



bot.run(TOKEN) #run the bot
