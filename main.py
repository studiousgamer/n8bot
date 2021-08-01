import discord
from discord.ext import commands
import aiohttp
from config import Config
from logger import Logger
import datetime
import motor.motor_asyncio
from cogs.utils.db_models import levelling,currency,tags

class N8Bot(commands.Bot):
    def __init__(self):       

        self.config = Config
        self.start_time = datetime.datetime.utcnow()

        super().__init__(command_prefix=self.config.PREFIX,
                         intents=discord.Intents.all(),
                         activity=discord.Activity(type=discord.ActivityType.watching, name=self.config.STATUS))



        for cog in self.config.INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f"Exception occurred while loading Cog {cog} : {e}")
            else:
                print(f"Cog {cog} loaded successfully")

            
        self.logger = Logger()
    
    async def _setup_db(self):
        await self.logger.info(f"Connecting to database")
        try:
            self.db = motor.motor_asyncio.AsyncIOMotorClient(self.config.DATABASE_URL)
        except Exception as e:
            await self.logger.error(f"Failed to connect \n{e}")
        else:
            await self.logger.info(f"Connected to database")
            await self.logger.info(await self.db.server_info())
            await self._setup_db_models()

    async def _setup_db_models(self):
        await self.logger.info("Setting up db models")
        self.levelling = levelling.Levelling(self.db)
        self.tags = tags.Tags(self.db)
        self.currecny = currency.Currency(self.db)




    async def on_ready(self):

        await self.logger.info(f"Logged in as {self.user}\nCurrent latency : {round(self.latency*1000)} ms")

        
    async def start(self, token: str, *, reconnect: bool = True):

        self.session = aiohttp.ClientSession(loop=self.loop)
        await self._setup_db()
        await self.logger.info(f"Starting bot with {len(self.config.INITIAL_COGS)} cogs")

        await super().start(token,reconnect=True)

if __name__ == "__main__":
    bot = N8Bot()
    bot.run(Config.TOKEN)