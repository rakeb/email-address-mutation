import datetime
import hashlib
import logging
import random

from django.core.exceptions import ObjectDoesNotExist

from emailmutation.email_sender import sender
from emailmutation.models import HashedEmailTable, MutationParam

logger = logging.getLogger('mutation.py')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

mod = 1


def fetch_user_mutation_param(email_sender):
    mutation_param = MutationParam.objects.filter(email_address=email_sender).latest('email_address')
    return mutation_param


def get_mID(last_n_email_hash):
    # random.seed()
    # index = random.randint(0, mod)
    # mId = last_n_email_hash[index]

    # mutation_id = int.from_bytes(hashed_value, byteorder='big')
    # mutation_id = int(hashed_value)
    # mutation_id %= mod

    return last_n_email_hash[1]


# def do_mutate(last_mail_body):
#     a = datetime.datetime.now()
#
#     m = hashlib.sha256()
#     m.update(last_mail_body.encode())
#
#     # # TODO for only evaluation purpose
#     # with open("/Users/mislam7/Dropbox/Adaptive_Conceal.pptx", "rb") as f:
#     #     byte = f.read(1)
#     #     while byte:
#     #         # Do stuff with byte.
#     #         m.update(byte)
#     #         byte = f.read(1)
#
#     hashed = m.digest()
#
#     # log.debug('Hash generated: {}'.format(hashed))
#
#     mutation_id = int.from_bytes(hashed, byteorder='big')
#     mutation_id %= mod
#
#     b = datetime.datetime.now()
#     c = b - a
#
#     with open('only_mutation_KB.txt', "a") as myfile:
#         myfile.write(str(c.microseconds / 1000))
#         myfile.write('\n')
#     return 1


# def mutate_and_send(mail_to, mail_from):
#     # mail_to = 'bob.email.mutation@gmail.com'
#     # mail_from = 'alice.email.mutation@gmail.com'
#
#     search_criteria = '(TO "' + mail_to + '")'
#     mailbox = '"[Gmail]/Sent Mail"'
#
#     # search_criteria = '(FROM "' + mail_from + '")'
#     # mailbox = 'inbox'
#
#     last_email = fm.fetch_mail(mail_from, 'emailmutation', search_criteria, mailbox)
#
#     if last_email is None:
#         excp_str = "Email not found using search criteria: {} in mailbox: {}".format(search_criteria, mailbox)
#         raise FileNotFoundError(excp_str)
#
#     last_mail_object = mailparser.parse_from_bytes(last_email)
#
#     # print(mail_to)
#     # print(mail_from)
#     # last_mail_body = last_mail_object.body.split('--- mail_boundary ---')[0]
#     last_mail_body = last_mail_object.body
#     # print(last_mail_body)
#
#     m_id = do_mutate(last_mail_body)
#
#     splitted_from = mail_from.split('@')
#     before_at = splitted_from[0]
#     after_at = splitted_from[1]
#
#     mutated_from = before_at + '.' + str(m_id) + '@' + after_at
#     # print(mutated_from)
#
#     msg = MIMEText(mail.body)
#     msg['Subject'] = mail.subject
#     msg['From'] = mutated_from
#     msg['To'] = mail_to
#
#     send_email.send_(mutated_from, 'emailmutation', [mail_to], msg.as_string())
#
#     # # TODO fro only evaluation purpose
#     # send_email.send_mail(mutated_from, mail_to, 'emailmutation', mail.subject, mail.body, [
#     #     '/Users/mislam7/Dropbox/Adaptive_Conceal.pptx'])
#
#     # print('done')


def get_shadow_address(email_sender, mID):
    splitted_from = email_sender.split('@')
    before_at = splitted_from[0]
    after_at = splitted_from[1]

    shadow_address = before_at + '.' + str(mID) + '@' + after_at
    return shadow_address


def get_shadow(mID, shadow_list):
    credential = shadow_list[mID]
    email_address = credential['email_address']
    password = credential['password']
    return email_address, password


def get_ground_truth(sender, recipient):
    from_email = sender
    to_email = recipient

    try:
        hashed_email_table_obj = HashedEmailTable.objects.filter(from_address=from_email, to_address=to_email).latest(
            'id')
        logger.debug(
            "Hashed List found in DB, from: {}, to: {}, hashed list: {}".format(from_email, to_email,
                                                                                hashed_email_table_obj.last_n_email_hash))
    except ObjectDoesNotExist:
        from_email = recipient
        to_email = sender
        try:
            hashed_email_table_obj = HashedEmailTable.objects.filter(from_address=from_email,
                                                                     to_address=to_email).latest('id')
            logger.debug(
                "Hashed List found in DB, from: {}, to: {}, hashed list: {}".format(from_email, to_email,
                                                                                    hashed_email_table_obj.last_n_email_hash))
        except ObjectDoesNotExist:
            from_email = sender
            to_email = recipient
            # TODO need to re think about last_n_email_hash
            last_n_email_hash = [0, 0]
            mID = 0
            hashed_email_table_obj = HashedEmailTable(from_address=from_email, to_address=to_email,
                                                      last_n_email_hash=last_n_email_hash, mID=mID)
            hashed_email_table_obj.save()
            logger.debug(
                "Hashed List not found in DB. Saving to DB from: {}, to: {}, hashed list: {}".format(from_email,
                                                                                                     to_email,
                                                                                                     last_n_email_hash))
    return hashed_email_table_obj.last_n_email_hash, (from_email, to_email), hashed_email_table_obj.mID


# def update_hashed_list(data, from_to_pair, hashed_list):
#     from_email = from_to_pair[0]
#     to_email = from_to_pair[1]
#
#     m = hashlib.sha256()
#     m.update(data.encode())
#
#     # # TODO for only evaluation purpose
#     # with open("/Users/mislam7/Dropbox/Adaptive_Conceal.pptx", "rb") as f:
#     #     byte = f.read(1)
#     #     while byte:
#     #         # Do stuff with byte.
#     #         m.update(byte)
#     #         byte = f.read(1)
#
#     hashed = m.digest()
#
#     mutation_id = int.from_bytes(hashed, byteorder='big')
#     mutation_id %= mod
#
#     hashed_list = hashed_list[1:]
#     hashed_list.append(mutation_id)
#     HashedEmailTable.objects.filter(from_address=from_email, to_address=to_email).update(last_n_email_hash=hashed_list)


def process_email_for_mutation(mail_object):
    email_sender = mail_object['email_sender']['emailAddress']
    email_recipient = mail_object['email_recipient'][0]['emailAddress']
    email_subject = mail_object['email_subject']
    email_body = mail_object['email_body']

    # a = datetime.datetime.now()
    hashed_list, from_to_pair, mID = get_ground_truth(email_sender, email_recipient)

    # mID = get_mID(hashed_list)
    # shadow_email_address = get_shadow_address(email_sender, mID)

    user_mutation_param = fetch_user_mutation_param(email_sender)
    shadow_email_address, password = get_shadow(mID, user_mutation_param.shadow_list)

    # b = datetime.datetime.now()
    # c = b - a
    # logger.info("Mutation time in milliseconds: {}".format(c.microseconds / 1000))

    # a = datetime.datetime.now()
    # email_size = sender.send_mail(shadow_email_address, email_recipient, email_sender, password, email_subject,
    #                               email_body)
    # b = datetime.datetime.now()
    # c = b - a
    # logger.info("Just sending email time in milliseconds: {}".format(c.microseconds / 1000))

    # a = datetime.datetime.now()
    sender.populate_sendbox(email_sender, email_recipient, email_subject, email_body, user_mutation_param.password)
    # b = datetime.datetime.now()
    # c = b - a
    # logger.info("Populating sendbox time in milliseconds: {}".format(c.microseconds / 1000))

    # logger.info("Email size: {}".format(email_size))

    # update_hashed_list(email_body, from_to_pair, hashed_list)
