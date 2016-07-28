import json
import datetime


class Message(object):

    def __init__(self, handler, *, session_id=None,
                 client_id=None, message=None, create_on=None):

        self.handler = handler
        self.session_id = session_id
        self.client_id = client_id
        self.message = message
        self.create_on = create_on

    def reply(self, message):
        """
        send message to the client
        """
        wrapped_message = dict(
            message=message,
            session_id=self.session_id,
            client_id=self.client_id,
            create_on=str(datetime.datetime.now()),
        )

        encoded_message = json.dumps(wrapped_message)
        self.handler.send(self.client_id, encoded_message)
