import logging
import socket
import threading

import ssl_test

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

HOST = '127.0.0.1'
PORT = 1143
first_time = True

bind_ip = HOST
bind_port = PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

logging.info("Listening on: {}: {}".format(bind_ip, bind_port))


def handle_thunderbird_client_connection(thunderbird_client_socket):
    while True:
        response = thunderbird_client_socket.recv(1024)
        logging.info("Thunderbird --> Gmail: {}".format(response))
        if not response:
            break;
        else:
            ssl_test.send_to_gmail_then_receive(thunderbird_client_socket, response)


if __name__ == '__main__':
    try:
        while True:
            thunderbird_client_socket, address = server.accept()
            # print('Accepted connection from {}:{}'.format(address[0], address[1]))
            logging.info("Accepted connection from {}:{}".format(address[0], address[1]))

            ssl_test.first_connection_to_gmail(thunderbird_client_socket)

            client_handler = threading.Thread(
                target=handle_thunderbird_client_connection,
                args=(thunderbird_client_socket,)
                # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
            )
            client_handler.start()
    except:
        logging.info("Closing bot socket...")
        server.close()
