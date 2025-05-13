from pyrogram import Client

API_ID = 123456  # Replace with your API ID
API_HASH = ""  # Replace with your API hash
SESSION_NAME = ""  # Name of the .session file that will be created

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

async def main():
    async with app:
        me = await app.get_me()
        print(f"? Logged in as: {me.first_name} [@{me.username}]")
        print(f"?? Session saved as: {SESSION_NAME}.session")

app.run(main())

