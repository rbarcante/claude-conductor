"""
USE: When implementing async operations with proper error handling and concurrency
REQUIRES: Python 3.10+, asyncio
PATTERN: Error Handling, Resilience
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


# Result type for explicit error handling


@dataclass
class Success(Generic[T]):
    """Successful result."""
    value: T

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False


@dataclass
class Failure:
    """Failed result."""
    error: Exception

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True


Result = Success[T] | Failure


class TimeoutError(Exception):
    """Operation timed out."""
    def __init__(self, timeout: float):
        super().__init__(f"Operation timed out after {timeout}s")
        self.timeout = timeout


class RetryExhaustedError(Exception):
    """All retry attempts exhausted."""
    def __init__(self, attempts: int, last_error: Exception):
        super().__init__(f"All {attempts} retry attempts exhausted")
        self.attempts = attempts
        self.last_error = last_error


# Retry configuration


@dataclass
class RetryConfig:
    """Retry behavior configuration."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True


def _calculate_delay(attempt: int, config: RetryConfig) -> float:
    """Calculate delay with exponential backoff and optional jitter."""
    import random

    delay = min(
        config.base_delay * (config.exponential_base ** (attempt - 1)),
        config.max_delay,
    )

    if config.jitter:
        delay = delay * (0.5 + random.random())

    return delay


# CUSTOMIZE: Define which errors are retryable


def is_retryable(error: Exception) -> bool:
    """Determine if an error should trigger a retry."""
    # Network errors
    if isinstance(error, (ConnectionError, TimeoutError, asyncio.TimeoutError)):
        return True

    # CUSTOMIZE: Add your retryable error types
    # if isinstance(error, SomeApiError) and error.status in (429, 503):
    #     return True

    return False


# Core async utilities


async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
) -> T:
    """
    Execute coroutine with timeout.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds

    Returns:
        Result of the coroutine

    Raises:
        TimeoutError: If operation times out
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError as e:
        raise TimeoutError(timeout) from e


async def with_retry(
    operation: Callable[[], Awaitable[T]],
    config: RetryConfig | None = None,
    on_retry: Callable[[int, Exception, float], None] | None = None,
) -> T:
    """
    Execute async operation with retry logic.

    Args:
        operation: Async function to execute
        config: Retry configuration
        on_retry: Callback on each retry (attempt, error, delay)

    Returns:
        Result of the operation

    Raises:
        RetryExhaustedError: If all retries fail
    """
    config = config or RetryConfig()
    last_error: Exception = Exception("No attempts made")

    for attempt in range(1, config.max_attempts + 1):
        try:
            return await operation()
        except Exception as e:
            last_error = e

            if attempt == config.max_attempts or not is_retryable(e):
                raise

            delay = _calculate_delay(attempt, config)

            if on_retry:
                on_retry(attempt, e, delay)

            await asyncio.sleep(delay)

    raise RetryExhaustedError(config.max_attempts, last_error)


async def try_async(
    operation: Callable[[], Awaitable[T]],
) -> Result[T]:
    """
    Execute async operation and return Result instead of raising.

    Args:
        operation: Async function to execute

    Returns:
        Success with value or Failure with error
    """
    try:
        value = await operation()
        return Success(value)
    except Exception as e:
        return Failure(e)


# Concurrency utilities


async def gather_with_concurrency(
    tasks: list[Callable[[], Awaitable[T]]],
    max_concurrency: int = 10,
) -> list[T]:
    """
    Execute tasks with limited concurrency.

    Args:
        tasks: List of async functions to execute
        max_concurrency: Maximum concurrent executions

    Returns:
        List of results in same order as tasks
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    results: list[T] = []

    async def limited_task(index: int, task: Callable[[], Awaitable[T]]) -> tuple[int, T]:
        async with semaphore:
            result = await task()
            return (index, result)

    completed = await asyncio.gather(
        *[limited_task(i, task) for i, task in enumerate(tasks)]
    )

    # Sort by original index
    sorted_results = sorted(completed, key=lambda x: x[0])
    return [result for _, result in sorted_results]


async def gather_with_errors(
    tasks: list[Callable[[], Awaitable[T]]],
    max_concurrency: int = 10,
) -> list[Result[T]]:
    """
    Execute tasks with limited concurrency, capturing errors.

    Args:
        tasks: List of async functions to execute
        max_concurrency: Maximum concurrent executions

    Returns:
        List of Results (Success or Failure) in same order as tasks
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def limited_task(index: int, task: Callable[[], Awaitable[T]]) -> tuple[int, Result[T]]:
        async with semaphore:
            result = await try_async(task)
            return (index, result)

    completed = await asyncio.gather(
        *[limited_task(i, task) for i, task in enumerate(tasks)]
    )

    sorted_results = sorted(completed, key=lambda x: x[0])
    return [result for _, result in sorted_results]


async def first_completed(
    tasks: list[Callable[[], Awaitable[T]]],
    timeout: float | None = None,
) -> T:
    """
    Return result of first completed task, cancel others.

    Args:
        tasks: List of async functions to race
        timeout: Optional timeout for all tasks

    Returns:
        Result of first completed task

    Raises:
        TimeoutError: If timeout exceeded before any task completes
        Exception: If all tasks fail
    """
    pending = {asyncio.create_task(task()) for task in tasks}

    try:
        done, pending = await asyncio.wait(
            pending,
            timeout=timeout,
            return_when=asyncio.FIRST_COMPLETED,
        )

        if not done:
            raise TimeoutError(timeout or 0)

        # Cancel remaining tasks
        for task in pending:
            task.cancel()

        # Return first completed result
        completed_task = done.pop()
        return completed_task.result()

    finally:
        # Ensure all pending tasks are cancelled
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


# CUSTOMIZE: Example usage
# async def fetch_user(user_id: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"/users/{user_id}")
#         return response.json()
#
# async def main():
#     # With retry
#     user = await with_retry(
#         lambda: fetch_user("123"),
#         config=RetryConfig(max_attempts=3),
#         on_retry=lambda attempt, err, delay: print(f"Retry {attempt}: {err}"),
#     )
#
#     # With timeout
#     user = await with_timeout(fetch_user("123"), timeout=5.0)
#
#     # Batch with concurrency
#     user_ids = ["1", "2", "3", "4", "5"]
#     users = await gather_with_concurrency(
#         [lambda uid=uid: fetch_user(uid) for uid in user_ids],
#         max_concurrency=3,
#     )
#
#     # With error handling
#     results = await gather_with_errors(
#         [lambda uid=uid: fetch_user(uid) for uid in user_ids],
#     )
#     for result in results:
#         if result.is_success:
#             print(f"Got user: {result.value}")
#         else:
#             print(f"Failed: {result.error}")
