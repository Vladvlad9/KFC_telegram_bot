import os
from dotenv import load_dotenv

load_dotenv(".env")
BOT_TOKEN = os.environ["BOT_TOKEN"]
DATABASE = os.environ["DATABASE"]

admins = [
	381252111,
]
