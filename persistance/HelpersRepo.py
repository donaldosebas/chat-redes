from aioconsole import ainput, aprint
import asyncio

class Helper:
    def get_menu_options(self):
        print('Select an option')
        print('1. Login')
        print('2. Register')
        print('3. Close')

    async def get_login_options(self):
        await aprint("""
            Logged in menu

            1. Send one to one message
            2. Logout
            3. Delete account from server 
            4. Add contact
        """)
    