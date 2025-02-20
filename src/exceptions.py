from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(BaseHTTPException):
    status_code = 404
    detail = "object not found"


class ObjectAlreadyExistsException(BaseHTTPException):
    status_code = 422
    detail = "object already exists"


class UserAlreadyExistsException(BaseHTTPException):
    status_code = 422
    detail = "user already exists"


class IncorrectTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "wrong token"


class EmailNotRegisteredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "user with this email not found"


class UserEmailAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "user with this email already exists"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "wrong password"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "access token not provided"
