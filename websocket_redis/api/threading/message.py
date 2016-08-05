import json
import datetime

from websocket_redis.api import AbstractMessage


class Message(AbstractMessage):

    def __init__(self, handler, session_id=None,
                 client_id=None, text=None, create_on=None):

        self.handler = handler
        self.session_id = session_id
        self.client_id = client_id
        self.text = text
        self.create_on = create_on

    def reply(self, text):
        """
        send message to the client
        """
        wrapped_message = dict(
            text=text,
            session_id=self.session_id,
            client_id=self.client_id,
            create_on=str(datetime.datetime.now()),
        )

        encoded_message = json.dumps(wrapped_message)
        self.handler.send(self.client_id, encoded_message)
