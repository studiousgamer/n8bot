import aiohttp
from config import Config
import json
from datetime import datetime

class Logger:

    def __init__(self):
        pass

    async def _send_webhook(self,event_type : str, color : int,message : str, content : str = ""):

        time = datetime.now()
        time = time.strftime("%x %X")
        data = {
        "content" : content,
        "embeds" : [
            {   
                "title" : event_type,
                "description" : message,
                "color" : color,
                "footer": {
                    "text": time,
                }
            }
        ]}
  
        header = {
            "Content-Type" : "application/json"
        }
        async with aiohttp.ClientSession() as session:
            
            async with session.post(Config.WEBHOOK_URL,data=json.dumps(data),headers=header) as response:

                if response.status < 300 and response.status > 200:
                    return True
            

    async def info(self,message : str):
        await self._send_webhook("info",Config.LOG_COLOR,f"```{message}```")

    async def warning(self,message : str):
        await self._send_webhook("Warning",Config.WARNING_COLOR,f"```{message}```")

    async def error(self,message : str):
        await self._send_webhook("Error",Config.ERROR_COLOR,f"```{message}```",content=f"<@&{Config.DEV_ROLE_ID}>")


