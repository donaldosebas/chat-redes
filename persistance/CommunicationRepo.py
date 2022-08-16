from aioconsole import ainput
import asyncio

class Communication:
    def __init__(self):
        self.messages = {}
    
    def receive_message(self, user, message):
        try:
            self.messages[user].append({
                'user': user,
                'message': message,
            })

        except:
            self.messages[user] = [{
                'user': user,
                'message': message,
            }]
    def send_message(self, user_to, message):
        try:
            self.messages[user_to].append({
                'user': 'me',
                'message': message,
            })

        except:
            self.messages[user_to] = [{
                'user': 'me',
                'message': message,
            }]

    async def message_one_to_one_whom(self):
        to = await ainput('To who? ')
        self.to = to

        return {
            'to_who': to,
        }
    async def message_one_to_one_message(self):
        message = await ainput('>> ')
        self.message = message

        return {
            'message': message,
        }

