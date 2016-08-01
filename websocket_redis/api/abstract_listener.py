import abc


class AbstractListener(object):

    @abc.abstractmethod
    def run(self, redis_connection, app_name):

        raise NotImplementedError("Not implemented method")

    @abc.abstractmethod
    def on_message(self, message):
        """
        overide this method for your user case
        """
        raise NotImplementedError("Not implemented method")

    @abc.abstractmethod
    def send(self, client_id, message):

        raise NotImplementedError("Not implemented method")
