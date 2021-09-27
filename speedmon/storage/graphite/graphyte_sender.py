import logging
import time

from graphyte import Sender

logger = logging.getLogger(__name__)

class GraphyteSender(Sender):
    def send_socket(self, message):
        """Low-level function to send message bytes to this Sender's socket.
        You should usually call send() instead of this function (unless you're
        subclassing or writing unit tests).
        """
        if self.log_sends:
            start_time = time.time()
        try:
            self.send_message(message)
        except Exception as error:
            logger.error('error sending message {!r}: {}'.format(message, error))
            raise
        else:
            if self.log_sends:
                elapsed_time = time.time() - start_time
                logger.info('sent message {!r} to {}:{} in {:.03f} seconds'.format(
                        message, self.host, self.port, elapsed_time))