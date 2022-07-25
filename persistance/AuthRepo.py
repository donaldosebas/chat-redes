class Auth:
    def login(self):
        print('Enter username: ')
        username = input()
        print('Enter password: ')
        password = input()
        self.username = username
        self.password = password

        return {
            'username': username,
            'password': password,
        }

    def register(self, username, password):
        print('register')
    
    def logout(self):
        print('logout')
    
    def delete_account(self):
        print('delete account')
