import slixmpp

from persistance.AuthRepo import Auth
from persistance.CommunicationRepo import Communication


class Client(slixmpp.ClientXMPP):
    def __init__(self):
        self.authRepo = Auth()
        self.communicationRepo = Communication()

    def login(self):
        credentials = self.authRepo.login()
        slixmpp.ClientXMPP.__init__(self, credentials['username'], credentials['password'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping

        self.add_event_handler("session_start", self.start)
        self.add_event_handler('message', self.message)

        self.connect(disable_starttls=True)


    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            self.send_message(mto=msg['from'],
            mbody='Thanks for sending:\n%s' % msg['body'])

    def send_one_to_one_message(self):
        message_info = self.communicationRepo.message_one_to_one()
        self.send_message(mto=message_info['to_who'],
                          mbody=message_info['message'],
                          mtype='chat')
        self.process()
# https://slixmpp.readthedocs.io/en/latest/using_asyncio.html?highlight=loop.run_forever()#running-the-event-loop
# https://stackoverflow.com/questions/56320676/xmpp-threaded-receiver-in-python-3