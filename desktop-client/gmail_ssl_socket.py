import socket
import ssl
import threading


def receive_and_send(gmail_client_socket):
    while True:
        try:
            r = gmail_client_socket.recv(1024)
            print(r)
            str_response = r.decode()
            # list_response.append(str_response)
            print(str_response)
        except Exception as e:
            # print(e)
            pass


def _start():
    hostname = 'imap.gmail.com'
    port = 993
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())

            threading.Thread(
                target=receive_and_send,
                args=(ssock,)
            ).start()


if __name__ == '__main__':
    _start()
