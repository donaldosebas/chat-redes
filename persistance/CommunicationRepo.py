from aioconsole import ainput, aprint
import asyncio

class Communication:
    async def message_one_to_one(self):
        await aprint('To who? ')
        to = await ainput()
        await aprint('Enter message: ')
        message = await ainput()
        self.to = to
        self.message = message

        return {
            'to_who': to,
            'message': message,
        }

