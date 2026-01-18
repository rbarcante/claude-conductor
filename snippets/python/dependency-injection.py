"""
USE: When implementing dependency injection for testable, loosely-coupled code
REQUIRES: Python 3.10+
PATTERN: Configuration
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


class Lifecycle(Enum):
    """Dependency lifecycle options."""
    TRANSIENT = auto()  # New instance every time
    SINGLETON = auto()  # Single shared instance
    SCOPED = auto()      # One instance per scope (e.g., request)


@dataclass
class Registration(Generic[T]):
    """Dependency registration metadata."""
    factory: Callable[["Container"], T]
    lifecycle: Lifecycle
    instance: T | None = None


class ContainerError(Exception):
    """Dependency injection error."""
    pass


class Container:
    """
    Simple dependency injection container.

    Supports constructor injection with lifecycle management.
    """

    def __init__(self) -> None:
        self._registrations: dict[type, Registration[Any]] = {}
        self._scoped_instances: dict[type, Any] = {}
        self._in_scope: bool = False

    def register(
        self,
        interface: type[T],
        factory: Callable[["Container"], T],
        lifecycle: Lifecycle = Lifecycle.TRANSIENT,
    ) -> "Container":
        """
        Register a dependency.

        Args:
            interface: The type/interface to register
            factory: Factory function that creates the instance
            lifecycle: Instance lifecycle (transient, singleton, scoped)

        Returns:
            Self for method chaining
        """
        self._registrations[interface] = Registration(
            factory=factory,
            lifecycle=lifecycle,
        )
        return self

    def register_instance(self, interface: type[T], instance: T) -> "Container":
        """Register an existing instance as singleton."""
        self._registrations[interface] = Registration(
            factory=lambda _: instance,
            lifecycle=Lifecycle.SINGLETON,
            instance=instance,
        )
        return self

    def register_transient(
        self,
        interface: type[T],
        factory: Callable[["Container"], T],
    ) -> "Container":
        """Register a transient dependency (new instance each time)."""
        return self.register(interface, factory, Lifecycle.TRANSIENT)

    def register_singleton(
        self,
        interface: type[T],
        factory: Callable[["Container"], T],
    ) -> "Container":
        """Register a singleton dependency (shared instance)."""
        return self.register(interface, factory, Lifecycle.SINGLETON)

    def register_scoped(
        self,
        interface: type[T],
        factory: Callable[["Container"], T],
    ) -> "Container":
        """Register a scoped dependency (one per scope)."""
        return self.register(interface, factory, Lifecycle.SCOPED)

    def resolve(self, interface: type[T]) -> T:
        """
        Resolve a dependency.

        Args:
            interface: The type/interface to resolve

        Returns:
            Instance of the requested type

        Raises:
            ContainerError: If dependency is not registered
        """
        if interface not in self._registrations:
            raise ContainerError(f"No registration found for {interface.__name__}")

        registration = self._registrations[interface]

        # Handle singleton
        if registration.lifecycle == Lifecycle.SINGLETON:
            if registration.instance is None:
                registration.instance = registration.factory(self)
            return registration.instance

        # Handle scoped
        if registration.lifecycle == Lifecycle.SCOPED:
            if not self._in_scope:
                raise ContainerError(
                    f"Cannot resolve scoped dependency {interface.__name__} outside of scope"
                )
            if interface not in self._scoped_instances:
                self._scoped_instances[interface] = registration.factory(self)
            return self._scoped_instances[interface]

        # Transient - always create new
        return registration.factory(self)

    def create_scope(self) -> "ContainerScope":
        """Create a new scope for scoped dependencies."""
        return ContainerScope(self)

    def _begin_scope(self) -> None:
        """Begin a new scope."""
        self._in_scope = True
        self._scoped_instances.clear()

    def _end_scope(self) -> None:
        """End the current scope."""
        self._in_scope = False
        self._scoped_instances.clear()


class ContainerScope:
    """Context manager for scoped dependencies."""

    def __init__(self, container: Container):
        self._container = container

    def __enter__(self) -> Container:
        self._container._begin_scope()
        return self._container

    def __exit__(self, *args: Any) -> None:
        self._container._end_scope()


# CUSTOMIZE: Define your interfaces and implementations


class ILogger(ABC):
    """Logger interface."""

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str, error: Exception | None = None) -> None:
        pass


class IUserRepository(ABC):
    """User repository interface."""

    @abstractmethod
    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def save(self, user: dict[str, Any]) -> None:
        pass


class IEmailService(ABC):
    """Email service interface."""

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> bool:
        pass


# CUSTOMIZE: Implement your dependencies


class ConsoleLogger(ILogger):
    """Simple console logger implementation."""

    def info(self, message: str) -> None:
        print(f"[INFO] {message}")

    def error(self, message: str, error: Exception | None = None) -> None:
        print(f"[ERROR] {message}")
        if error:
            print(f"  Exception: {error}")


class InMemoryUserRepository(IUserRepository):
    """In-memory user repository for testing."""

    def __init__(self) -> None:
        self._users: dict[str, dict[str, Any]] = {}

    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self._users.get(user_id)

    def save(self, user: dict[str, Any]) -> None:
        self._users[user["id"]] = user


@dataclass
class UserService:
    """Example service using injected dependencies."""
    repository: IUserRepository
    logger: ILogger
    email_service: IEmailService

    def create_user(self, name: str, email: str) -> dict[str, Any]:
        user = {"id": f"user_{name}", "name": name, "email": email}
        self.repository.save(user)
        self.logger.info(f"Created user: {name}")
        self.email_service.send(email, "Welcome!", f"Hello {name}!")
        return user


# CUSTOMIZE: Configure your container


def configure_container() -> Container:
    """Configure dependency injection container."""
    container = Container()

    # Register dependencies
    container.register_singleton(ILogger, lambda c: ConsoleLogger())
    container.register_singleton(IUserRepository, lambda c: InMemoryUserRepository())

    # CUSTOMIZE: Replace with real implementation
    # container.register_singleton(IEmailService, lambda c: SmtpEmailService(c.resolve(ILogger)))

    # Register services that depend on other services
    container.register_transient(
        UserService,
        lambda c: UserService(
            repository=c.resolve(IUserRepository),
            logger=c.resolve(ILogger),
            email_service=c.resolve(IEmailService),
        ),
    )

    return container


# CUSTOMIZE: Example usage
# container = configure_container()
# user_service = container.resolve(UserService)
# user = user_service.create_user("Alice", "alice@example.com")
#
# # Using scopes (e.g., per-request in web apps)
# with container.create_scope() as scoped:
#     request_service = scoped.resolve(RequestScopedService)
