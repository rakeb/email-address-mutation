import imaplib


def fetch_mail(email_address, password, search_criteria, mailbox):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    label_list = mail.list()
    # print(label_list)
    # Out: list of "folders" aka labels in gmail.
    mail.select(mailbox)  # connect to inbox.

    ########
    # search_using = '(FROM "' + search_criteria + '")'
    result, data = mail.search(None, search_criteria)

    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    if len(id_list) <=0:
        return None
    latest_email_id = id_list[-1]  # get the latest

    result, data = mail.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822)             for the given ID

    raw_email = data[0][1]  # here's the body, which is raw text of the whole email
    # including headers and alternate payloads

    #######





    # # print(mail.select('"[Gmail]/Sent Mail"'))
    # result, data = mail.search(None, "ALL")
    #
    # ids = data[0]  # data is a list.
    # id_list = ids.split()  # ids is a space separated string
    # latest_email_id = id_list[-1]  # get the latest
    #
    # result, data = mail.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822) for the given ID
    #
    # raw_email = data[0][1]  # here's the body, which is raw text of the whole email
    # # including headers and alternate payloads




    # print(raw_email)
    return raw_email


if __name__ == '__main__':
    mail_to = 'no-reply@accounts.google.com'
    search_criteria = '(From "' + mail_to + '")'
    fetch_mail('alice.email.mutation@gmail.com', 'emailmutation', search_criteria, 'Msent')
