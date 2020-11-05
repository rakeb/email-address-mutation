import logging
import mailparser
import mutation

vip_list = [
    'alice.email.mutation@gmail.com',
    'bob.email.mutation@gmail.com',
    'rakeb.void@gmail.com',
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
    mail_from = mail.from_[0][1]

    mutation.mutate_and_send(mail)

    if mail_to in vip_list:
        return True, mail
    else:
        return False, mail


if __name__ == '__main__':
    r = b'To: rakeb.void@gmail.com\r\nFrom: Rakeb Mazhar 1 <rakeb.mazharul.1@gmail.com>\r\nSubject: Will it work?\r\nMessage-ID: <f359c746-a5bd-9335-e831-96c6a08a71f0@gmail.com>\r\nDate: Wed, 17 Apr 2019 20:15:19 -0400\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0)\r\n Gecko/20100101 Thunderbird/60.6.1\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8; format=flowed\r\nContent-Transfer-Encoding: 7bit\r\nContent-Language: en-US\r\n\r\nMaybe I cant send mail through bot\r\n'
    r = ['4 append "[Gmail]/Sent Mail" (\\Seen) {459}\r\n',
         'To: bob.email.mutation@gmail.com\r\nFrom: Rakeb Mazhar 1 <alice.email.mutation@gmail.com>\r\nSubject: sadkad\r\nMessage-ID: <50378ffe-869c-cc9f-7885-efea7de55656@gmail.com>\r\nDate: Thu, 18 Apr 2019 22:55:35 -0400\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0)\r\n Gecko/20100101 Thunderbird/60.6.1\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8; format=flowed\r\nContent-Transfer-Encoding: 7bit\r\nContent-Language: en-US\r\n\r\njgkgkgk iasdu g hLFHb\r\n\r\n']
    # analyze_request(r)
    check_if_recipient_is_vip(r)
