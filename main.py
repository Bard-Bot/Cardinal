from bot import Cardinal
from os import environ
from typing import List

bot = Cardinal()


extensions: List[str] = [

]

for extension in extensions:
    bot.load_extension(extension)


try:
    bot.run(environ['BOT_TOKEN'])
except RuntimeError:
    # TODO: sentry_sdk
    pass
except Exception:
    pass
