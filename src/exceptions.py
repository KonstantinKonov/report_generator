from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(BaseHTTPException):
    status_code = 404
    detail = "object not found"


class ObjectAlreadyExistsException(BaseException):
    status_code = 422
    detail = "object already exists"