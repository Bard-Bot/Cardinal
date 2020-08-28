from bot import Cardinal
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = Cardinal()


extensions = [

]

for extension in extensions:
    bot.load_extension(extension)


try:
    bot.run(environ['BOT_TOKEN'])
except RuntimeError as e:
    # TODO: sentry_sdk
    pass
except Exception as e:
    pass
