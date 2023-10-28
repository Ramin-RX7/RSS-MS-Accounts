from schemas import Error as ErrorScheme


class BaseError:
    message = ""
    def __new__(cls, message=None):
        return ErrorScheme(
            type = cls.__name__,
            message = message or cls.message
        )


class InvalidCredentials(BaseError):
    message = "Invalid Credentials has been given"

class UserAlreadyExists(BaseError):
    message = "User with similar username/email already exists"
