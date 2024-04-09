from pyrogram import Client
from os import environ as env
api_id = env.get('API_ID')
api_hash = env.get('API_HASH')
bot_token = env.get('BOT_TOKEN')

bot = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    bot.run()
