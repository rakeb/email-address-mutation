import glob
import json
import logging as log
import os
import sys
import time

# log.getLogger().setLevel(log.INFO)
log.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d:%H:%M:%S',
                level=log.INFO)

sender_email_address = None

MAIL = {}


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


def direct_send_mail():
    log.info("Attack email sending starts...")
    create_mail()
    update_inbox()


def start_client():
    while True:
        direct_send_mail()
        time.sleep(.01)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        log.info("Provide Email Address to run this script")
    else:
        sender_email_address = sys.argv[1]
        log.info('Email address: {}'.format(sender_email_address))
        start_client()
