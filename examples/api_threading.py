import datetime

from websocket_redis.api.threading import APIClientListener


class MyAPIClientListener(APIClientListener):

    def on_message(self, message):

        print("new message {}".format(message.text))
        new_massage = "thread hi, {} , {}".format(
            message.client_id,
            datetime.datetime.now()
        )

        message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        host="localhost",
        port=6379
    )
    handler = MyAPIClientListener(redis_connection, app_name="test_app")

    handler.run()
