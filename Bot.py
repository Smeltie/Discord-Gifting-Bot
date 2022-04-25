## Importing required libraries
import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
import random
import time
import asyncio

## Set the prefix
prefix = "$"

## Optional Drop count (currently unused)
global drops
drops = 0

## List of items
global game
game = [("ITEM_NAME", "IMAGE_URL")
]

## Remove Bots default help command
bot = commands.Bot(command_prefix = prefix)
bot.remove_command("help")

## starting the bot and setting status
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('BOT_PLAYING_STATUS'))
    print("Bot is ready to go and make people happy")

## Help command
@bot.command()
async def help(ctx):
    await ctx.send("I give away gifts, not much else to it")

## Main command handling the gifting
@bot.command()
async def gift(ctx):
    global drops
    global game
## Check if the person dropping the gift is permitted
    if ctx.message.author.id == BOT_OWNER_ID:
        giftresult = random.choice(game)
        giftembed=discord.Embed(title="A random gift has appeared", description="react with :gift: to claim this gift", color=0xf04642)
        giftembed.set_image(url="GIFT_IMAGE_URL")
        giftembed.set_footer(text="Bot developed by Smeltie", icon_url="https://i.imgur.com/HE74l9P.png")
        message = await ctx.send(embed=giftembed)
        await message.add_reaction('🎁')
        role = ctx.guild.get_role(REQUIRED_ROLE)
        def check(reaction, user):
            if role in user.roles:
                return user.id not in (BLACKLISTED_UIDS) and str(reaction.emoji) == '🎁' 

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
        except asyncio.TimeoutError:
            await ctx.send("No one claimed the gift so it dissapeared again.")
            await message.delete()
        else:
            drops += 1
            await message.delete()
            await ctx.send(f"{user.mention} has claimed a gift")
            openembed=discord.Embed(title=(f"{user.name}" " has claimed " f"{giftresult[0]}"), description=("DM <@BOT_OWNERID> to claim your gift"), color=0xf04642)
            openembed.set_image(url=f"{giftresult[1]}")
            openembed.set_footer(text="Bot developed by Smeltie", icon_url="https://i.imgur.com/HE74l9P.png")
            await ctx.send(embed=openembed)
        False
    else: 
        await ctx.send('Invalid permission')

## Bot token
bot.run('BOT_TOKEN')
