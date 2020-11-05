import datetime
import socket
import ssl
import threading
import time
import traceback

import client_request_analysis as cra
import custom_utility as cu
import mutation as m
from custom_log import logger

TO_ADDRESS = 'alice.email.mutation@gmail.com'


class GmailClient():
    def __init__(self, thunderbird_client_socket, flag_queue):
        logger.debug("Startig Gmail Client...")

        self.thunderbird_client_socket = thunderbird_client_socket
        self.flag_queue = flag_queue

        self.tag = '1'  # default 1
        self.command = None
        # self.host = 'exchange.iinet.net.au'   # microsoft
        self.host = 'imap.gmail.com'  # gmail
        self.port = 993

        sock = socket.socket(socket.AF_INET)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        self.gmail_client_socket = context.wrap_socket(sock, server_hostname=self.host)
        self.gmail_client_socket.connect((self.host, self.port))

        # append command handling
        self.command_data = []
        # self.append_tag = '1'
        # self.append_tag_flag = False
        self.first_time_in_append = False

        # fetch command handling
        self.fetch_header_tag = False
        self.fetch_body_tag = False
        self.shadow_sender_address = None
        self.real_sender_address = None
        self.flag_dict = {
            'threat_flag': False,
            'remove_mutation_id_flag': False
        }
        # self.threat_flag = False
        # self.will_remove_mutation_id = False

        logger.debug("Gmail Client Started")
        threading.Thread(
            target=self.receive_and_send,
            # args=(thunderbird_client_socket,)
        ).start()

    def send_to_gmail(self, data):
        logger.debug("Previous command: {}".format(self.command))
        logger.info("Thunderbird --> Gmail: {}".format(data))
        command_str = data.decode()
        try:
            if self.command != 'append':
                command_as_list = command_str.rstrip().split()
                self.tag = command_as_list[0]
                self.command = command_as_list[1]

                if self.command == 'append':
                    pass
                elif self.command == 'UID' and command_as_list[2] == 'fetch':
                    header_fetch_str = 'UID RFC822.SIZE FLAGS BODY.PEEK[HEADER.FIELDS'
                    # body_fetch_str = 'UID RFC822.SIZE BODY.PEEK'
                    body_fetch_str = 'UID RFC822.SIZE BODY'

                    if header_fetch_str in command_str:
                        self.fetch_header_tag = True
                    elif body_fetch_str in command_str:
                        self.fetch_body_tag = True
                        logger.info("body tag set")
                    else:
                        pass
                else:
                    pass
            else:  # command is append
                if data != b'\r\n':
                    self.command_data.append(command_str)
                    logger.debug("command data in string: {}".format(self.command_data))
                else:  # end of append command
                    # for time
                    prev_time = datetime.datetime.now()
                    is_recipient_vip, mail_object, to_address = cra.check_if_recipient_is_vip(self.command_data)
                    if not is_recipient_vip:
                        logger.info("To address: {} is not a vip, send it directly to gmail".format(to_address))
                        # self.send_list_command_to_gmail(self.command_data)
                    else:
                        self.command = ''
                        del self.command_data[:]

                        # this will send real email using mutated from address
                        m.mutate_and_send(mail_object)
                    curr_time = datetime.datetime.now()
                    time_diff = curr_time - prev_time
                    self.save_time_diff_in_file('mutation_time_MB_2.txt', time_diff.microseconds)

            logger.debug("Command and tags: {} and {}".format(self.command, self.tag))
            logger.info("Data is sending to gmail: {}".format(data))
            self.gmail_client_socket.sendall(data)
        except IndexError as e:
            logger.error("Gmail client closed with exception: {}".format(e))

    # def send_to_gmail(self, data):
    #     logger.debug("Previous command: {}".format(self.command))
    #     logger.info("Thunderbird --> Gmail: {}".format(data))
    #     try:
    #         if self.command != 'append':
    #             command_str = data.decode()
    #             command_as_list = command_str.rstrip().split()
    #             self.tag = command_as_list[0]
    #             self.command = command_as_list[1]
    # 
    #             if self.command == 'append':
    #                 self.first_time_in_append = True
    #             elif self.command == 'UID' and command_as_list[2] == 'fetch':
    #                 header_fetch_str = 'UID RFC822.SIZE FLAGS BODY.PEEK[HEADER.FIELDS'
    #                 # body_fetch_str = 'UID RFC822.SIZE BODY.PEEK'
    #                 body_fetch_str = 'UID RFC822.SIZE BODY'
    # 
    #                 if header_fetch_str in command_str:
    #                     self.fetch_header_tag = True
    #                 elif body_fetch_str in command_str:
    #                     self.fetch_body_tag = True
    #                     logger.info("body tag set")
    #                 else:
    #                     pass
    #             else:
    #                 pass
    #         else:
    #             str_command = data.decode()
    #             self.command_data.append(str_command)
    #             logger.debug("command data in string: {}".format(self.command_data))
    # 
    #             if data == b'\r\n':
    #                 is_recipient_vip, mail_object, to_address = cra.check_if_recipient_is_vip(self.command_data)
    #                 if not is_recipient_vip:
    #                     logger.info("To address: {} is not a vip, send it directly to gmail".format(to_address))
    #                     self.send_list_command_to_gmail(self.command_data)
    #                 else:
    #                     response = self.tag + ' OK Success'
    #                     response = response.encode() + b'\r\n'
    #                     logger.info("IMPORTANT: Bot replying (mimicking Gmail) to Thunderbird: {}".format(response))
    #                     self.send_raw_response_to_thinderbird(response, "Bot --> Thunderbird: {}")
    #                     self.command = ''
    # 
    #                     # TODO nasty job will be done here
    #                     str_append_command = self.command_data[0]
    #                     str_append_command = str_append_command.replace('[Gmail]/Sent Mail', 'Msent')
    #                     self.command_data[0] = str_append_command
    #                     self.send_list_command_to_gmail(self.command_data)
    # 
    #                     # this will send real email using mutated from address
    #                     m.mutate_and_send(mail_object)
    #             logger.info("returning from send_to_gmail method")
    #             return
    # 
    #         logger.debug("Command and tags: {} and {}".format(self.command, self.tag))
    # 
    #         if self.command == 'append' and self.first_time_in_append:
    #             str_command = data.decode()
    #             self.command_data.append(str_command)
    # 
    #             # self.append_tag = self.tag
    #             # self.append_tag_flag = True
    # 
    #             response = b'+ go ahead\r\n'
    #             logger.info("IMPORTANT: Bot replying (mimicking Gmail) to Thunderbird: {}".format(response))
    #             self.send_raw_response_to_thinderbird(response, "Bot --> Thunderbird: {}")
    # 
    #             self.first_time_in_append = False
    #             logger.info("returning from send_to_gmail method")
    #             return
    # 
    #         logger.info("Data is sending to gmail: {}".format(data))
    #         self.gmail_client_socket.sendall(data)
    #     except IndexError as e:
    #         logger.error("Gmail client closed with exception: {}".format(e))

    # def send_to_gmail(self, data):
    #     logger.info("Thunderbird --> Gmail: {}".format(data))
    #     command_str = data.decode()
    #     try:
    #         if self.command != 'append':
    #             command_as_list = command_str.rstrip().split()
    #             self.tag = command_as_list[0]
    #             self.command = command_as_list[1]
    #
    #             if self.command == 'append':
    #                 self.command_data.append(command_str)
    #                 response = b'+ go ahead\r\n'
    #                 logger.info("IMPORTANT: Bot replying (mimicking Gmail) to Thunderbird: {}".format(response))
    #                 self.send_raw_response_to_thinderbird(response, "Bot --> Thunderbird: {}")
    #                 logger.info("returning from send_to_gmail method")
    #                 return
    #         else:
    #             self.command_data.append(command_str)
    #             logger.debug("command data in string: {}".format(self.command_data))
    #             if data == b'\r\n':
    #                 response = self.tag + ' OK Success'
    #                 response = response.encode() + b'\r\n'
    #                 logger.info("IMPORTANT: Bot replying (mimicking Gmail) to Thunderbird: {}".format(response))
    #                 self.send_raw_response_to_thinderbird(response, "Bot --> Thunderbird: {}")
    #                 self.command = ''
    #             logger.info("returning from send_to_gmail method")
    #             return
    #         logger.info("Data is sending to gmail: {}".format(data))
    #         self.gmail_client_socket.sendall(data)
    #     except IndexError as e:
    #         logger.error("Gmail client closed with exception: {}".format(e))

    # def send_to_gmail(self, data):
    #     logger.info("Thunderbird --> Gmail: {}".format(data))
    #     try:
    #         command_str = data.decode()
    #         command_as_list = command_str.rstrip().split()
    #         self.tag = command_as_list[0]
    #         self.command = command_as_list[1]
    #     except IndexError as e:
    #         logger.error("Index error: {}".format(e))
    # 
    #     logger.info("Data is sending to gmail: {}".format(data))
    #     self.gmail_client_socket.sendall(data)

    def receive_and_send(self):
        logger.info("Gmail client is ready to receive and send back to ThunderBird")
        list_response = []
        while True:
            try:
                r = self.gmail_client_socket.recv(1024)
                if not r:
                    break;
                else:
                    str_response = r.decode()

                    logger.debug("String Response: {}".format(str_response))

                    capability = '* CAPABILITY IMAP4rev1 YESAUTH\r\n' + \
                                 self.tag + ' OK Pre-login capabilities listed, post-login capabilities have more\r\n'

                    if 'CAPABILITY' in str_response:
                        if 'authenticated (Success)' not in str_response:
                            str_response = capability
                        else:
                            str_response = self.tag + ' OK login (Success)\r\n'

                    list_response.append(str_response)
                    one_sentence_response = cra.get_one_sentence(list_response)

                    if self.fetch_header_tag:
                        if 'OK Success' in one_sentence_response:
                            word_before_ok = self.previous_word('OK', one_sentence_response.split())
                            if self.tag == word_before_ok:
                                self.fetch_header_tag = False
                                logger.info("Fetched Email Header for analysis: {}".format(one_sentence_response))
                                from_address = cra.get_sender_email_address(one_sentence_response)
                                logger.info("from_address: {}".format(from_address))
                                is_vip = cra.check_if_sender_vip(from_address)
                                if is_vip:
                                    # self.threat_flag = True
                                    # self.flag_dict['threat_flag'] = True
                                    logger.info("From address: {} is VIP, will adding THREAT alert in subject".format(
                                        from_address))
                                    one_sentence_response = cra.add_threat_in_subject(one_sentence_response)
                                elif cra.check_if_sender_shadow(from_address):
                                    is_authentic, real_from_address = m.validate_sender(from_address, TO_ADDRESS)
                                    if is_authentic:
                                        logger.info("Mutation Authentication complete, will remove mutation id...")
                                        self.shadow_sender_address = from_address
                                        self.real_sender_address = real_from_address
                                        # self.will_remove_mutation_id = True
                                        self.flag_dict['remove_mutation_id_flag'] = True
                                        one_sentence_response = cra.remove_mutation_id(one_sentence_response,
                                                                                       self.shadow_sender_address,
                                                                                       self.real_sender_address)
                                    else:
                                        # self.threat_flag = True
                                        self.flag_dict['threat_flag'] = True
                                        logger.info("Mutation Authentication failed, adding THREAT alert")
                                        one_sentence_response = cra.add_threat_in_subject(one_sentence_response)
                                else:
                                    pass
                                self.flag_queue.put(self.flag_dict)
                        else:
                            continue

                    # if self.fetch_body_tag:
                    #     if 'OK Success' in one_sentence_response:
                    #         word_before_ok = self.previous_word('OK', one_sentence_response.split())
                    #         if self.tag == word_before_ok:
                    #             self.fetch_body_tag = False
                    #             if not self.flag_queue.empty():
                    #                 flag_dict = self.flag_queue.get()
                    #                 threat_flag = flag_dict['threat_flag']
                    #                 remove_mutation_id_flag = flag_dict['remove_mutation_id_flag']
                    #                 if threat_flag:
                    #                     one_sentence_response = cra.add_threat_in_subject(one_sentence_response)
                    #                 if remove_mutation_id_flag:
                    #                     one_sentence_response = cra.remove_mutation_id(one_sentence_response)
                    #                     logger.info("mutation id removed...")
                    #     else:
                    #         continue

                    if self.fetch_body_tag:
                        if 'OK Success' in one_sentence_response:
                            word_before_ok = self.previous_word('OK', one_sentence_response.split())
                            if self.tag == word_before_ok:
                                self.fetch_body_tag = False
                                logger.info("Fetched Complete Email for analysis: {}".format(one_sentence_response))
                                # can produce error
                                # from_address = cra.get_sender_email_address(one_sentence_response)
                                to_address, from_address, mail_object = cu.get_mail_from_str(one_sentence_response)

                                logger.info("from_address: {}, to_address: {}".format(from_address, to_address))

                                # for time diff
                                prev_time = datetime.datetime.now()

                                is_vip = cra.check_if_sender_vip(from_address)
                                if is_vip:
                                    # self.threat_flag = True
                                    # self.flag_dict['threat_flag'] = True
                                    logger.info("From address: {} is VIP, will adding THREAT alert in subject".format(
                                        from_address))
                                    one_sentence_response = cra.add_threat_in_subject(one_sentence_response)
                                    # for time diff
                                    curr_time = datetime.datetime.now()
                                    time_diff = curr_time - prev_time
                                    self.save_time_diff_in_file('verification_time_MB_2.txt', time_diff.microseconds)
                                elif cra.check_if_sender_shadow(from_address):
                                    is_authentic, real_from_address = m.validate_sender(from_address, to_address)
                                    if is_authentic:
                                        logger.info("Mutation Authentication complete, will remove mutation id...")
                                        # self.shadow_sender_address = from_address
                                        # self.real_sender_address = real_from_address
                                        # self.will_remove_mutation_id = True
                                        # self.flag_dict['remove_mutation_id_flag'] = True
                                        # one_sentence_response = cra.remove_mutation_id(one_sentence_response,
                                        #                                                self.shadow_sender_address,
                                        #                                                self.real_sender_address)
                                        one_sentence_response = cra.remove_mutation_id(one_sentence_response,
                                                                                       from_address, real_from_address)
                                    else:
                                        # self.threat_flag = True
                                        # self.flag_dict['threat_flag'] = True
                                        logger.info("Mutation Authentication failed, adding THREAT alert")
                                        one_sentence_response = cra.add_threat_in_subject(one_sentence_response)
                                    # for time diff
                                    curr_time = datetime.datetime.now()
                                    time_diff = curr_time - prev_time
                                    self.save_time_diff_in_file('verification_time_MB_2.txt', time_diff.microseconds)
                                else:
                                    pass
                                    # self.flag_queue.put(self.flag_dict)
                        else:
                            continue

                    # one_sentence_response = cra.get_one_sentence(list_response)
                    self.send_response_to_thinderbird(one_sentence_response)
                    del list_response[:]

                    # self.send_list_response_to_thinderbird(list_response)
            except BrokenPipeError as e:
                logger.error("ThunderBird Client socket is down: {}".format(e))
                traceback.print_exc()
                return

    def close_gmail_socket(self):
        # print("James client closing...")
        logger.debug("Gmail client closing...")
        self.gmail_client_socket.close()

    def previous_word(self, target, source):
        for i, w in enumerate(source):
            if w == target:
                return source[i - 1]

    def send_list_command_to_gmail(self, list_command):
        try:
            for str_command in list_command:
                byte_command = str_command.encode()
                logger.info("Bot --> Gmail: {}".format(byte_command))
                self.gmail_client_socket.sendall(byte_command)
                time.sleep(0.1)

            del list_command[:]
        except Exception as e:
            logger.error("Gmail client closed with exception: {}".format(e))

    def send_list_response_to_thinderbird(self, list_response):
        for str_response in list_response:
            if 'jerry@test.com' in str_response:
                str_response = str_response.replace('jerry@test.com', 'rakeb@test.com')
                logger.debug("Before sending str_response: {}".format(str_response))
            self.send_response_to_thinderbird(str_response)
        del list_response[:]

    def send_response_to_thinderbird(self, response):
        byte_response = response.encode()
        self.send_raw_response_to_thinderbird(byte_response)

    def send_raw_response_to_thinderbird(self, byte_response, additional_string=None):
        if additional_string is None:
            additional_string = "Gmail --> Thunderbird: {}"
        logger.info(additional_string.format(byte_response))
        self.thunderbird_client_socket.send(byte_response)

    def save_time_diff_in_file(self, filename, timediff):
        with open(filename, "a") as myfile:
            myfile.write(str(timediff/1000))
            myfile.write('\n')
