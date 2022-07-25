class Communication:
    def message_one_to_one(self):
        print('To who? ')
        to = input()
        print('Enter message: ')
        message = input()
        self.to = to
        self.message = message

        return {
            'to_who': to,
            'message': message,
        }

