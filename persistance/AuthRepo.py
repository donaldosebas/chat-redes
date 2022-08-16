from aioconsole import ainput, aprint
import asyncio

class Auth:
    async def login(self):
        await aprint('Enter username: ')
        username = await ainput()
        await aprint('Enter password: ')
        password = await ainput()
        self.username = username
        self.password = password

        return {
            'username': username,
            'password': password,
        }

    async def register(self):
        await aprint('Enter username: ')
        username = await ainput()
        await aprint('Enter password: ')
        password = await ainput()
        self.username = username
        self.password = password

        return {
            'username': username,
            'password': password,
        }
    
    def logout(self):
        print('logout')
    
    def delete_account(self):
        print('delete account')
