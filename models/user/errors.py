class UserError(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectPasswordError(UserError):
    pass


class UserNotFoundError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass