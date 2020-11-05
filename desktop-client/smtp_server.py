from datetime import datetime
import asyncore
from smtpd import SMTPServer

from custom_log import logger


class EmlServer(SMTPServer):
    no = 0

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        # def process_message(self, peer, mailfrom, rcpttos, data, kwargs):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
                                  self.no)
        filename = 'inbox/' + filename
        # print(filename)

        f = open(filename, 'w')
        f.write(data.decode())
        logger.info("Email saved as: {}".format(filename))
        self.no += 1


def run():
    foo = EmlServer(('127.0.0.1', 1025), None)
    # logger.info("SMTP server started...")
    logger.info("SMTP Server Started: {}: {}".format('127.0.0.1', 1025))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
