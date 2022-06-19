import requests, nextcord, secrets, asyncio, time, TwitterBot, TelegramBot
credentials = secrets.get_credentials()
testnetURL = "https://testnet.FTMScan.com/address/api?"
morb_token = ""
empty_token = ""
ftm_api_key = credentials["FTMScanAPIKey"]
class DiscordBot(nextcord.Client):
    def __init__(self):
        self.iTime_to_morb = 0
        self.bPost = False
        self.loop.create_task(self.on_ready)
        self.iChannel = int(credentials["DiscordChannel"])
        self.sMessage = ""

    async def post(self, message):
        self.get_channel(self.iChannel).send(message)

    async def post(self, message, image):
        self.get_channel(self.iChannel).send(message, image)

    async def on_ready(self):
        asyncio.sleep(10)
        with TelegramBot.TelegramBot() as tBot:
            await TelegramBot.getMe()
        print(self.user)
        pass

    async def loop(self):
        while True:
            await self.on_ready()
            await self.get_morbin_time()
            if self.bPost:
                self.sMessage = f"Warning Morbin Time is in {self.iTime_to_morb} minutes!"
                self.loop.create_task(self.post(self.sMessage))
                self.loop.create_task(self.post_telegram(self.sMessage))
                self.loop.create_task(self.post_twitter(self.sMessage))
            self.bPost = False
            if self.iTime_to_morb != 0:
                await asyncio.sleep(self.iTime_to_morb*30) #60 seconds * 1/2
    
    async def post_telegram(self):
        with TelegramBot.TelegramBot() as telegram_bot:
            telegram_bot.post(self.sMessage)
        pass
    
    async def post_twitter(self):
        with TwitterBot.TwitterBot() as twitter_bot:
            twitter_bot.handle_bot(self.sMessage)
        pass

    async def get_morbin_time(self):
        request = testnetURL 
        + f"module=account&action=txlist&address={morb_token}"
        + f"&startblock=0&endblock=9999999&page=1&offset=1&sort=desc&apikey={ftm_api_key}"
        result = requests.get(request).json
        self.iTime_to_morb = (int(time.time()) - result["timeStamp"]) // 60
        if self.iTime_to_morb < 10:
            self.bPost= True

dBot = DiscordBot()