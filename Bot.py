import splinter, time
try:
    with splinter.Browser() as bot:
        try:
            bot.visit("https://www.fantomnameservice.com")
        except Exception as e:
            print(e)
        time.sleep(80)
except Exception as e:
    print(e)