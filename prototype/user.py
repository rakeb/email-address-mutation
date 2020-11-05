import glob
import json
import logging as log
import os
import pickle
import socket
import sys
import threading
from pprint import pformat
import time

# log.getLogger().setLevel(log.INFO)
log.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d:%H:%M:%S',
                level=log.INFO)

HOST = '127.0.0.1'
PORT = None
client_socket = None
sender_email_address = None

MAIL = {}
REQ = {}
SMTP = 'smtp'
IMAP = 'imap'
My_name = ''


def close_james_socket():
    global s
    s.close()


def send_to_james(data):
    global s
    # print('Send to JAMES: {}'.format(data))
    try:
        s.sendall(data)
    except:
        print("James client closed")


def receiver():
    global client_socket
    log.info('Client ready to received from BOT')
    while True:
        try:
            r = client_socket.recv(1024)
            if not r:
                break
            res = pickle.loads(r)
            log.info('Received from server: ')
            log.info(pformat(res))
        except:
            log.error('Error occurred while receiving from server')


def create_mail():
    global sender_email_address
    log.info('Enter receiver email address: ')
    receiver_email_address = input()
    log.info('Enter email subject: ')
    subject = input()
    log.info('Enter email body: ')
    body = input()

    MAIL['sender'] = sender_email_address
    MAIL['receiver'] = receiver_email_address
    MAIL['subject'] = subject
    MAIL['body'] = body

    log.info('Mail created: {}'.format(MAIL))


def mail_send_handler():
    global sender_email_address
    global client_socket

    log.info("Sending mail")
    create_mail()
    # receiver_email_address = input('Enter receiver email address: ')
    # subject = input('Enter email subject: ')
    # body = input('Enter email body: ')
    #
    # MAIL['sender'] = sender_email_address
    # MAIL['receiver'] = receiver_email_address
    # MAIL['subject'] = subject
    # MAIL['body'] = body

    log.info('Sending mail: {}'.format(MAIL))
    REQ['protocol'] = SMTP
    REQ['mail'] = MAIL
    client_socket.send(pickle.dumps(REQ))


def mail_receiver_handler(is_check_mutation=True):
    log.info("Sending IMAP request...")
    REQ['protocol'] = IMAP
    REQ['check_mutation'] = is_check_mutation
    client_socket.send(pickle.dumps(REQ))


def get_latest_email_id(dir_name):
    list_of_files = glob.glob(dir_name + '/*')  # * means all if need specific format then *.csv
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
    except ValueError:
        return 0

    log.info('latest_file: {}'.format(latest_file))

    # user_name = sender_email_address.split('@')[0]
    f_name = latest_file.split(dir_name + '/')[1].split('.')[0]
    return int(f_name)


def update_inbox():
    receiver_email_address = MAIL['receiver']
    inbox_dir = receiver_email_address.split('@')[0] + '/inbox'

    id = get_latest_email_id(inbox_dir)
    id = id + 1
    log.info('Email ID: {}'.format(id))
    inbox_email_id = inbox_dir + '/' + str(id) + '.txt'
    with open(inbox_email_id, 'w') as file:
        file.write(json.dumps(MAIL))
        file.close()
    log.info("Inbox updated")


def update_sentbox():
    sent_dir_name = My_name + '/sent'

    id = get_latest_email_id(sent_dir_name)
    id = id + 1
    log.debug('Email ID: {}'.format(id))
    sent_email_id = sent_dir_name + '/' + str(id) + '.txt'
    with open(sent_email_id, 'w') as file:
        file.write(json.dumps(MAIL))
        file.close()
    log.info("Sent box updated")


def direct_send_mail():
    log.info("Direct send mail starts...")
    create_mail()
    # log.info("Press 1 to send email as attacker, press enter otherwise")
    # what = input()
    # if what != '1':
    update_sentbox()
    update_inbox()


def connect_bot():
    global client_socket

    # if client_socket is not None:
    #     return True

    host = HOST
    port = PORT  # The same port as used by the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        log.info("client started")
        return True
    except ConnectionRefusedError:
        log.info('Please start your bot at port: {} and press Enter or bypass using bot by pressing 1: '.format(PORT))
        bypass_bot = input()
        if bypass_bot == '1':
            return False
        else:
            return connect_bot()


def start_client():
    if connect_bot():
        threading.Thread(target=receiver, ).start()
        while True:
            log.info("Type 1 to send email:")
            log.info("Type 2 to receive email using mutation:\n")
            # log.info("Type 3 to receive email without using mutation: ")
            what = input()
            if what == '1':
                mail_send_handler()
            elif what == '2':
                mail_receiver_handler()
            elif what == '3':
                mail_receiver_handler(False)
            else:
                log.info("Invalid entry")
            time.sleep(.01)
    else:
        while True:
            direct_send_mail()
            time.sleep(.01)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log.info("Provide Email Address and PortNumber to run this script")
    else:
        sender_email_address = sys.argv[1]
        PORT = int(sys.argv[2])
        log.info('Email address: {} and Port Number: {}'.format(sender_email_address, PORT))
        try:
            My_name = sender_email_address.split('@')[0]
            domain_name = sender_email_address.split('@')[1]
            os.mkdir(My_name)
            os.mkdir(My_name + '/sent')
            os.mkdir(My_name + '/inbox')
            os.mkdir(My_name + '/trash')

        except IndexError:
            log.info("Not a valid Email address")
            exit(1)
        except OSError:
            log.info("User: %s login successful ", sender_email_address)
            # exit(1)
        start_client()
