from pyrogram import Client
from pyrogram.types import ChatPrivileges
from pyrogram.enums import ChatMembersFilter  # ✅ FIXED filter bug
import asyncio

API_ID = 123456  # your API ID from https://my.telegram.org
API_HASH = ""
SESSION_NAME = ""

CHANNEL_A_TITLE = ""
CHANNEL_B_TITLE = ""  # The channel where you want to add the bots
DELAY_SECONDS = 5  # delay between each promotion

async def main():
    async with Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH) as app:
        # Search for Channel A
        chat_a = await find_chat_by_title(app, CHANNEL_A_TITLE)
        chat_b = await find_chat_by_title(app, CHANNEL_B_TITLE)

        if not chat_a or not chat_b:
            print("❌ Could not find one or both channels.")
            return

        # Get list of bot admins in Channel A
        admins_a = []
        async for member in app.get_chat_members(chat_a.id, filter=ChatMembersFilter.ADMINISTRATORS):  # ✅ FIXED
            if member.user.is_bot:
                admins_a.append(member.user)

        print(f"👥 Found {len(admins_a)} bot admins in '{CHANNEL_A_TITLE}'.")

        # Promote each bot in Channel B
        for bot in admins_a:
            try:
                existing = await app.get_chat_member(chat_b.id, bot.id)
                if existing.status == "administrator":
                    print(f"✅ @{bot.username or bot.id} is already an admin in '{CHANNEL_B_TITLE}'")
                    continue
            except:
                pass  # bot might not be in the channel yet

            try:
                await app.promote_chat_member(
                    chat_id=chat_b.id,
                    user_id=bot.id,
                    privileges=ChatPrivileges(
                        can_change_info=True,
                        can_post_messages=True,
                        can_edit_messages=True,
                        can_delete_messages=True,
                        can_invite_users=True,
                        can_restrict_members=False,
                        can_pin_messages=True,
                        can_promote_members=True,
                        can_manage_video_chats=True,
                        can_manage_chat=True
                    )
                )
                print(f"✅ Promoted @{bot.username or bot.id} to admin in '{CHANNEL_B_TITLE}'")
            except Exception as e:
                print(f"❌ Failed to promote {bot.username or bot.id}: {e}")

            await asyncio.sleep(DELAY_SECONDS)

async def find_chat_by_title(app, title):
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        if chat.title == title:
            return chat
    return None

if __name__ == "__main__":
    asyncio.run(main())
