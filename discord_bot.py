import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_TOKEN="MTA2ODA1MTc2Njc2OTM2OTE0OA.GctSRx.hyM9t5JaVRo--1wGZCxQ2Ib-TN5Wy96ZC_j3NA"

bot = commands.Bot(command_prefix='>', self_bot=True)

@bot.event
async def on_ready():
    print("-"*20, f"\nLogged in as: \nUser: {bot.user.name} \nID: {bot.user.id}")
    channel = bot.get_channel(1068234179562717286)
    print(channel)

    # async for command in ctx.slash_commands():
    #     print(command.name)

    # await channel.send("/imagine prompt: \tDetermined man reaching for stars, contrasting colors.")

# @bot.command()
# async def who(ctx, user: discord.User):
#     await ctx.send(f"Username: {user.name}#{user.discriminator}\nID: {user.id}")

@bot.event  
async def on_message(message):
    # print(message.author.id)
    # if message.author == bot.user:
    # print(message.content)
    # print(message)
    async for command in message.channel.slash_commands():
        print("cmd: ", command.name)
#     # await bot.process_commands(message)

#     # if message.channel.id == 1068062846707056664:
#     #     print(message.content)
#     #     # if "kaptaan" in message.content:
#     #     print(f"Message Received for you: {message.content}")
#     #     # await message.add_reaction('\N{THUMBS UP SIGN}')
#     # # else:
#     # #     print("Not a message for you")
#         if message.author == bot.user:
#             return
#         if message.channel.id == 1068234179562717286:
#             try:
#                 attachments = await wait_for_message(bot, message.channel, "kaptaan", timeout=180)
#             except Exception as e:
#                 print(e)
#                 # await message.channel.send(str(e))
#             # else:
#             #     for i, attachment in enumerate(attachments):
#             #         await message.channel.send(f"Attachment {i+1}: {attachment}")
#         await bot.process_commands(message)

# async def wait_for_message(client, channel, username, timeout=180):
#     def check(message):
#         return message.channel == channel and username in message.content
#     try:
#         msg = await client.wait_for('message', check=check, timeout=timeout)
#     except asyncio.TimeoutError:
#         raise Exception("Timed out waiting for message.")
#     else:
#         attachments = []
#         for attachment in msg.attachments:
#             file = await attachment.to_file()
#             attachments.append(file)
#             file.save(f"{file.filename}") # Save the file to disk
#         return attachments


bot.run(DISCORD_TOKEN)
