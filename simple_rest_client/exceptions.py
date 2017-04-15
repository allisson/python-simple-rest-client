class ActionNotFound(Exception):
    pass


class ActionURLMatchError(Exception):
    pass


class ClientConnectionError(Exception):
    pass


class ErrorWithResponse(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response


class ClientError(ErrorWithResponse):
    pass


class ServerError(ErrorWithResponse):
    pass
