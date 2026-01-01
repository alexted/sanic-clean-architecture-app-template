from .constants import ErrorType


class OtherError(Exception):
    """Base class for custom errors"""

    type: ErrorType = ErrorType.INTERNAL_ERROR
    code: int = 500

    def __init__(self, message: str = None, code: int = None) -> None:
        """
        :param message: Error message
        :param code: HTTP status code
        """
        super().__init__(message)

        self.message = message
        self.code = code or self.code

    def __str__(self) -> str:
        """String representation of the error"""
        return f"message: {self.message}, code: {self.code}"

    @property
    def error(self) -> ErrorType:
        return self.type


class InternalError(OtherError):
    type = ErrorType.INTERNAL_ERROR


class ExternalServiceError(OtherError):
    type = ErrorType.EXTERNAL_SERVICE_ERROR


class RequestError(OtherError): ...


class BadRequestError(RequestError):
    code = 400


class NotFoundError(RequestError):
    type = ErrorType.NOT_FOUND
    code = 404


class AccessDeniedError(RequestError):
    type = ErrorType.ACCESS_DENIED
    code = 403
