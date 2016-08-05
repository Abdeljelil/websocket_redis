import abc


class AbstractMessage(object):

    def __repr__(self):

        return "<Message client_id:{}, message:\'{}\'>".format(
            self.client_id,
            self.text
        )

    @abc.abstractmethod
    def replay(self, text):

        raise NotImplementedError("Please Implement this method")
