import requests, secrets
credentials = secrets.get_credentials()
url = "https://api.telegram.org/"
class TelegramBot():
    def __init__(self):
        self.api_key = credentials["TelegramAPIKey"]
        self.chat_id = 0
        pass
    async def post(self, message):
        request = url + self.api_key + f"/sendMessage&chat_id={self.chat_id}&text={message}"
        result = requests.post(request).json
        print(result)
        pass
    async def getMe(self):
        request = url+self.api_key+f"/getMe"
        result = requests.get(request).json
        print(result)