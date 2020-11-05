import logging
from email.parser import Parser
from email.policy import default

import mailparser
import re

import custom_utility as cu

import mutation

vip_list = [
    'alice.email.mutation@gmail.com',
    'bob.email.mutation@gmail.com',
    'rakeb.void@gmail.com',
]

shadow_list = [
    'alice.email.mutation.1@gmail.com',
    'bob.email.mutation.1@gmail.com',
    'rakeb.mazharul.1@gmail.com',
]

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


def analyze_request(reqeust):
    str_req = reqeust.decode()
    logging.info("Request received from Mail-Client: {}".format(str_req))
    mail = mailparser.parse_from_string(str_req)
    # print("helloworld")


def check_if_recipient_is_vip(list_data):
    raw_string = ''

    for line in list_data:
        if 'append "[Gmail]/Sent Mail"' not in line:
            raw_string += line
    mail = mailparser.parse_from_string(raw_string)

    mail_to = mail.to[0][1]
    # mail_from = mail.from_[0][1]
    # sub = mail.subject
    # print("subject: {}".format(sub))
    # mutation.mutate_and_send(mail)

    if mail_to in vip_list:
        return True, mail, mail_to
    else:
        return False, mail, mail_to


# def get_sender_email_address(list_response):
#     full_string = ''
#     for lines in list_response:
#         line_as_list = lines.splitlines()
#         for line in line_as_list:
#             full_string += line
#     match = re.search(r'<[\w\.-]+@[\w\.-]+>', full_string)
#     from_address = match.group(0)
#     from_address = from_address[1:-1]
#     # print(from_address)
#     return from_address


def get_sender_email_address(full_str):
    match = re.search(r'<[\w\.-]+@[\w\.-]+>', full_str)
    from_address = match.group(0)
    from_address = from_address[1:-1]
    # print(from_address)
    return from_address


def check_if_sender_vip(from_address):
    if from_address in vip_list:
        return True
    else:
        return False


# def add_threat_in_subject(list_response):
#     new_list_response = []
#     for line in list_response:
#         byte_line = line.encode()
#         splitted_line = line.splitlines()
#         if 'Subject:' in line:
#             line.replace('Subject:', 'Subject:[Threat]')
#         new_list_response.append(line)
#     return new_list_response

def add_threat_in_subject(full_str):
    if 'Subject:' in full_str:
        full_str = full_str.replace('Subject:', 'Subject:[Threat]')
    return full_str


def check_if_sender_shadow(from_address):
    if from_address in shadow_list:
        return True
    else:
        return False


# def remove_mutation_id(list_response, shadow_sender_address, real_sender_address):
#     new_list_response = []
#     for line in list_response:
#         if shadow_sender_address in line:
#             line.replace(shadow_sender_address, real_sender_address)
#         new_list_response.append(line)
#     return new_list_response


def remove_mutation_id(full_str=None, shadow_sender_address=None, real_sender_address=None):
    if shadow_sender_address is None:
        shadow_sender_address = get_sender_email_address(full_str)
        real_sender_address, before_at, mutation_id, domain = cu.get_real_email_address(shadow_sender_address)
    if shadow_sender_address in full_str:
        full_str = full_str.replace(shadow_sender_address, real_sender_address)
    return full_str


def test_replace(param, param1):
    str = 'alice is bad as like alice with bob'
    str = str.replace(param, param1)
    print(str)


def get_one_sentence(list_response):
    full_string = ''
    for lines in list_response:
        full_string += lines
    return full_string


def previous_word(target, source):
    for i, w in enumerate(source):
        if w == target:
            return source[i - 1]


if __name__ == '__main__':
    r = b'To: rakeb.void@gmail.com\r\nFrom: Rakeb Mazhar 1 <rakeb.mazharul.1@gmail.com>\r\nSubject: Will it work?\r\nMessage-ID: <f359c746-a5bd-9335-e831-96c6a08a71f0@gmail.com>\r\nDate: Wed, 17 Apr 2019 20:15:19 -0400\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0)\r\n Gecko/20100101 Thunderbird/60.6.1\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8; format=flowed\r\nContent-Transfer-Encoding: 7bit\r\nContent-Language: en-US\r\n\r\nMaybe I cant send mail through bot\r\n'
    r = ['4 append "[Gmail]/Sent Mail" (\\Seen) {459}\r\n',
         'To: bob.email.mutation@gmail.com\r\nFrom: Rakeb Mazhar 1 <alice.email.mutation@gmail.com>\r\nSubject: sadkad\r\nMessage-ID: <50378ffe-869c-cc9f-7885-efea7de55656@gmail.com>\r\nDate: Thu, 18 Apr 2019 22:55:35 -0400\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0)\r\n Gecko/20100101 Thunderbird/60.6.1\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8; format=flowed\r\nContent-Transfer-Encoding: 7bit\r\nContent-Language: en-US\r\n\r\njgkgkgk iasdu g hLFHb\r\n\r\n']
    # analyze_request(r)
    # check_if_recipient_is_vip(r)
    # check_if_recipient_vip_from_response_list(None)
    # get_sender_email_address(r)

    response_list = [
        '* 5 FETCH (UID 6 RFC822.SIZE 4950 BODY[] {4950}\r\nDelivered-To: alice.email.mutation@gmail.com\r\nReceived: by 2002:a92:c702:0:0:0:0:0 with SMTP id a2csp1191032ilp;\r\n        Sun, 21 Apr 2019 13:34:14 -0700 (PDT)\r\nX-Received: by 2002:a5b:587:: with SMTP id l7mr1150537ybp.44.1555878854786;\r\n        Sun, 21 Apr 2019 13:34:14 -0700 (PDT)\r\nARC-Seal: i=1; a=rsa-sha256; t=1555878854; cv=none;\r\n        d=google.com; s=arc-20160816;\r\n        b=dYAHEn3YDMz9UW/PMw1w7hds5yATckr+zkovo4l3IcFK+LIkFF6juZ7MnLrUpWsNMI\r\n         q',
        'WqJ2OH+6Rg4ErukqkB5A/TPqsZBv6Z3lxqRmQt1INg8ZXB//9DP4G1xegomUE0lES70\r\n         vsRF+mvP3WcsQWQhBLIztyS+Ces/aWg9EmOJsfRp6hKna9ruQ2/lVVJjiG22BeCD3Azx\r\n         W6GIxK0gOwMwLPNNWsHwLn2+BFKeBX0rpTLcNKITOLr5bJCCxY9havb5fNmLC+qxKh+2\r\n         GG/QYRk55Ad8DmGKOi4PtuAADeTjxbSurNkIKHaQ28ko1nRgid0lX0YfT0vo6RqJPCs8\r\n         vMNQ==\r\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;\r\n        h=to:subject:message-id:date:from:mime-version:dkim-signature;\r\n        bh=b6AaQFeOl1Wi4tqvxCtVe9bUGJMnE8ljzUu2lY1BA1E=;\r\n        b=wQD2C9oj6wrzL79eP7iGi4lF7WG75dQMe40UUaFLUbvqN/KIxCLu4XlqZ+GewtqMvH\r\n         YX6DIKGwHToDZ7BDfARe/P6X8WiYpd+9YTcaaZZB3RlaSwoKI3UirmB82x7xB0NNzSjM\r\n         HjrZHyvMVA2yRpjg3y2887kUxRcx62k+K9tpkkSDgbA0NvFx+Y4uHr6tR1ZhPdUIn/tp\r\n         Rsb095Vn5xiGPdKSnHRMvJ37DYjTFPCWz+qmnvAUJYKVZ7A+RJAVaR2a6D7HJxvKBeTc\r\n         h76QUHlBkC5Wn+Ud8YCwtN97c3aTeDPo0nl64fEme8F/cGsoIkqe8Ngyy8Af5ACCELVn\r\n         Vh5w==\r\nARC-Authentication-Results: i=1; mx.google.com;\r\n       dkim=pass he',
        'ad',
        'er.i=@gmail.com header.s=20161025 header.b=To3o6Zga;\r\n       spf=pass (google.com: domain of bob.email.mutation@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=bob.email.mutation@gmail.com;\r\n       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com\r\nReturn-Path: <bob.email.mutation@gmail.com>\r\nReceived: from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])\r\n        by mx.google.com with SMTPS id z63sor4825792ywe.123.2019.04.21.13.34.14\r\n        for <alice.email.mutation@gmail.com>\r\n        (Google Transport Security);\r\n        Sun, 21 Apr 2019 13:34:14 -0700 (PDT)\r\nReceived-SPF: pass (google.com: domain of bob.email.mutation@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;\r\nAuthentication-Results: mx.google.com;\r\n       dkim=pass header.i=@gmail.com header.s=20161025 header.b=To3o6Zga;\r\n       spf=pass (google.com: domain of bob.email.mutation@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=bob.email.mu',
        'tation@gmail.com;\r\n       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com\r\nDKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=gmail.com; s=20161025;\r\n        h=mime-version:from:date:message-id:subject:to;\r\n        bh=b6AaQFeOl1Wi4tqvxCtVe9bUGJMnE8ljzUu2lY1BA1E=;\r\n        b=To3o6ZgaY',
        'Z1jrmMmrYHapzAz9qXuwqpfyE0fNSFHL7cvdXXhJ5kVtOXtYc+4lRPOxy\r\n         6jpn7dHMpKm0b8qr3CPR1hSTQ+/y4OnU7FQVeyfP8Jo9NE7DKpNgTx8bGBChm43UX6PX\r\n         gS42OjyqTqhWtsdZwXS0hoCiCzNGRwRPrBwfe8l3hjM87YNx0bq9kMgzuSIrh1Z+TAvf\r\n         ojv9798kFGPk4J9Fs+N1CSrj+3oeDcqs40iKK+VkhP41n0ziIYyGG4XPFYX2kkPts9Q0\r\n         Mycu6FAwtOssv7TC0Op9OS2TTSxc6Uq4m6qtgH0GnhdOofupUk2sbWKhd4X7ikuPvaHl\r\n         fenQ==\r\nX-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\r\n        d=1e100.net; s=20161025;\r\n        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;\r\n        bh=b6AaQFeOl1Wi4tqvxCtVe9bUGJMnE8ljzUu2lY1BA1E=;\r\n        b=qKbZKa/mPupiJ74TdPhWDejVLYCnMSfRvTvjvuH5rTmYW+sAUJgE5yuHlUkO9DDcmo\r\n         ',
        'pMkjz/jUhyVfXVFade12lnaJWmCu6p7tkRWWHwcc5S7YR8UxA0XcR4l8mFU+KZ1dCEjC\r\n         wf0USeoZrSs/qxudIxPYob/xtFQk4JWMHPwtzIO/M9ID8bPlb9VrA13JYad8w5lfeXdO\r\n         06MDLiO/oyobIgYz27/8bG1AYlkbCYNJ18aHH2ZToNBM+TFzaDmjhWQwflerTrUYG3M/\r\n         XEflzyLqdxMJ3BfyGDJduv1j3zB8oOMJBje5nE3VL+jDIELHgIA5Ixyd446hogNyIDf/\r\n         tP4A==\r\nX-Gm-Message-State: APjAAAXge0R2BoWKTE9U6ysivx6XIE72G18ACv40kkpHpqIQU6kfosol\r\n\thz/OwcPxft+ibIt+DCNldEVGxuLsBDBYwkAHPLt3IQ==\r\nX-Google-Smtp-Source: APXvYqy3yFVBREOoQ4lKS5OpqmWxorPvIe/X54KivIKKIpT6ZHecX3jkB8KidAx4BJUlIbKzwZthiWuLrBLSXtwuvgg=\r\nX-Received: by 2002:a81:5ed4:: with SMTP id s203mr12278235ywb.281.1555878854423;\r\n Sun, 21 Apr 2019 13:34:14 -0700 (PDT)\r\nMIME-Version: 1.0\r\nFrom: Bob Em <bob.email.mutation@gmail.com>\r\nDate: Sun, 21 Apr 2019 16:34:03 -0400\r\nMessage-ID: <CAJcAnS4F4s5GHH7tugwzzyCuhKB3Q7QBopfO9HR-QTkGUfFvvw@mail.gmail.com>\r\nSubject: Lets see what happenes\r\nTo: alice.email.mutation@gmail.com\r\nContent-Type: multipart/alternative; boundary="0000000000006e79210587104651"\r\n\r\n--0',
        '000000000006e79210587104651\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\nDear Alice,\r\n\r\nSomething will be wrong in this email.\r\n\r\nThanks,\r\n\r\n--0000000000006e79210587104651\r\nContent-Type: text/html; charset="UTF-8"\r\n\r\n<div dir="ltr">Dear Alice,<div><br></div><div>Something will be wrong in this email.</div><div><b',
        'r></div><div>Thanks,</div></div>\r\n\r\n--0000000000006e79210587104651--\r\n)\r\n9', ' OK Success\r\n']

    # response_list = add_threat_in_subject(response_list)
    # print(response_list)

    # test_replace("alice", "bob")
    fullstring = get_one_sentence(response_list)
    # print(fullstring)

    if 'OK Success' in fullstring:
        word_before_ok = previous_word('OK', fullstring.split())
        print(word_before_ok)
