from operator import indexOf
from queue import Empty
import requests, nextcord, secrets, asyncio, time, TwitterBot, TelegramBot
from enum import Enum
from web3 import Web3
credentials = secrets.get_credentials()
last_winning_block= secrets.get_last_winning_block()
testnetURL = "https://api-testnet.FTMScan.com/api?"
morb_token = "0xc9f4f188cA767227eB26c8e6c619bba13BD6dDa0"
empty_token = "0x0000000000000000000000000000000000000000"
jackpot_min_amt_changed = "0xaf059ee9d42c1ffcd90b59907d307cfab29e5d2ecf6402a5174ad8d4ec4e401b"
jackpot_time_extended = "0xa8162f194f354dc15e429cc707c82c54a8a66cd6415e8e71670f4f404caccc00"
bought_morbius = "0x0000000000000000000000006913f60a53f5408df3175b306dd943e83b3a284e"
its_morbin_time = "0xe6e35173318ce029f42a2f07d65a76cfae9604c672a3c8160109fe4886bdfcbc"
buy_back_for_morbin_time = "0x5e78eb00bb758809ccd7dd288bf7450dd825f4661703d21faa7e3cc392fb571b"
#sold_morbius = "0xb0db0551bcb75964440d0dd0f9449c9b176f08ca4fa1a60b2b1e903bd58b1ac3"
jackpot_award = "0xbb60574db333fcc16f66d64cf8f428581daaf704cf6a01e321d264b6cc0793e6"
max_morb_countdown = 99999 # minutes before warning must occur
decimal_place = 10 ** 18
old_block = secrets.get_last_winning_block()
last_morbtime_block = old_block[0]
last_jackpot_award = old_block[1]
last_morbtime_block_old = old_block[0]
last_jackpot_award_old = old_block[1]

class PostType(Enum):
    Empty = 0
    JackPot = 1
    MorbinTime = 2
    WarningTime = 3
class DiscordBot(nextcord.Client):
    def __init__(self):
        super().__init__()
        self.iTime_to_morb = 0
        self.post_type = PostType.Empty
        self.sMessage = ""
        self.iChannel = int(credentials["DiscordChannel"])
        self.ftm_api_key = credentials["FTMScanAPIKey"]
        self.morb_trigger = 100000
        self.loop.create_task(self.main_loop())

    async def post(self, message):
        try:
            await dBot.get_channel(self.iChannel).send(message)
        except:
            "unsuccessful post"
    async def post_image(self, message, image):
        try:
            await dBot.get_channel(self.iChannel).send(message, image)
        except: 
            "unseccessful post"

    async def on_ready(self):
        try:
            await asyncio.sleep(4)
            #with TelegramBot.TelegramBot() as tBot:
            #    await tBot.getMe()
            print(dBot.user)
        except:
            pass
        pass

    async def parse_hex(self, hex):
        data_count = 0
        hex_data_table = list()
        while data_count < len(hex)//64:
            #print(hex[(data_count)*64-1:data_count*64])
            hex_data_table.append(hex[(data_count)*64:(data_count+1)*64])
            data_count += 1
        
        return hex_data_table

    async def main_loop(self):
        await self.on_ready()
        while True:
            try:
                await self.get_jack_pot_time()
                print("next step")
                
                if self.post_type != PostType.Empty:
                    await self.check_post_type()
            except Exception as e:
                print(e)
                self.post_type = PostType.Empty
            finally:
                print("iTimeToMorb:",self.iTime_to_morb)
                print("Time:", int(time.time()))
                wait_time = max_morb_countdown - ((time.time() - self.iTime_to_morb ) // 30)
                print("Time until next check: ", wait_time)
                await asyncio.sleep(wait_time)

    async def check_post_type(self):
        match self.post_type:
            case PostType.WarningTime:
                sMessage = f"Warning Morbin Time is in {self.iTime_to_morb} minutes!"
                self.loop.create_task(self.send_post(sMessage))
            case PostType.MorbinTime: #ftm bought morb bought morb burned total morb burned total 
                sMessage1 = f"ITS MORBIN TIME! FTM used to buy back VAMP {self.ftm_buyback} Amount of VAMP Burned: {self.morb_burned}."
                sMessage2 = f"MorbinTime has occurred {self.total_morb_count} Total VAMP burned {self.total_morb_burned}. Total FTM used: {self.total_ftm_morb_time}"
                sMessage3 = f"Another {self.jackpot_dollar_ftm:.2f}$ {self.jackpot_ftm_balance} FTM has been seeded into the jackpot!"
                self.loop.create_task(self.send_post(sMessage1))
                self.loop.create_task(self.send_post(sMessage2))
                self.loop.create_task(self.send_post(sMessage3))
            case PostType.JackPot:
                sMessage1 = f"WE HAVE A JACKPOT WINNER!\n {self.jackpot_winner}\n congratulations on winning {self.total_jackpot:.2f}$ with of FTM {self.ftm_award}" 
                sMessage2 = f"Another {self.jackpot_dollar_ftm:.2f}$ {self.jackpot_ftm_balance}FTM has been seeded into the jackpot!"
                sMessage3 = f"The jackpot has been won {self.total_jackpot} times. Total FTM dispersed: {self.total_ftm_award} Total Dollars Won: {self.total_dollar_award:.2f}$"
                sMessage4 = f"{self.ftm_buyback} FTM was used to burn {self.morb_burned} VAMP." 
                sMessage5 = f"Total VAMP burned: {self.total_morb_burned} using {self.total_ftm_burned} FTM"
                self.loop.create_task(self.send_post(sMessage1))
                self.loop.create_task(self.send_post(sMessage2))
                self.loop.create_task(self.send_post(sMessage3))
                self.loop.create_task(self.send_post(sMessage4))
                self.loop.create_task(self.send_post(sMessage5))
            case PostType.Empty:
                return

    async def send_post(self, msg):
        #self.loop.create_task(self.post_telegram(msg))
        self.loop.create_task(self.post(msg))
        #self.loop.create_task(self.post_twitter(msg))

    async def post_telegram(self, msg):
        print("Telegram")
        try:
            with TelegramBot.TelegramBot() as telegram_bot:
                await telegram_bot.post(msg)
        except Exception as e:
            print("Something is wrong with the telegram bot: ", str(e))
        

    async def post_twitter(self, msg):
        print("Twitter")
        try:
            twitter_bot = TwitterBot.TwitterBot()
            await twitter_bot.handle_bot(msg)
        except Exception as e:
            print("Something is wrong with the Twitter bot \n", str(e))
    
    # async def get_morbin_time(self):
    #     print("getMorbinTime")
    #     lastbuyrequest = f"{testnetURL}module=logs&action=getLogs&address={morb_token}&fromblock=0&toblock=9999999&topic1={bought_morbius}&apikey={self.ftm_api_key}"
    #     print("request: ",lastbuyrequest)
    #     lastbuyjson = requests.get(lastbuyrequest).json()
    #     self.last_buyer = lastbuyjson['address']
    #     print("result: ", lastbuyjson)
    #     data = await self.parse_hex_to_int(lastbuyjson['result'][0]['data'].split('x'))
        
    #     await asyncio.sleep(10)
    
        # print(self.iTime_to_morb < self.max_morb)
        # if self.iTime_to_morb > self.max_morb:
        #     self.post_type = PostType.WarningTime
        # if self.iTime_to_morb < self.max_morb:
        #     self.post_type = PostType.MorbinTime
        # self.iTime_to_morb = data[1]

    async def get_jack_pot_time(self):
        jackpot_get_request = f"{testnetURL}module=logs&action=getLogs&fromblock=0&toblock=9999999&address={morb_token}&sort=desc&topic0={jackpot_time_extended}&apikey={self.ftm_api_key}"
        jackpot_json = requests.get(jackpot_get_request).json()
        jackpot_data = await self.parse_hex(jackpot_json['result'][0]['data'].split('x')[1])
        
        self.last_block = jackpot_json['result'][0]["blockNumber"]
        iTStamp = jackpot_json["result"][0]["timeStamp"]
        #iTStamp = await self.parse_hex(iTStamp.split('x')[1])
        print("iTstamp", iTStamp)
        self.iTime_to_morb          = Web3.toInt(hexstr=iTStamp.split('x')[1])
        print("iTimeToMorb: ", self.iTime_to_morb)
        #self.last_buyer             = "0x"+jackpot_data[0]
        self.jackpot_amount_FTM     = Web3.toInt(hexstr=jackpot_data[1])
        self.jackpot_amount_dollar  = Web3.toInt(hexstr=jackpot_data[2])
        #self.iTime_to_morb          = Web3.toInt(hexstr=jackpot_data[3])
        await self.check_morbin_time()

    async def get_jackpot_award(self):
        jackpot_award_get_request = f"{testnetURL}module=logs&action=getLogs&fromblock=0&toblock=9999999&address={morb_token}&topic0={jackpot_award}&apikey="#{self.ftm_api_key}"
        print(jackpot_award_get_request)
        jackpot_award_json = requests.get(jackpot_award_get_request).json()['result']
        jackpot_award_json = jackpot_award_json[len(jackpot_award_json)-1]
        print(jackpot_award_json["blockNumber"])
        jackpot_award_data = await self.parse_hex(jackpot_award_json['data'].split('x')[1])
        self.jackpot_winner = "0x"+jackpot_award_data[0]                        #
        self.last_jackpot_block = jackpot_award_json["blockNumber"]
        print("--------")
        self.ftm_award              = Web3.toInt(hexstr=jackpot_award_data[1])  / float(decimal_place)
        self.ftm_buyback            = Web3.toInt(hexstr=jackpot_award_data[2])  / float(decimal_place)
        self.total_jackpot         = Web3.toInt(hexstr=jackpot_award_data[3]) 
        self.total_ftm_award          = Web3.toInt(hexstr=jackpot_award_data[4])  / float(decimal_place)
        self.total_dollar_award        = Web3.toInt(hexstr=jackpot_award[5])      /float(decimal_place)
        self.total_ftm_burned     = Web3.toInt(hexstr=jackpot_award_data[6])  / float(decimal_place)
        print(self.total_dollar_award)
        
        self.jackpot_ftm_balance    = Web3.toInt(hexstr=jackpot_award_data[7]) / float(decimal_place)
        print(self.jackpot_ftm_balance)
        self.jackpot_dollar_ftm     = Web3.toInt(hexstr=jackpot_award_data[8]) / float(decimal_place)
        print(self.jackpot_dollar_ftm)
        self.timeofaward            = Web3.toInt(hexstr=jackpot_award_data[9])
        print(self.timeofaward)
        print("Amount of FTM given: ",self.ftm_award)

        pass
    async def get_morbinTime(self):
        morbin_time_get_request = f"{testnetURL}module=logs&action=getLogs&fromblock=0&toblock=9999999&address={morb_token}&topic0={its_morbin_time}&apikey="#{self.ftm_api_key}"
        print(morbin_time_get_request)
        morbin_time_json = requests.get(morbin_time_get_request).json()['result']
        morbin_time_json = morbin_time_json[len(morbin_time_json)-1]
        self.last_morbtime = morbin_time_json["blockNumber"]
        morbin_time_data = await self.parse_hex(morbin_time_json['data'].split('x')[1])
        #print("Morbin_time_data: ",morbin_time_data)
        self.ftm_buyback            = Web3.toInt(hexstr=morbin_time_data[0]) / float(decimal_place)
        print(self.ftm_buyback)
        self.total_morb_count       = Web3.toInt(hexstr=morbin_time_data[1])
        print(self.total_morb_count)
        self.total_ftm_morb_time    = Web3.toInt(hexstr=morbin_time_data[2])
        print(self.total_ftm_morb_time)
        self.jackpot_ftm_balance    = Web3.toInt(hexstr=morbin_time_data[3]) / float(decimal_place)
        print(self.jackpot_ftm_balance)
        self.jackpot_dollar_ftm = Web3.toInt(hexstr=morbin_time_data[4]) / float(decimal_place)
        print(self.jackpot_dollar_ftm)
        self.iTime_to_morb          = Web3.toInt(hexstr=morbin_time_data[5])
        print(self.iTime_to_morb)
        pass
    async def get_buy_back_morbin_time(self):
        buyback_morbin_time_get_request = f"{testnetURL}module=logs&action=getLogs&fromblock=0&toblock=9999999&address={morb_token}&topic0={buy_back_for_morbin_time}&apikey={self.ftm_api_key}"
        print(buyback_morbin_time_get_request)
        buyback_morbin_time_json = requests.get(buyback_morbin_time_get_request).json()['result']
        print(buyback_morbin_time_json)
        buyback_morbin_time_json = buyback_morbin_time_json[len(buyback_morbin_time_json)-1]
        morbin_time_data = await self.parse_hex(buyback_morbin_time_json['data'].split('x')[1])
        self.morb_burned            = Web3.toInt(hexstr=morbin_time_data[0])
        print("----------------")
        print(self.morb_burned)
        self.total_morb_burned      = Web3.toInt(hexstr=morbin_time_data[1])
        print(self.total_morb_burned)
       

    async def check_morbin_time(self):
        await self.get_jackpot_award()
        await self.get_buy_back_morbin_time()
        await self.get_morbinTime()
        last_winner = secrets.get_last_winning_block()
        self.post_type = PostType.Empty

        if self.iTime_to_morb < time.time() and last_jackpot_award != self.last_jackpot_block:
            print("JACKPOT!")
            self.post_type = PostType.JackPot
            
            
        elif  self.jackpot_amount_dollar > self.morb_trigger and self.last_morbtime != last_morbtime_block:
            print("MORBIN TIME!")
            self.post_type = PostType.MorbinTime
            

        elif self.iTime_to_morb // 60 < time.time() // 60 + 10:
            self.post_type = PostType.WarningTime
        print("post_type: ", self.post_type)
        secrets.write_winning_block(self.last_morbtime,self.last_jackpot_block)
        self.loop.create_task(self.fetch_winning_blocks())

    async def fetch_winning_blocks(self):
        global last_jackpot_award, last_morbtime_block
        new_blocks = secrets.get_last_winning_block()
        last_jackpot_award = new_blocks[1]
        last_morbtime_block = new_blocks[0]

dBot = DiscordBot()

#print(', '.join("%s: %s" % item for item in attrs.items()))
dBot.run(credentials['DiscordAPIKey'])