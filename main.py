import discord
from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord import client
from itertools import cycle
import asyncio
import random
import datetime
import json

#Stato & Prefix
client = commands.Bot(command_prefix="j.")
status = cycle(['Il mio comando è j.help!', 'Mettimi uno status secondario'])

client.remove_command("help")

@client.event
async def on_ready():
  change_status.start()
  print('Il Bot è online!')

@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

#Categorie
@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Usa j.help <comando> per maggiori informazioni.",color = ctx.author.color)

  em.add_field(name = "Moderation", value = "clear - kick - ban - unban")

  em.add_field(name = "Commands", value = "language - support")

  em.add_field(name = "Games", value = "tictactoe")

  await ctx.send(embed = em)

#Help commands
@help.command()
async def language(ctx):

  em = discord.Embed(title = "language", description = "Quale programma sono stato usato?")

  em.add_field(name = "**Syntax**", value = "j.language")

  await ctx.send(embed = em)

@help.command()
async def support(ctx):

   em = discord.Embed(title = "support", description = "Hai trovato bugs? Vuoi un bisogno di aiuto? Hai trovato errori? Questo comando fa per te!")

   em.add_field(name = "**Syntax**", value = "j.support")

   await ctx.send(embed = em)

@help.command()
async def clear(ctx):

  em = discord.Embed(title = "clear", description = "Elimina messaggi fino a 500 messaggi! (Attenzione! aggiungi un numero extra per il comando che hai eseguito! Se non puoi eseguire questo comando, devi avere il permesso di gestire i messaggi!")

  em.add_field(name = "**Syntax**", value = "j.clear <amount>")

  await ctx.send(embed = em)

@help.command()
async def unban(ctx):

  em = discord.Embed(title = "unban", description = "sbanna un utente, ma attenzione! Se non sei in grado di eseguire questo comando, il bot deve essere più alto del ruolo che l'utente ha o non ha i permessi per bannare e cacciare gli utenti (si consiglia di metterlo in cima)")

  em.add_field(name = "**Syntax**", value = "j.unban")

  await ctx.send(embed = em)

@help.command()
async def kick(ctx):

  em = discord.Embed(title = "kick", description = "kicka un utente che hai menzionato! Se non sei in grado di eseguire questo comando, devi essere autorizzato a kickare gli utenti!")

  em.add_field(name = "**Syntax**", value = "j.kick <@mention user>")

  await ctx.send(embed = em)

@help.command()
async def ban(ctx):

  em = discord.Embed(title = "ban", description = "Bannare per sempre un utente che hai citato! Se non sei in grado di eseguire questo comando, devi avere l'autorizzazione per bannare gli utenti!")

  em.add_field(name = "**Syntax**", value = "j.ban <@mention user>")

  await ctx.send(embed = em)

@help.command()
async def tictactoe(ctx):

  em = discord.Embed(title = "tictactoe", description = "Se vuoi giocare a TRIS devi menzionare 2 giocatori")

  em.add_field(name = "**1 comando:**", value = "j.tictactoe [@player 1] [@player 2]")

  em.add_field(name = "**2 comando:**", value = "j.usa <1 to 9>")

  await ctx.send(embed = em)

#Moderation
@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=500):
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason = "No reason provided"):
    await member.send("It was kicked by the server!, **Reason**: "+reason)
    await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason = "No reason provided"):
    await ctx.send(member.name + " has been banned from the server! **Reason**: "+reason)
    await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator)==(member_name, member_disc):

             await ctx.guild.unban(user)
             await ctx.send(member_name +" has been unbanned!")
             return
    await ctx.send(member+" was not found")

#Tris
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("Un gioco è già in corso! Finiscilo prima di iniziarne uno nuovo.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " ha vinto!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("E' pareggio!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("non è tuo turno ora.")
    else:
        await ctx.send("Per iniziare una nuova partita, digita j.tictactoe")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@player 1/2>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

#Commands
@client.command()
async def language(ctx):
  await ctx.send("Sono stato programmato in **Python**")

@client.command()
async def support(ctx):
  await ctx.send("Link di supporto: **Coming Soon**")

#TOKEN
keep_alive()
client.run('XXX') #XXX sta per TOKEN del vostro bot
