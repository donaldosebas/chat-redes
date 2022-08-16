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
            5. Get contacts
            6. Set Presence
            7. Get user info
        """)
    async def get_presence_options(self):
        await aprint("""
            Presence options

            1. Available
            2. Away
            3. Not Available
            4. Bussy
        """)
    