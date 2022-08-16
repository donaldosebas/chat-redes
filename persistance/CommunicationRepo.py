from aioconsole import ainput, aprint
import asyncio

class Communication:
    async def message_one_to_one_whom(self):
        await aprint('To who? ')
        to = await ainput()
        self.to = to

        return {
            'to_who': to,
        }
    async def message_one_to_one_message(self):
        await aprint('Enter message: ')
        message = await ainput()
        self.message = message

        return {
            'message': message,
        }

