---
use: When object creation logic is complex or varies based on configuration/input
requires: Understanding of polymorphism in your language
pattern: Configuration
---

# Factory Pattern

Encapsulates object creation logic, providing a consistent interface while hiding instantiation complexity.

## AI Quick Reference

### When to Apply
- Object creation requires complex setup or configuration
- The specific class to instantiate depends on runtime conditions
- You want to centralize and standardize object creation
- Construction parameters come from external configuration

### Factory Types
| Type | Use Case |
|------|----------|
| **Simple Factory** | Single method creates different types based on input |
| **Factory Method** | Subclasses decide which class to instantiate |
| **Abstract Factory** | Create families of related objects |
| **Builder** | Step-by-step construction of complex objects |

### Key Benefits
- Decouples client code from concrete classes
- Centralizes creation logic for consistency
- Enables easy testing with mock factories
- Supports open/closed principle (add types without modifying client)

---

## Simple Factory (TypeScript)

```typescript
// Product interface
interface Logger {
  log(message: string): void;
}

// Concrete implementations
class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(`[CONSOLE] ${message}`);
  }
}

class FileLogger implements Logger {
  constructor(private filepath: string) {}
  log(message: string): void {
    // Write to file
    console.log(`[FILE:${this.filepath}] ${message}`);
  }
}

class RemoteLogger implements Logger {
  constructor(private endpoint: string) {}
  log(message: string): void {
    // Send to remote service
    console.log(`[REMOTE:${this.endpoint}] ${message}`);
  }
}

// CUSTOMIZE: Add your logger types
type LoggerType = 'console' | 'file' | 'remote';

interface LoggerConfig {
  type: LoggerType;
  filepath?: string;
  endpoint?: string;
}

// Factory
class LoggerFactory {
  static create(config: LoggerConfig): Logger {
    switch (config.type) {
      case 'console':
        return new ConsoleLogger();
      case 'file':
        if (!config.filepath) {
          throw new Error('filepath required for file logger');
        }
        return new FileLogger(config.filepath);
      case 'remote':
        if (!config.endpoint) {
          throw new Error('endpoint required for remote logger');
        }
        return new RemoteLogger(config.endpoint);
      default:
        throw new Error(`Unknown logger type: ${config.type}`);
    }
  }
}

// Usage
const logger = LoggerFactory.create({ type: 'console' });
logger.log('Hello, world!');
```

## Factory Method (TypeScript)

```typescript
// Product interface
interface Notification {
  send(recipient: string, message: string): Promise<void>;
}

// Abstract creator
abstract class NotificationService {
  // Factory method - subclasses implement
  protected abstract createNotification(): Notification;

  // Template method using the factory
  async notify(recipient: string, message: string): Promise<void> {
    const notification = this.createNotification();
    await notification.send(recipient, message);
    console.log(`Notification sent to ${recipient}`);
  }
}

// Concrete products
class EmailNotification implements Notification {
  async send(recipient: string, message: string): Promise<void> {
    console.log(`Email to ${recipient}: ${message}`);
  }
}

class SmsNotification implements Notification {
  async send(recipient: string, message: string): Promise<void> {
    console.log(`SMS to ${recipient}: ${message}`);
  }
}

// Concrete creators
class EmailNotificationService extends NotificationService {
  protected createNotification(): Notification {
    return new EmailNotification();
  }
}

class SmsNotificationService extends NotificationService {
  protected createNotification(): Notification {
    return new SmsNotification();
  }
}

// Usage
const emailService = new EmailNotificationService();
await emailService.notify('user@example.com', 'Hello!');
```

## Abstract Factory (Python)

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Abstract products
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# Concrete products - Light theme
class LightButton(Button):
    def render(self) -> str:
        return "<button class='light'>Click me</button>"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "<input type='checkbox' class='light'/>"


# Concrete products - Dark theme
class DarkButton(Button):
    def render(self) -> str:
        return "<button class='dark'>Click me</button>"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "<input type='checkbox' class='dark'/>"


# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass


# Concrete factories
class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


# CUSTOMIZE: Factory selection
def get_ui_factory(theme: str) -> UIFactory:
    factories = {
        "light": LightThemeFactory,
        "dark": DarkThemeFactory,
    }
    factory_class = factories.get(theme)
    if not factory_class:
        raise ValueError(f"Unknown theme: {theme}")
    return factory_class()


# Usage - client code works with any theme
def render_ui(factory: UIFactory) -> str:
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    return f"{button.render()}\n{checkbox.render()}"


# Switch themes without changing client code
light_ui = render_ui(get_ui_factory("light"))
dark_ui = render_ui(get_ui_factory("dark"))
```

## Builder Pattern (Python)

```python
from dataclasses import dataclass, field
from typing import Self


@dataclass
class HttpRequest:
    """Complex object built step by step."""
    method: str = "GET"
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    query_params: dict[str, str] = field(default_factory=dict)
    body: str | None = None
    timeout: int = 30


class HttpRequestBuilder:
    """Builder for HttpRequest with fluent interface."""

    def __init__(self):
        self._request = HttpRequest()

    def method(self, method: str) -> Self:
        self._request.method = method
        return self

    def url(self, url: str) -> Self:
        self._request.url = url
        return self

    def header(self, key: str, value: str) -> Self:
        self._request.headers[key] = value
        return self

    def query(self, key: str, value: str) -> Self:
        self._request.query_params[key] = value
        return self

    def body(self, body: str) -> Self:
        self._request.body = body
        return self

    def timeout(self, seconds: int) -> Self:
        self._request.timeout = seconds
        return self

    def build(self) -> HttpRequest:
        if not self._request.url:
            raise ValueError("URL is required")
        return self._request


# Usage - readable, step-by-step construction
request = (
    HttpRequestBuilder()
    .method("POST")
    .url("https://api.example.com/users")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer token")
    .body('{"name": "John"}')
    .timeout(60)
    .build()
)
```

## Best Practices

1. **Use factory when** - Creation logic is complex or conditional
2. **Prefer composition** - Inject factories rather than hardcoding
3. **Name clearly** - `createX()`, `buildX()`, `XFactory`
4. **Validate early** - Check required parameters in factory
5. **Keep factories simple** - If factory is complex, consider builder
