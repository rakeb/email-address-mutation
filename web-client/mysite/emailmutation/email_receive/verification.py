import datetime
import hashlib
import logging

from emailmutation.email_sender.mutation import fetch_user_mutation_param, get_shadow
from emailmutation.models import HashedEmailTable, MarkVerificationStatus, AllShadowEmail, AllVipEmail

logger = logging.getLogger('verification.py')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

mod = 1


def check_vip_sender(email_sender):
    try:
        all_emails_obj = AllVipEmail.objects.filter(vip_email=email_sender).latest('vip_email')
        logger.debug("Sender: {} is a VIP, should not send email directly.".format(email_sender))
        return True
    except AllVipEmail.DoesNotExist:
        logger.debug("Sender: {} is not a VIP.".format(email_sender))
        return False


def check_sender_shadow(email_sender):
    try:
        all_emails_obj = AllShadowEmail.objects.filter(shadow_email=email_sender).latest('shadow_email')
        logger.debug("Sender: {} is a Shadow, will begin verification.".format(email_sender))
        return True
    except AllShadowEmail.DoesNotExist:
        logger.debug("Sender: {} is not a Shadow. Stopping verification.".format(email_sender))
        return False


def get_mID(sender, recipient):
    from_email = sender
    to_email = recipient

    try:
        hashed_email_table_obj = HashedEmailTable.objects.filter(from_address=from_email, to_address=to_email).latest(
            'id')
        logger.debug(
            "Hashed List found in DB, from: {}, to: {}, hashed list: {}".format(from_email, to_email,
                                                                                hashed_email_table_obj.last_n_email_hash))
        return hashed_email_table_obj.mID, (from_email, to_email)
    except HashedEmailTable.DoesNotExist:
        from_email = recipient
        to_email = sender
        try:
            hashed_email_table_obj = HashedEmailTable.objects.filter(from_address=from_email,
                                                                     to_address=to_email).latest('id')
            logger.debug(
                "Hashed List found in DB, from: {}, to: {}, hashed list: {}".format(from_email, to_email,
                                                                                    hashed_email_table_obj.last_n_email_hash))
            return hashed_email_table_obj.mID, (from_email, to_email)
        except HashedEmailTable.DoesNotExist:
            return None, None


def get_real_email_address(shadow_email_address):
    splitted_shadow_address = shadow_email_address.split('@')
    before_shadow_at = splitted_shadow_address[0]
    domain = splitted_shadow_address[1]

    splitted_before_at = before_shadow_at.rsplit('.', 1)
    mutation_id = splitted_before_at[1]
    before_at = splitted_before_at[0]

    real_email_address = before_at + '@' + domain

    return real_email_address, before_at, mutation_id, domain


def update_mID(data, from_email, to_email):
    m = hashlib.sha256()
    m.update(data.encode())

    # # TODO for only evaluation purpose
    # with open("/Users/mislam7/Dropbox/Adaptive_Conceal.pptx", "rb") as f:
    #     byte = f.read(1)
    #     while byte:
    #         # Do stuff with byte.
    #         m.update(byte)
    #         byte = f.read(1)

    hashed = m.digest()

    mutation_id = int.from_bytes(hashed, byteorder='big')
    mutation_id %= mod

    HashedEmailTable.objects.filter(from_address=from_email, to_address=to_email).update(mID=mutation_id)


def verify_mutation(email_sender, real_email_address, email_recipient):
    mID, from_to_pair = get_mID(real_email_address, email_recipient)

    if mID is None:
        logger.info("No hashed value found for Sender: {}, receiver: {}, verification does not applicable".format(
            email_sender, email_recipient))
        return False

    user_mutation_param = fetch_user_mutation_param(real_email_address)
    shadow_email_address, password = get_shadow(mID, user_mutation_param.shadow_list)

    if shadow_email_address == email_sender:
        logger.info("Verification Successful. Sender: {}, is using a valid shadow".format(email_sender))
        return True
    else:
        logger.info("Verification Failed. Sender: {}, is NOT using a valid shadow".format(email_sender))
        return False


def save_verification_status(message_id):
    obj, created = MarkVerificationStatus.objects.update_or_create(message_id=message_id, status=True)


def check_already_verified(message_id):
    try:
        mark_verification_status_obj = MarkVerificationStatus.objects.filter(message_id=message_id).latest('message_id')
        return mark_verification_status_obj.status
    except MarkVerificationStatus.DoesNotExist:
        return None


def process_email_for_verification(mail_object):
    message_id = mail_object['message_id']
    email_sender = mail_object['email_sender']['emailAddress']
    email_body = mail_object['email_body']
    email_recipient = mail_object['email_recipient'][0]

    a = datetime.datetime.now()

    status = check_already_verified(message_id)

    if status is not None:
        if status is True:
            logger.info("Verification Successful, already verified message_id: {}".format(message_id))
            return True
        else:
            logger.info("Verification Failed, already verified message_id: {}".format(message_id))
            return False

    if check_vip_sender(email_sender):
        logger.info("Sender: {}, is a VIP, verification Failed".format(email_sender))
        return False
    if not check_sender_shadow(email_sender):
        logger.info("Sender: {}, is a NOT a Shadow, verification does not required".format(email_sender))
        return None
    else:
        real_email_address, before_at, random_prefix, domain = get_real_email_address(email_sender)
        status = verify_mutation(email_sender, real_email_address, email_recipient)

    b = datetime.datetime.now()
    c = b - a
    logger.info("Verification time in milliseconds: {}".format(c.microseconds / 1000))

    if status:
        save_verification_status(message_id)
        update_mID(email_body, real_email_address, email_recipient)
    return status
