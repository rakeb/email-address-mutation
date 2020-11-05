# Import smtplib for the actual sending function
import smtplib

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# Import the email modules we'll need


def send_(email_from=None, password=None, email_to=None, msg=None):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # fp = open(textfile, 'rb')
    # # Create a text/plain message
    # msg = MIMEText(fp.read())
    # fp.close()

    # me == the sender's email address
    # you == the recipient's email address

    # ------------
    # me = 'alice.email.mutation.1@gmail.com'
    # you = 'bob.email.mutation@gmail.com'
    # msg = MIMEText('Hello world')
    # msg['Subject'] = 'Email Mutation'
    # msg['From'] = me
    # msg['To'] = you
    # ------------

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()

    # ------------
    # https://myaccount.google.com/apppasswords
    # s.login(me, 'emailmutation')
    # s.sendmail(me, [you], msg.as_string())
    # ------------

    s.login(email_from, password)
    s.sendmail(email_from, email_to, msg)

    s.quit()


def send_mail(send_from, send_to, password, subject, body, files=None):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    # smtp = smtplib.SMTP(server)
    # smtp.sendmail(send_from, send_to, msg.as_string())
    # smtp.close()

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()

    s.login(send_from, password)
    s.sendmail(send_from, send_to, msg.as_string())

    s.quit()


if __name__ == '__main__':
    send_()
