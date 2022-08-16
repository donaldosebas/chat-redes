from aioconsole import ainput, aprint
import asyncio

class Helper:
    async def get_menu_options(self):
        await aprint('Select an option')
        await aprint('1. Login')
        await aprint('2. Register')
        await aprint('3. Close')

    async def get_login_options(self):
        await aprint("""
            Logged in menu

            1. Send one to one message
            2. Logout
            3. Delete account from server 
        """)
    