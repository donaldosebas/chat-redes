#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
import asyncio
from getpass import getpass
from argparse import ArgumentParser
from infrastructure.ClientRepo import Client

from persistance.HelpersRepo import Helper


helpers = Helper()
Client = Client()

if __name__ == '__main__':

    parser = ArgumentParser(description=Client.__doc__)
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')



    option = '0'
    
    while (option != '6'):
        helpers.get_menu_options()
        option = input()

        if (option == '1'):
            Client.login()

        if (option == '3'):
            Client.send_one_to_one_message()
