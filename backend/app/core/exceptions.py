class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "APP_ERROR",
        status_code: int = 400,
        detail: dict | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found", **kwargs) -> None:
        super().__init__(message, code="NOT_FOUND", status_code=404, **kwargs)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized", **kwargs) -> None:
        super().__init__(message, code="UNAUTHORIZED", status_code=401, **kwargs)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden", **kwargs) -> None:
        super().__init__(message, code="FORBIDDEN", status_code=403, **kwargs)


class ConflictError(AppException):
    def __init__(self, message: str = "Conflict", **kwargs) -> None:
        super().__init__(message, code="CONFLICT", status_code=409, **kwargs)
