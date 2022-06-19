import requests, nextcord, secrets, asyncio, time, TwitterBot, TelegramBot
credentials = secrets.get_credentials()
testnetURL = "https://api-testnet.FTMScan.com/api?"
morb_token = "0x21830508486b4b28445d1ab1C89bBA7d457Ae47C"
empty_token = "0x0000000000000000000000000000000000000000"
iTime_to_morb = 0
bPost = False
sMessage = ""
iChannel = int(credentials["DiscordChannel"])
ftm_api_key = credentials["FTMScanAPIKey"]
max_morb = 999 # minutes before warning must occur

async def post(message):
    try:
        await dBot.get_channel(iChannel).send(message)
    except:
        "unsuccessful post"
async def post_image(message, image):
    try:
        await dBot.get_channel(iChannel).send(message, image)
    except: 
        "unseccessful post"

async def on_ready():
    try:
        await asyncio.sleep(4)
        #with TelegramBot.TelegramBot() as tBot:
        #    await tBot.getMe()
        print(dBot.user)
    except:
        pass
    pass

async def main_loop():
    await on_ready()
    while True:
        try:
            await get_morbin_time()
            print("next step")
            global bPost, iTime_to_morb
            if bPost:
                print(f"bPost {bPost}")
                sMessage = f"Warning Morbin Time is in {iTime_to_morb} minutes!"
                print(sMessage)
                dBot.loop.create_task(post(sMessage))
                print('first task scheduled')
                #dBot.loop.create_task(post_telegram(sMessage))
                dBot.loop.create_task(post_twitter(sMessage))
                print('second task scheduled')
            bPost = False
            await asyncio.sleep(iTime_to_morb*30) #60 seconds * 1/2
        except:
            bPost = False
            await asyncio.sleep(iTime_to_morb*30)

async def post_telegram(msg):
    print("Telegram")
    try:
        with TelegramBot.TelegramBot() as telegram_bot:
            await telegram_bot.post(msg)
    except Exception as e:
        print("Something is wrong with the telegram bot: ", str(e))
    

async def post_twitter(msg):
    print("Twitter")
    try:
        twitter_bot = TwitterBot.TwitterBot()
        await twitter_bot.handle_bot(msg)
    except Exception as e:
        print("Something is wrong with the Twitter bot \n", str(e))

async def get_morbin_time():
    print("getMorbinTime")
    request = f"{testnetURL}module=account&action=txlist&address={morb_token}&startblock=0&endblock=9999999&page=1&offset=1&sort=desc&apikey={ftm_api_key}"
    print(request)
    result = requests.get(request).json()["result"][0]
    print(result)
    global iTime_to_morb, bPost
    iTime_to_morb = (int(time.time()) - int(result["timeStamp"])) // 60
    print(iTime_to_morb < max_morb)
    if iTime_to_morb < max_morb:
        bPost= True

dBot = nextcord.Client()
dBot.loop.create_task(main_loop())
#print(', '.join("%s: %s" % item for item in attrs.items()))
dBot.run(credentials['DiscordAPIKey'])