import logging
import socket
import ssl
import threading

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# HOST, PORT = 'exchange.iinet.net.au', 993
HOST, PORT = 'imap.gmail.com', 993


def loop_receive(conn):
    try:
        while True:
            r = conn.recv()
            logger.info("Gmail server response: {}".format(r.decode()))
            # conn.write(b'1 capability\r\n')
            # print(conn.recv().decode())
            # conn.write(b'2 authenticate PLAIN\r\n')
            # print(conn.recv().decode())
            # conn.write(b'AHJvYmVydEB0ZXN0LmNvbQBhZG1pbg==\r\n')
            # print(conn.recv().decode())
            # return r
    except Exception as e:
        print(e)


def loop_send(conn):
    try:
        while True:
            data = input()
            # data = data.encode() + b'\r\n'
            logger.info("Gmail server response: {}".format(data))
            conn.write(data)
    except Exception as e:
        print(e)


def handle(conn):
    # conn.write(b'GET / HTTP/1.1\n')
    #
    try:
        r = conn.recv()
        logger.info("Gmail server response: {}".format(r.decode()))
        # conn.write(b'1 capability\r\n')
        # print(conn.recv().decode())
        # conn.write(b'2 authenticate PLAIN\r\n')
        # print(conn.recv().decode())
        # conn.write(b'AHJvYmVydEB0ZXN0LmNvbQBhZG1pbg==\r\n')
        # print(conn.recv().decode())
        return r
    except Exception as e:
        print(e)


def send_to_gmail(conn, data):
    try:
        logger.info("Sending data to Gmail server: {}".format(data.decode()))
        conn.write(data)
        return receive_from_gmail(conn)
    except Exception as e:
        print(e)


def receive_from_gmail(conn):
    try:
        r = conn.recv()
        logger.info("Response from Gmail server : {}".format(r.decode()))
        return r
    except Exception as e:
        print(e)


def send_response_to_thinderbird(r, client_socket):
    # logger.info("Send response to ThunderBird: {}".format(r))
    logger.info("Gmail --> Thunderbird: {}".format(r))
    client_socket.send(r)


def receive_allways(conn=None):
    while True:
        try:
            # sock = socket.socket(socket.AF_INET)
            # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            # context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
            # conn = context.wrap_socket(sock, server_hostname=HOST)
            print(conn.recv().decode())
            # conn.write(b'GET / HTTP/1.1\n')
            # print(conn.recv().decode())
        except Exception as e:
            print(e)
            break


def send_always(conn):
    pass


def mod_handle(conn):
    threading.Thread(
        target=receive_allways,
        args=(conn,)
    ).start()

    threading.Thread(
        target=send_always,
        args=(conn,)
    ).start()


def main():
    sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
    conn = context.wrap_socket(sock, server_hostname=HOST)
    conn.connect((HOST, PORT))

    threading.Thread(
        target=loop_receive,
        args=(conn,)
    ).start()

    threading.Thread(
        target=loop_send,
        args=(conn,)
    ).start()

    # try:
    #     conn.connect((HOST, PORT))
    #     r = handle(conn)
    #     # mod_handle(conn)
    # finally:
    #     conn.close()


def first_connection_to_gmail(thunderbird_client_socket):
    sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
    conn = context.wrap_socket(sock, server_hostname=HOST)

    try:
        conn.connect((HOST, PORT))
        r = receive_from_gmail(conn)
        send_response_to_thinderbird(r, thunderbird_client_socket)
    finally:
        conn.close()


def send_to_gmail_then_receive(thunderbird_client_socket, data):
    sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
    conn = context.wrap_socket(sock, server_hostname=HOST)

    try:
        conn.connect((HOST, PORT))
        r = send_to_gmail(conn, data)
        send_response_to_thinderbird(r, thunderbird_client_socket)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
