"""
USE: When building a type-safe HTTP client for API communication
REQUIRES: httpx>=0.24, Python 3.10+
PATTERN: Error Handling, Configuration
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar
import httpx

T = TypeVar("T")


class ErrorCode(str, Enum):
    """API error codes for programmatic handling."""
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT = "TIMEOUT"
    UNAUTHORIZED = "UNAUTHORIZED"
    NOT_FOUND = "NOT_FOUND"
    SERVER_ERROR = "SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


@dataclass
class ApiError(Exception):
    """Structured API error with context."""
    code: ErrorCode
    message: str
    status_code: int | None = None
    details: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


@dataclass
class ApiResponse(Generic[T]):
    """Typed API response wrapper."""
    data: T
    status_code: int
    headers: dict[str, str] = field(default_factory=dict)


@dataclass
class ApiClientConfig:
    """API client configuration."""
    # CUSTOMIZE: Set your API base URL
    base_url: str = "https://api.example.com"
    timeout: float = 30.0
    max_retries: int = 3
    headers: dict[str, str] = field(default_factory=lambda: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    })


def _map_status_to_error_code(status: int) -> ErrorCode:
    """Map HTTP status to error code."""
    if status == 401 or status == 403:
        return ErrorCode.UNAUTHORIZED
    if status == 404:
        return ErrorCode.NOT_FOUND
    if status == 422:
        return ErrorCode.VALIDATION_ERROR
    if status >= 500:
        return ErrorCode.SERVER_ERROR
    return ErrorCode.NETWORK_ERROR


class ApiClient:
    """Type-safe HTTP client with retry and error handling."""

    def __init__(self, config: ApiClientConfig | None = None):
        self.config = config or ApiClientConfig()
        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            headers=self.config.headers,
        )

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle response and raise ApiError on failure."""
        if response.is_success:
            return response.json() if response.content else {}

        try:
            error_body = response.json()
            message = error_body.get("message", f"HTTP {response.status_code}")
            details = error_body.get("details")
        except Exception:
            message = f"HTTP {response.status_code}"
            details = None

        raise ApiError(
            code=_map_status_to_error_code(response.status_code),
            message=message,
            status_code=response.status_code,
            details=details,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute request with retry logic."""
        last_error: Exception | None = None

        for attempt in range(self.config.max_retries):
            try:
                response = self._client.request(method, endpoint, **kwargs)
                return self._handle_response(response)
            except httpx.TimeoutException as e:
                last_error = ApiError(
                    code=ErrorCode.TIMEOUT,
                    message=f"Request timed out after {self.config.timeout}s",
                )
                if attempt == self.config.max_retries - 1:
                    raise last_error from e
            except httpx.NetworkError as e:
                last_error = ApiError(
                    code=ErrorCode.NETWORK_ERROR,
                    message=str(e),
                )
                if attempt == self.config.max_retries - 1:
                    raise last_error from e
            except ApiError:
                raise

        raise last_error or ApiError(
            code=ErrorCode.NETWORK_ERROR,
            message="Request failed after retries",
        )

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """GET request."""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """POST request with JSON body."""
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """PUT request with JSON body."""
        return self._request("PUT", endpoint, json=json)

    def patch(self, endpoint: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """PATCH request with JSON body."""
        return self._request("PATCH", endpoint, json=json)

    def delete(self, endpoint: str) -> dict[str, Any]:
        """DELETE request."""
        return self._request("DELETE", endpoint)


# CUSTOMIZE: Example usage
# @dataclass
# class User:
#     id: str
#     name: str
#     email: str
#
# with ApiClient() as client:
#     try:
#         data = client.get("/users/123")
#         user = User(**data)
#     except ApiError as e:
#         print(f"Failed: {e.code} - {e.message}")
