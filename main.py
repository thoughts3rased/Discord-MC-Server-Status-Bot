import discord
from discord.ext import tasks, commands
import mcstatus
from mcstatus import MinecraftServer
TOKEN = 'Nzk1MDg5MjMzNDcxMzQwNTc1.X_ESjQ.cMokQjOzO8k17gwKdLRsRiUe9YQ'
PREFIX = '!'
INTENTS = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkServer.start()
    def cog_unload(self):
        self.checkServer.cancel()
    @tasks.loop(minutes=0.25)
    async def checkServer(self):
        try:
            server = MinecraftServer("164.132.149.15", 25565)
            status = server.status()
            if status.players.online == 0:
                await bot.change_presence(status = discord.Status.idle, activity = discord.Game(name = "There are no players online."))
            elif status.players.online >= 1:
                await bot.change_presence(status = discord.Status.online, activity = discord.Game(name = "There is 1 player online."))
            elif status.players.online > 1:
                await bot.change_presence(status = discord.Status.online, activity = discord.Game(name = "There are "+ str(status.players.online)+" players online.")) 
        except:
            await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = "Server is offline."))
    @checkServer.before_loop
    async def before_loop(self):
        print("Waiting on load for loop.")
        await self.bot.wait_until_ready()
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    bot.add_cog(Loops(bot))
bot.run(TOKEN)