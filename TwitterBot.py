import asyncio
from selenium.webdriver.common import keys
import splinter, secrets, random
credentials = secrets.get_credentials()
class TwitterBot():
    def __init__(self):
        pass
    async def login(self):
        try:
            self.browser.visit("https://twitter.com/i/flow/login")
            await asyncio.sleep(self.sleep_time() * 3)
            self.browser.find_by_name("text").fill(credentials["TwitterUserName"])
            #self.browser#$.send_keys(keys.Keys.ENTER)
            await asyncio.sleep(self.sleep_time())
            self.browser.find_by_xpath("//div[@role='button']")[2].click()
            await asyncio.sleep(self.sleep_time())
            #self.browser.find_by_name("")
            self.browser.fill('password', credentials["TwitterPassword"])
            await asyncio.sleep(self.sleep_time())
            self.browser.find_by_xpath("//div[@data-testid='LoginForm_Login_Button']").click()
            await asyncio.sleep(self.sleep_time())
        except Exception as e:
            print(str(e))
        
    async def post(self):
        try:
            self.browser.visit("https://twitter.com")
            await asyncio.sleep(self.sleep_time())
            self.browser.find_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()
            await asyncio.sleep(self.sleep_time())
            self.browser.find_by_xpath("//div[@role='textbox']").fill(self.message)
            await asyncio.sleep(self.sleep_time())
            self.browser.find_by_xpath("//div[@data-testid='tweetButton']").click()
            await asyncio.sleep(self.sleep_time())
        except Exception as e:
            print(e)
    def sleep_time(self):
        return random.random() * 2 + 1

    async def handle_bot(self, message):
        with splinter.Browser() as browser:
            self.browser = browser
            self.message = message
            await self.login()
            await self.post()