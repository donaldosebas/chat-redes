from urllib import response
import slixmpp
import xmpp
from persistance.AuthRepo import Auth
from persistance.CommunicationRepo import Communication
from persistance.HelpersRepo import Helper
from slixmpp.xmlstream.stanzabase import ET
from aioconsole import ainput, aprint

exit = 'exit()'
recibir_de = ''
class Client(slixmpp.ClientXMPP):
    def __init__(self):
        self.authRepo = Auth()
        self.communicationRepo = Communication()
        self.helperRepo = Helper()

    def login(self):
        credentials = self.authRepo.login()
        slixmpp.ClientXMPP.__init__(self, credentials['username'], credentials['password'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0077')


        self.add_event_handler('message', self.message)
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
                recibir_de=message_info['to_who']
                option = 'init'
                while option != exit:
                    option = await self.send_one_to_one_message(message_info)
                    await self.get_roster()
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
                await self.getContacts()
                await self.get_roster()
            else:
                await aprint("Please select an option from the given menu")


    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            await aprint(recibir_de, 'RECIBIR AAAA')
            await aprint('\n',msg['from'], '>>', msg['body'])

    async def send_one_to_one_message(self, message_info):
        message = await self.communicationRepo.message_one_to_one_message()
        if message['message'] == exit:
            return exit
        self.send_message(mto=message_info['to_who'],
                          mbody=message['message'],
                          mtype='chat')

    async def addContact(self, newContact):
        self.send_presence_subscription(newContact)
        await aprint(newContact, 'Was added successfully to contacts')

    async def getContacts(self):
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

        

# https://slixmpp.readthedocs.io/en/latest/using_asyncio.html?highlight=loop.run_forever()#running-the-event-loop
# https://stackoverflow.com/questions/56320676/xmpp-threaded-receiver-in-python-3