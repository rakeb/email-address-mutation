import datetime
import hashlib
from email.mime.text import MIMEText

import mailparser

import fetch_mail as fm
import send_email
import custom_utility as cu

mod = 1


def do_mutate(last_mail_body):
    a = datetime.datetime.now()


    m = hashlib.sha256()
    m.update(last_mail_body.encode())

    # # TODO for only evaluation purpose
    # with open("/Users/mislam7/Dropbox/Adaptive_Conceal.pptx", "rb") as f:
    #     byte = f.read(1)
    #     while byte:
    #         # Do stuff with byte.
    #         m.update(byte)
    #         byte = f.read(1)

    hashed = m.digest()

    # log.debug('Hash generated: {}'.format(hashed))

    mutation_id = int.from_bytes(hashed, byteorder='big')
    mutation_id %= mod

    b = datetime.datetime.now()
    c = b - a

    with open('only_mutation_KB.txt', "a") as myfile:
        myfile.write(str(c.microseconds/1000))
        myfile.write('\n')
    return 1


def mutate_and_send(mail):
    mail_to = mail.to[0][1]
    mail_from = mail.from_[0][1]

    # mail_to = 'bob.email.mutation@gmail.com'
    # mail_from = 'alice.email.mutation@gmail.com'

    search_criteria = '(TO "' + mail_to + '")'
    mailbox = '"[Gmail]/Sent Mail"'

    # search_criteria = '(FROM "' + mail_from + '")'
    # mailbox = 'inbox'

    last_email = fm.fetch_mail(mail_from, 'emailmutation', search_criteria, mailbox)

    if last_email is None:
        excp_str = "Email not found using search criteria: {} in mailbox: {}".format(search_criteria, mailbox)
        raise FileNotFoundError(excp_str)

    last_mail_object = mailparser.parse_from_bytes(last_email)

    # print(mail_to)
    # print(mail_from)
    # last_mail_body = last_mail_object.body.split('--- mail_boundary ---')[0]
    last_mail_body = last_mail_object.body
    # print(last_mail_body)

    m_id = do_mutate(last_mail_body)

    splitted_from = mail_from.split('@')
    before_at = splitted_from[0]
    after_at = splitted_from[1]

    mutated_from = before_at + '.' + str(m_id) + '@' + after_at
    # print(mutated_from)

    msg = MIMEText(mail.body)
    msg['Subject'] = mail.subject
    msg['From'] = mutated_from
    msg['To'] = mail_to

    send_email.send_(mutated_from, 'emailmutation', [mail_to], msg.as_string())

    # # TODO fro only evaluation purpose
    # send_email.send_mail(mutated_from, mail_to, 'emailmutation', mail.subject, mail.body, [
    #     '/Users/mislam7/Dropbox/Adaptive_Conceal.pptx'])

    # print('done')


def validate_sender(from_address, to_address):
    real_email_address, before_at, mutation_id, domain = cu.get_real_email_address(from_address)

    # splitted_from = from_address.split('@')
    # before_at = splitted_from[0]
    # after_at = splitted_from[1]
    #
    # splitted_before_at = before_at.rsplit('.', 1)
    # mutation_id = splitted_before_at[1]
    # before_at = splitted_before_at[0]
    #
    # real_from_address = before_at + '@' + after_at

    search_criteria = '(FROM "' + before_at + '")'
    mailbox = 'inbox'

    last_email = fm.fetch_mail(to_address, 'emailmutation', search_criteria, mailbox)

    if last_email is None:
        return False, None

    last_mail_object = mailparser.parse_from_bytes(last_email)

    # print(mail_to)
    # print(mail_from)
    # last_mail_body = last_mail_object.body.split('--- mail_boundary ---')[0]
    last_mail_body = last_mail_object.body
    # print(last_mail_body)

    m_id = do_mutate(last_mail_body)

    if mutation_id == str(m_id):
        return True, real_email_address
    else:
        return False, None


if __name__ == '__main__':
    # mail = mailparser.parse_from_string('')
    # mutate_and_send(mail)
    validate_sender('rakeb.mazharul.1@gmail.com', 'alice.email.mutation@gmail.com')
