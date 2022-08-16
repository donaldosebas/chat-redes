from urllib import response
import slixmpp
import xmpp
from persistance.AuthRepo import Auth
from persistance.CommunicationRepo import Communication
from persistance.HelpersRepo import Helper
from slixmpp.xmlstream.stanzabase import ET
from aioconsole import ainput, aprint

exit = 'exit()'
class Client(slixmpp.ClientXMPP):
    def __init__(self):
        self.authRepo = Auth()
        self.communicationRepo = Communication()
        self.helperRepo = Helper()
        self.recibir_de = ''

    def login(self):
        credentials = self.authRepo.login()
        slixmpp.ClientXMPP.__init__(self, credentials['username'], credentials['password'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0077') # Unregister account
        self.register_plugin('xep_0045') # Group chat
        self.register_plugin('xep_0085')  # Chat State Notifications

        self.add_event_handler('chatstate_gone', self.contactGone)
        self.add_event_handler('chatstate_active', self.contactActive)
        self.add_event_handler('chatstate_inactive', self.contactInactive)
        self.add_event_handler('chatstate_paused', self.contactPause)
        self.add_event_handler('chatstate_composing', self.contactTyping)
        self.add_event_handler("message", self.message)
        self.add_event_handler('groupchat_message', self.message_group)
        self.add_event_handler("session_start", self.start)

        self.connect(disable_starttls=True)
        self.process(forever=False)
    
    def register(self):
        credentials = self.authRepo.register()
        jid = xmpp.JID(credentials['username'])
        client = xmpp.Client(jid.getDomain(), debug=[])
        client.connect()
        return xmpp.features.register(client, jid.getDomain(), {
            'username': jid.getNode(),
            'password': credentials['password']
        })
    
    async def unregister(self):
        query = self.Iq()
        query['type'] = 'set'
        query['from'] = self.boundjid.user
        query['register']['remove'] = True

        try:
            await query.send()
            self.disconnect()
        except:
            await aprint('There has been an issue')
            self.disconnect()
            

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await aprint("Conectado exitosamente")
        login_start = True
        while login_start:
            await self.helperRepo.get_login_options()
            opcion_submenu = await ainput("Which option you want to take? ")
            if opcion_submenu == '1':
                await aprint("For exiting do exit()")
                message_info = await self.communicationRepo.message_one_to_one_whom()
                self.recibir_de=message_info['to_who']
                if message_info['to_who'] in self.communicationRepo.messages:
                    for i in self.communicationRepo.messages[message_info['to_who']]:
                        if i['user'] == 'me':
                            await aprint('>>', i['message'])
                        else:
                            await aprint(i['user'], '>>', i['message'])
                option = 'init'
                while option != exit:
                    option = await self.send_one_to_one_message(message_info)
                    await self.get_roster()
                self.recibir_de = ''
            elif opcion_submenu == '2':
                self.disconnect()
                login_start = False
            elif opcion_submenu == '3':
                await self.unregister()
                await self.get_roster()
                login_start = False
            elif opcion_submenu == '4':
                contact = await self.authRepo.add_new_contact()
                await self.addContact(contact['contact'])
                await self.get_roster()
            elif opcion_submenu == '5':
                await self.get_contacts()
                await self.get_roster()
            elif opcion_submenu == '6':
                await self.setPresence()
                await self.get_roster()
            elif opcion_submenu == '7':
                user = await self.authRepo.get_user_info()
                await self.get_user(user['user'])
            elif opcion_submenu == '8':
                await aprint("For exiting do exit()")
                room = await self.join_group()
                self.recibir_de=room
                await self.get_roster()
                await aprint(f'Group chat ---------- {room}')
                if room in self.communicationRepo.messages:
                    for i in self.communicationRepo.messages[room]:
                        if i['user'] == 'me':
                            await aprint('>>', i['message'])
                        else:
                            await aprint(i['user'], '>>', i['message'])
                option = 'init'
                while option != exit:
                    option = await self.send_group_message(room)
                    await self.get_roster()
                self.recibir_de = ''

            else:
                await aprint("Please select an option from the given menu")


    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            message_from = str(msg['from']).split('/')[0]
            if message_from == self.recibir_de:
                await aprint('\n',message_from, '>>', msg['body'])
            else:
                await aprint('\n', '[NOTIFICACION]', message_from)
            self.communicationRepo.receive_message(message_from, msg['body'])


    async def message_group(self, msg):
        if msg['type'] in ('groupchat') and msg['body'] != 'message':
            message_from = str(msg['from']).split('/')
            if message_from[0] == self.recibir_de:
                await aprint('\n',message_from[1], '>>', msg['body'])
            else:
                await aprint('\n', '[NOTIFICACION]', 'Grupo: ', message_from[0], ' De: ', message_from[1])
            self.communicationRepo.receive_message_group(message_from[0], message_from[1], msg['body'])

    async def send_one_to_one_message(self, message_info):
        message = await self.communicationRepo.message_one_to_one_message()
        if message['message'] == exit:
            return exit
        self.send_message(mto=message_info['to_who'],
                          mbody=message['message'],
                          mtype='chat')
        self.communicationRepo.send_message(message_info['to_who'], message['message'])

    async def addContact(self, newContact):
        self.send_presence_subscription(newContact)
        await aprint(newContact, 'Was added successfully to contacts')

    async def get_contacts(self):
        roster = self.client_roster.groups()
        self.contacts = []

        for group in roster:
            for user in roster[group]:
                self.client_roster[user]['subscription']
                conexions = self.client_roster.presence(user)
                if not conexions:
                    status = 'offline'
                else:
                    for _, obj in conexions.items():
                        if obj['status'] == '':
                            status = 'online'
                        else:
                            status = obj['status']
                
                self.contacts.append([
                user,
                status
                ])
                status = ''
        await aprint('User->Status')
        for contact in self.contacts:
            await aprint(f'{contact[0]}->{contact[1]}')

    async def setPresence(self):
        options = ['chat', 'away', 'xa', 'dnd']
        await self.helperRepo.get_presence_options()
        option = await ainput('==> ')
        presence_value = options[int(option) - 1]
        status = await ainput('Enter status: ')
        self.send_presence(pshow=presence_value, pstatus=status)
        await self.get_roster()
    
    async def get_user(self, contact):
        try:
            roster = list(self.client_roster.presence(contact).items())[0][1]
            status_dict = {'': 'Available' , 'away': 'Away', 'xa': 'Not available', 'dnd': 'Busy'}
            status = roster['status']
            presence = status_dict[roster['show']]
            await aprint(f"""
                Info for {contact}
                STATUS: {status}
                PRESENCE: {presence}
            """)
        except:
            await aprint(f'{contact} is Offline')


    async def join_group(self):
        room = await ainput("Write the group name: ")
        nickname = await ainput("write your nickname: ")
        self.plugin['xep_0045'].join_muc(room+"@conference.alumchat.fun", nickname)
        return room+"@conference.alumchat.fun"
    
    async def send_group_message(self, room):
        message = await self.communicationRepo.message_one_to_one_message()
        if message['message'] == exit:
            return exit
        self.send_message(mto=room, mbody=message, mtype='groupchat')
        self.communicationRepo.send_message(room, message['message'])

    async def contactGone(self, event):
        msg_from = str(event['from'])
        if (self.recibir_de in msg_from):
            await aprint(f'[NOTIFICACION] {msg_from} y se marchó... y a su barco le llamó libertad...')

    async def contactInactive(self, event):
        msg_from = str(event['from'])
        if (self.recibir_de in msg_from):
            await aprint(f'[NOTIFICACION] {msg_from} is inactive')

    async def contactActive(self, event):
        msg_from = str(event['from'])
        if (self.recibir_de in msg_from):
            await aprint(f'[NOTIFICACION] {msg_from} is active')

    async def contactPause(self, event):
        msg_from = str(event['from'])
        if (self.recibir_de in msg_from):
            await aprint(f'[NOTIFICACION] {msg_from} stopped writing...')

    async def contactTyping(self, event):
        msg_from = str(event['from'])
        if (self.recibir_de in msg_from):
            await aprint(f'[NOTIFICACION] {msg_from} is writing...')

