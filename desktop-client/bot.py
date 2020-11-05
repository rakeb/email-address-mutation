import logging
import queue
import socket
import threading
import traceback

import gmail_client as GC
import smtp_server
from custom_log import logger

HOST = '127.0.0.1'
PORT = 1143
first_time = True

bind_ip = HOST
bind_port = PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

logger.info("IMAP Server Started: {}: {}".format(bind_ip, bind_port))


def handle_thunderbird_client_connection(thunderbird_client_socket, gmail_client):
    try:
        while True:
            response = thunderbird_client_socket.recv(1024)
            if not response:
                break;
            else:
                gmail_client.send_to_gmail(response)
    except Exception as e:
        logger.error("Thunderbird client closed with exception: {}".format(e))
        traceback.print_exc()


if __name__ == '__main__':
    try:
        flag_queue = queue.Queue()
        smtp_handler = threading.Thread(target=smtp_server.run,)
        smtp_handler.setDaemon(True)
        smtp_handler.start()
        logger.info('ready for mail client')
        while True:
            thunderbird_client_socket, address = server.accept()
            logging.info("Accepted connection from {}:{}".format(address[0], address[1]))

            gmail_client = GC.GmailClient(thunderbird_client_socket, flag_queue)

            client_handler = threading.Thread(
                target=handle_thunderbird_client_connection,
                # without comma you'd get a... TypeError:
                # handle_client_connection() argument after
                # * must be a sequence, not _socketobject
                args=(thunderbird_client_socket, gmail_client,)
            )
            client_handler.setDaemon(True)
            client_handler.start()
    except KeyboardInterrupt as e:
        logging.warn("Closing bot socket...")
        server.close()
        traceback.print_exc()
