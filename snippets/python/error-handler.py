"""
USE: When implementing structured error handling with custom exception hierarchy
REQUIRES: Python 3.10+
PATTERN: Error Handling
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import logging
import traceback

logger = logging.getLogger(__name__)


@dataclass
class AppError(Exception):
    """Base application error with structured context."""
    code: str
    message: str
    user_message: str
    status_code: int = 500
    context: dict[str, Any] = field(default_factory=dict)
    cause: Exception | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str | None = None

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for logging/serialization."""
        return {
            "code": self.code,
            "message": self.message,
            "user_message": self.user_message,
            "status_code": self.status_code,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id,
        }


# CUSTOMIZE: Add domain-specific error types


@dataclass
class ValidationError(AppError):
    """Input validation failed."""
    field: str = ""
    value: Any = None

    def __post_init__(self) -> None:
        self.code = "VALIDATION_ERROR"
        self.status_code = 400
        self.context = {"field": self.field, "value": self.value}
        if not self.user_message:
            self.user_message = f"Invalid value for {self.field}"


@dataclass
class NotFoundError(AppError):
    """Resource not found."""
    resource: str = ""
    resource_id: str | int = ""

    def __post_init__(self) -> None:
        self.code = "NOT_FOUND"
        self.status_code = 404
        self.message = f"{self.resource} with id {self.resource_id} not found"
        self.user_message = f"{self.resource} not found"
        self.context = {"resource": self.resource, "id": self.resource_id}


@dataclass
class UnauthorizedError(AppError):
    """Authentication required or failed."""

    def __post_init__(self) -> None:
        self.code = "UNAUTHORIZED"
        self.status_code = 401
        if not self.message:
            self.message = "Authentication required"
        if not self.user_message:
            self.user_message = "Please log in to continue"


@dataclass
class ForbiddenError(AppError):
    """Permission denied."""
    action: str = ""
    resource: str | None = None

    def __post_init__(self) -> None:
        self.code = "FORBIDDEN"
        self.status_code = 403
        resource_msg = f" on {self.resource}" if self.resource else ""
        self.message = f"Not permitted to {self.action}{resource_msg}"
        self.user_message = "You do not have permission to perform this action"
        self.context = {"action": self.action, "resource": self.resource}


@dataclass
class ConflictError(AppError):
    """Operation conflicts with existing state."""

    def __post_init__(self) -> None:
        self.code = "CONFLICT"
        self.status_code = 409
        if not self.user_message:
            self.user_message = "This operation conflicts with existing data"


@dataclass
class RateLimitError(AppError):
    """Rate limit exceeded."""
    retry_after: int = 60

    def __post_init__(self) -> None:
        self.code = "RATE_LIMITED"
        self.status_code = 429
        self.message = f"Rate limit exceeded. Retry after {self.retry_after}s"
        self.user_message = "Too many requests. Please try again later."
        self.context = {"retry_after": self.retry_after}


def is_app_error(error: Exception) -> bool:
    """Type guard for AppError."""
    return isinstance(error, AppError)


@dataclass
class ErrorResponse:
    """Standardized error response for APIs."""
    code: str
    message: str
    request_id: str | None = None


def handle_error(
    error: Exception,
    request_id: str | None = None,
) -> tuple[int, dict[str, Any]]:
    """
    Handle error and return (status_code, response_body).

    Logs full error details and returns safe response for users.
    """
    # Log full error details
    log_context = {
        "request_id": request_id,
        "error_type": type(error).__name__,
        "error_message": str(error),
    }

    if is_app_error(error):
        app_error: AppError = error  # type: ignore
        log_context.update(app_error.to_dict())
        logger.error("Application error", extra=log_context)

        return app_error.status_code, {
            "error": {
                "code": app_error.code,
                "message": app_error.user_message,
                "request_id": request_id,
            }
        }

    # Unknown error - log full traceback, return generic message
    log_context["traceback"] = traceback.format_exc()
    logger.exception("Unexpected error", extra=log_context)

    return 500, {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "request_id": request_id,
        }
    }


def wrap_error(
    error: Exception,
    code: str = "INTERNAL_ERROR",
    user_message: str = "An unexpected error occurred",
) -> AppError:
    """Wrap a non-AppError exception in an AppError."""
    if is_app_error(error):
        return error  # type: ignore

    return AppError(
        code=code,
        message=str(error),
        user_message=user_message,
        cause=error,
    )


# CUSTOMIZE: Example usage with FastAPI
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
#
# app = FastAPI()
#
# @app.exception_handler(AppError)
# async def app_error_handler(request: Request, error: AppError):
#     status_code, body = handle_error(error, request.state.request_id)
#     return JSONResponse(status_code=status_code, content=body)
#
# @app.exception_handler(Exception)
# async def generic_error_handler(request: Request, error: Exception):
#     status_code, body = handle_error(error, request.state.request_id)
#     return JSONResponse(status_code=status_code, content=body)
