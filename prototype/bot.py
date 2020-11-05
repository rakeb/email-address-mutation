import glob
import hashlib
import json
import logging as log
import os
import pickle
import socket
import sys
import threading

# log.getLogger().setLevel(log.INFO)
log.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d:%H:%M:%S',
                level=log.INFO)

HOST = '127.0.0.1'
PORT = None
server = None
client_socket = None
MUTATION_EMAIL_COUNT = 2
MOD = 1000
MAIL = {}
RES = {}
SMTP = 'smtp'
My_name = ''
Domain_name = ''

vip_list = {}

with open('vip_list.json') as f:
    vip_list = json.load(f)
    f.close()
log.info('VIP list: {}'.format(vip_list))


def send_to_client(message, response_code):
    global client_socket

    RES['message'] = message
    RES['response_code'] = response_code

    log.info('Sending response to client: {}'.format(RES))
    client_socket.send(pickle.dumps(RES))


def get_latest_email_id(dir_name):
    list_of_files = glob.glob(dir_name + '/*')  # * means all if need specific format then *.csv
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
    except ValueError:
        return 0

    log.debug('Latest email: {}'.format(latest_file))

    f_name = latest_file.split(dir_name + '/')[1].split('.')[0]
    return int(f_name)


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


def read_email(email_file_name):
    with open(email_file_name) as f:
        email_json = json.load(f)
        f.close()
    log.info('Email from inbox: {}'.format(email_json))
    return email_json


def check_shadow_real_equality(first_address, last_address):
    if first_address == last_address:
        return True
    # f_name = first_address.split('@')[0]
    # f_domain = first_address.split('@')[1]
    # l_name = last_address.split('@')[0]
    # l_domain = last_address.split('@')[1]
    #
    # if f_domain == l_domain:
    #     if f_name in l_name or l_name in f_name:
    #         return True
    if last_address in first_address:
        return True
    return False


def get_hash_from_history_emails(m_type, match_address):
    if m_type == 'outgoing':
        last_nth_email = MUTATION_EMAIL_COUNT - 1
        hash_message = MAIL['body']
        dir_name = My_name + '/sent'
        matcher = 'receiver'
    else:
        last_nth_email = MUTATION_EMAIL_COUNT
        hash_message = ''
        dir_name = My_name + '/inbox'
        matcher = 'sender'

    list_of_files = glob.glob(dir_name + '/*')
    list_of_files.sort(key=os.path.getmtime, reverse=True)

    log.info('List of emails: {}'.format(list_of_files))
    log.info('Mutation Type: {}, matching with {}'.format(m_type, match_address))
    counter = 0
    hash_emails = {}
    for email_file in list_of_files:
        email_from_inbox = read_email(email_file)
        # if email_from_inbox['sender'] == MAIL['sender'] and email_from_inbox['receiver'] == MAIL['receiver']:
        if check_shadow_real_equality(email_from_inbox[matcher], match_address):
            # hash_message += json.dumps(email_from_inbox)
            hash_emails['email_id'] = email_file
            hash_emails['email'] = email_from_inbox
            hash_message += email_from_inbox['body']
            counter += 1
            if counter >= last_nth_email:
                break

    log.info('Hash Emails: {}'.format(hash_emails))
    return json.dumps(hash_message)


def generate_hash(m_type, match_address):
    return get_hash_from_history_emails(m_type, match_address)


def do_mutation(m_type, match_address):
    hash_message = generate_hash(m_type, match_address)

    log.info('Final Hash Message: {}'.format(hash_message))

    m = hashlib.sha256()
    m.update(hash_message.encode())

    hashed = m.digest()

    log.debug('Hash generated: {}'.format(hashed))

    mutation_id = int.from_bytes(hashed, byteorder='big')
    mutation_id %= MOD
    log.info('Mutation ID generated: {}'.format(mutation_id))

    if m_type == 'incoming':
        return mutation_id

    user_name = My_name
    user_name += '_' + str(mutation_id)
    sender_address = user_name + '@' + Domain_name
    MAIL['sender'] = sender_address
    log.debug('Mutated email: {}'.format(MAIL))
    log.info('Mutated sender address: {}'.format(MAIL['sender']))


def update_inbox():
    # _MAIL = {"sender": "rakeb@gmail.com", "receiver": "rakeb@aasdad", "subject": "test",
    #          "body": "lets test mutation first"}
    receiver_email_address = MAIL['receiver']

    inbox_dir = receiver_email_address.split('@')[0] + '/inbox'

    id = get_latest_email_id(inbox_dir)
    id = id + 1
    log.debug('Email ID: {}'.format(id))
    inbox_email_id = inbox_dir + '/' + str(id) + '.txt'
    with open(inbox_email_id, 'w') as file:
        file.write(json.dumps(MAIL))
        file.close()
    log.info("Inbox updated")


def handle_received_mail():
    receiver_email_address = MAIL['receiver']
    receiver_user_name = receiver_email_address.split('@')[0]

    if not os.path.isdir(receiver_user_name):
        log.info('Receiver not found: {}'.format(receiver_email_address))
        send_to_client("Receiver not found: " + receiver_email_address, "bounce")
    else:
        do_mutation('outgoing', receiver_email_address)
        update_inbox()
        update_sentbox()
        send_to_client('Email successfully sent to recipient', 'OK')


def check_sender_id(sender_address, m_id):
    if str(m_id) not in sender_address:
        return False
    if str(m_id) == sender_address.split('@')[0].rsplit('_', 1)[1]:
        return True
    return False


def response_imap_req(response):
    dir_name = My_name + '/inbox'
    list_of_files = glob.glob(dir_name + '/*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_email = read_email(latest_file)
    sender_address = latest_email['sender']

    if not response['check_mutation']:
        send_to_client(latest_email, 'OK')
        return

    possible_sender = ''
    if sender_address in vip_list:
        possible_sender = sender_address.split('@')[0]
    # else:
    #     for key, value in vip_list.items():
    #         if sender_address in value:
    #             possible_sender = key.split('@')[0]
    if possible_sender == '':
        if '_' in sender_address:
            # domain = sender_address.split('@')[1]
            # user = sender_address.rsplit('_', 1)[0]
            # possible_sender = user + '@' + domain
            possible_sender = sender_address.rsplit('_', 1)[0]

    if possible_sender == '':
        send_to_client(latest_email, 'OK')
        return
    else:
        log.info('Search if emails received from : {}'.format(possible_sender))
        m_id = do_mutation('incoming', possible_sender)
        if check_sender_id(sender_address, m_id):
            status = 'OK'
            latest_email['sender'] = sender_address.replace('_' + str(m_id), '')
        else:
            status = 'THREAT'
            trashed_file = latest_file.replace('inbox', 'trash')
            os.rename(latest_file, trashed_file)
            log.info('Threat email moved to Trash')
        send_to_client(latest_email, status)


def handle_client_connection():
    global client_socket
    global MAIL
    while True:
        response = client_socket.recv(1024)
        if not response:
            break;
        response = pickle.loads(response)
        log.info('Received from client: {}'.format(response))

        if response['protocol'] == SMTP:
            MAIL = response['mail']
            handle_received_mail()
        else:
            response_imap_req(response)


def start_server():
    global server
    bind_ip = HOST
    bind_port = PORT

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    log.info('Server started at {} port {}'.format(HOST, PORT))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log.info("Provide Email Address and PortNumber to run bot")
    else:
        sender_email_address = sys.argv[1]
        PORT = int(sys.argv[2])
        log.info('Email address: {} and Port Number: {}'.format(sender_email_address, PORT))
        try:
            My_name = sender_email_address.split('@')[0]
            Domain_name = sender_email_address.split('@')[1]
        except IndexError:
            log.info("Not a valid Email address")
            exit(1)

        start_server()

        try:
            while True:
                client_socket, address = server.accept()
                log.info('Accepted connection from {}:{}'.format(address[0], address[1]))
                client_handler = threading.Thread(
                    target=handle_client_connection,
                )
                client_handler.start()
        except:
            server.close()
