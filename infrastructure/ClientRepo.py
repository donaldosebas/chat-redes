from urllib import response
import slixmpp
import xmpp
from persistance.AuthRepo import Auth
from persistance.CommunicationRepo import Communication
from persistance.HelpersRepo import Helper
from slixmpp.xmlstream.stanzabase import ET


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

        self.add_event_handler("session_start", self.start)
        self.add_event_handler('message', self.message)

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
            print('There has been an issue')
            self.disconnect()
            

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        print("Conectado exitosamente")
        login_start = True
        while login_start:
            self.helperRepo.get_login_options()
            opcion_submenu = int(input("Which option you want to take? "))

            if opcion_submenu == 1:
                self.send_one_to_one_message()
                await self.get_roster()
            elif opcion_submenu == 2:
                self.disconnect()
                login_start = False
            elif opcion_submenu == 3:
                await self.unregister()
                await self.get_roster()
                login_start = False
            else:
                print("Please select an option from the given menu")


    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            print(msg['body'])

    def send_one_to_one_message(self):
        message_info = self.communicationRepo.message_one_to_one()
        self.send_message(mto=message_info['to_who'],
                          mbody=message_info['message'],
                          mtype='chat')

        

# https://slixmpp.readthedocs.io/en/latest/using_asyncio.html?highlight=loop.run_forever()#running-the-event-loop
# https://stackoverflow.com/questions/56320676/xmpp-threaded-receiver-in-python-3