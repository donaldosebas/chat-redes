#!/usr/bin/env python3

import logging
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

        if (option == '2'):
            Client.register()
            print('Successfully registered')

        if (option == '3'):
            print('Thanks for using chatApp')