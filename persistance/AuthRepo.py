from aioconsole import ainput, aprint
import asyncio
from getpass import getpass

class Auth:
    def login(self):
        print('Enter username: ')
        username = input()
        print('Enter password: ')
        password = getpass("Password: ")
        self.username = username
        self.password = password

        return {
            'username': username,
            'password': password,
        }

    def register(self):
        print('Enter username: ')
        username = input()
        print('Enter password: ')
        password = getpass("Password: ")
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
    
    async def get_user_info(self):
        await aprint('Enter user check: ')
        user = await ainput()
        self.user = user

        return {
            'user': user,
        }
    
    async def add_new_contact(self):
        await aprint('Enter contact to add: ')
        contact = await ainput()
        self.contact = contact

        return {
            'contact': contact,
        }
