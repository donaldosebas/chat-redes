#!/usr/bin/env python3

import logging
from argparse import ArgumentParser
from infrastructure.ClientRepo import Client

from persistance.HelpersRepo import Helper

"""
Administración de cuenta (25% del funcionamiento) 
    X Registrar una nueva cuenta en el servidor 
    X Iniciar sesión con una cuenta 
    X Cerrar sesión con una cuenta 
    X Eliminar la cuenta del servidor 
Comunicación (75% del funcionamiento) 
    X  Mostrar todos los usuarios/contactos y su estado 
    X Agregar un usuario a los contactos 
    X Mostrar detalles de contacto de un usuario 
    X Comunicación 1 a 1 con cualquier usuario/contacto 
    - Participar en conversaciones grupales 
    X Definir mensaje de presencia 
    X Enviar/recibir notificaciones 
    X Enviar/recibir archivos 
"""


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