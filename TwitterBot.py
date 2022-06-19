import asyncio
import splinter, secrets, random
credentials = secrets.get_credentials()
class TwitterBot():
    def __init__(self):
        pass
    async def login(self):
        self.browser.visit("https://twitter.com/login")
        self.browser.fill('name', credentials["TwitterUsername"])
        asyncio.sleep(self.sleep_time())
        self.browser.fill('password', credentials["TwitterPassword"])
        
    async def post(self):
        self.browser.visit("https://twitter.com")
        asyncio.sleep(self.sleep_time())
        self.browser.find_by_xpath("").click()
        self.browser.find_by_xpath("").fill(self.message)
        self.browser.find_by_xpath("").click()
    
    def sleep_time(self):
        return random.random() * 2 + 1

    async def handle_bot(self, message):
        with splinter.Browser as browser:
            self.browser = browser
            self.message = message
            await self.login()
            await self.post(message)