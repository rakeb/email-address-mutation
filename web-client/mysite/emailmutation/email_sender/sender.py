import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

logger = logging.getLogger('sender.py')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


# def send_mail(send_from, send_to, reply_to_email_address, password, subject, body, files=['/Users/mislam7/Dropbox/Camera Uploads/2017-11-08 12.04.52.jpg.enc']):
#     msg = MIMEMultipart()
#     msg['From'] = send_from
#     msg['To'] = send_to
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = subject
#     msg.add_header('reply-to', reply_to_email_address)
#
#     msg.attach(MIMEText(body))
#
#     for f in files or []:
#         with open(f, "rb") as fil:
#             part = MIMEApplication(
#                 fil.read(),
#                 Name=basename(f)
#             )
#         # After the file is closed
#         part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
#         msg.attach(part)
#
#     # smtp = smtplib.SMTP(server)
#     # smtp.sendmail(send_from, send_to, msg.as_string())
#     # smtp.close()
#
#     s = smtplib.SMTP('smtp.gmail.com:587')
#     s.ehlo()
#     s.starttls()
#
#     s.login(send_from, password)
#     str_msg = msg.as_string()
#     s.sendmail(send_from, send_to, str_msg)
#
#     s.quit()
#     return len(str_msg.encode('utf-8'))


def send_mail(send_from, send_to, reply_to_email_address, password, subject, body):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.add_header('reply-to', reply_to_email_address)
    msg.attach(MIMEText(body))

    # for f in files or []:
    #     with open(f, "rb") as fil:
    #         part = MIMEApplication(
    #             fil.read(),
    #             Name=basename(f)
    #         )
    #     # After the file is closed
    #     part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    #     msg.attach(part)

    # smtp = smtplib.SMTP(server)
    # smtp.sendmail(send_from, send_to, msg.as_string())
    # smtp.close()

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()

    logger.info("sender: {}, password: {}".format(send_from, password))

    s.login(send_from, password)
    str_msg = msg.as_string()
    s.sendmail(send_from, send_to, str_msg)

    s.quit()

    return len(str_msg.encode('utf-8'))


import imaplib
import time
import email.message


# import imaplib2


def open_connection(username, password):
    # Read the config file
    # config = ConfigParser.ConfigParser()
    # config.read([os.path.expanduser('~/.pymotw')])

    # Connect to the server
    # hostname = config.get('server', 'hostname')
    hostname = 'imap.gmail.com'
    port = 993
    # if verbose: print 'Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname, port)

    # Login to our account
    # username = config.get('account', 'username')
    # username = 'alice.email.mutation@gmail.com'
    # password = 'emailmutation'
    # if verbose: print 'Logging in as', username
    connection.login(username, password)
    return connection


def populate_sendbox(sender, receiver, subject, body, password):
    new_message = email.message.Message()
    # new_message.set_unixfrom('pymotw')
    new_message['Subject'] = subject
    new_message['From'] = sender
    new_message['To'] = receiver
    # new_message.set_payload('This is the body of the message.')
    # msgtext = 'This is the body of the message.'
    new_message.set_payload("%s \r\n" % body)

    # msg = MIMEMultipart()
    # msg['From'] = 'pymotw@example.com'
    # msg['To'] = 'example@example.com'
    # msg['Date'] = formatdate(localtime=True)
    # msg['Subject'] = 'subject goes here'
    # body = 'This is the body of the message.\n'
    #
    # # msg.add_header('reply-to', reply_to_email_address)
    # msg.attach(MIMEText(body))

    c = open_connection(sender, password)

    c.append('"[Gmail]/Sent Mail"', '', imaplib.Time2Internaldate(time.time()), str(new_message).encode())
    # c.append('INBOX', '', imaplib.Time2Internaldate(time.time()), msg.as_string())

    # c.select('"[Gmail]/Sent Mail"')
    # typ, [msg_ids] = c.search(None, 'ALL')
    # for num in msg_ids.split():
    #     typ, msg_data = c.fetch(num, '(BODY.PEEK[HEADER])')
    #     for response_part in msg_data:
    #         if isinstance(response_part, tuple):
    #             print('\n%s:' % num)
    #             print(response_part[1])

    # c.close()
    c.logout()

    # try:
    #     c.append('INBOX', '', imaplib.Time2Internaldate(time.time()), str(new_message))
    #
    #     c.select('INBOX')
    #     typ, [msg_ids] = c.search(None, 'ALL')
    #     for num in msg_ids.split():
    #         typ, msg_data = c.fetch(num, '(BODY.PEEK[HEADER])')
    #         for response_part in msg_data:
    #             if isinstance(response_part, tuple):
    #                 print('\n%s:' % num)
    #                 print(response_part[1])
    #
    # finally:
    #     try:
    #         c.close()
    #     except:
    #         pass
    #     c.logout()


if __name__ == '__main__':
    # open_connection()
    populate_sendbox()
