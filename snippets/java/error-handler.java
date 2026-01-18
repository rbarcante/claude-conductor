/**
 * USE: When building a custom exception hierarchy with error codes and context
 * REQUIRES: Java 17+ (records, sealed classes)
 * PATTERN: Error Handling
 */

import java.time.Instant;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

// CUSTOMIZE: Add your specific error codes
public enum ErrorCode {
    // Client errors (4xx equivalent)
    VALIDATION_ERROR("E4001", "Validation failed"),
    NOT_FOUND("E4004", "Resource not found"),
    UNAUTHORIZED("E4010", "Authentication required"),
    FORBIDDEN("E4030", "Access denied"),
    CONFLICT("E4090", "Resource conflict"),

    // Server errors (5xx equivalent)
    INTERNAL_ERROR("E5000", "Internal server error"),
    SERVICE_UNAVAILABLE("E5003", "Service temporarily unavailable"),
    TIMEOUT("E5040", "Operation timed out"),

    // Domain-specific errors (customize these)
    INSUFFICIENT_FUNDS("E6001", "Insufficient funds"),
    INVALID_STATE("E6002", "Invalid state transition"),
    RATE_LIMITED("E6003", "Rate limit exceeded");

    private final String code;
    private final String defaultMessage;

    ErrorCode(String code, String defaultMessage) {
        this.code = code;
        this.defaultMessage = defaultMessage;
    }

    public String getCode() { return code; }
    public String getDefaultMessage() { return defaultMessage; }
}

// Structured error details for API responses
public record ErrorDetails(
    String errorId,
    String code,
    String message,
    Instant timestamp,
    String path,
    Map<String, Object> context
) {
    public ErrorDetails {
        Objects.requireNonNull(code, "code cannot be null");
        Objects.requireNonNull(message, "message cannot be null");
        errorId = errorId != null ? errorId : UUID.randomUUID().toString();
        timestamp = timestamp != null ? timestamp : Instant.now();
        context = context != null ? context : Map.of();
    }

    public static ErrorDetails of(ErrorCode errorCode, String message) {
        return new ErrorDetails(null, errorCode.getCode(), message, null, null, null);
    }

    public static ErrorDetails of(ErrorCode errorCode) {
        return of(errorCode, errorCode.getDefaultMessage());
    }

    public ErrorDetails withPath(String path) {
        return new ErrorDetails(errorId, code, message, timestamp, path, context);
    }

    public ErrorDetails withContext(Map<String, Object> context) {
        return new ErrorDetails(errorId, code, message, timestamp, path, context);
    }
}

// Base exception with error details
public class ApplicationException extends RuntimeException {
    private final ErrorCode errorCode;
    private final ErrorDetails details;

    public ApplicationException(ErrorCode errorCode, String message) {
        this(errorCode, message, null, null);
    }

    public ApplicationException(ErrorCode errorCode, String message, Throwable cause) {
        this(errorCode, message, cause, null);
    }

    public ApplicationException(ErrorCode errorCode, String message, Throwable cause, Map<String, Object> context) {
        super(message, cause);
        this.errorCode = Objects.requireNonNull(errorCode, "errorCode cannot be null");
        this.details = new ErrorDetails(
            null,
            errorCode.getCode(),
            message != null ? message : errorCode.getDefaultMessage(),
            null,
            null,
            context
        );
    }

    public ErrorCode getErrorCode() { return errorCode; }
    public ErrorDetails getDetails() { return details; }

    public ApplicationException withContext(Map<String, Object> context) {
        return new ApplicationException(errorCode, getMessage(), getCause(), context);
    }
}

// CUSTOMIZE: Domain-specific exceptions
public class ValidationException extends ApplicationException {
    private final Map<String, String> fieldErrors;

    public ValidationException(String message, Map<String, String> fieldErrors) {
        super(ErrorCode.VALIDATION_ERROR, message, null, Map.of("fieldErrors", fieldErrors));
        this.fieldErrors = fieldErrors;
    }

    public Map<String, String> getFieldErrors() { return fieldErrors; }
}

public class NotFoundException extends ApplicationException {
    private final String resourceType;
    private final String resourceId;

    public NotFoundException(String resourceType, String resourceId) {
        super(
            ErrorCode.NOT_FOUND,
            String.format("%s not found: %s", resourceType, resourceId),
            null,
            Map.of("resourceType", resourceType, "resourceId", resourceId)
        );
        this.resourceType = resourceType;
        this.resourceId = resourceId;
    }

    public String getResourceType() { return resourceType; }
    public String getResourceId() { return resourceId; }
}

public class UnauthorizedException extends ApplicationException {
    public UnauthorizedException(String message) {
        super(ErrorCode.UNAUTHORIZED, message);
    }

    public UnauthorizedException() {
        this("Authentication required");
    }
}

public class ForbiddenException extends ApplicationException {
    private final String requiredPermission;

    public ForbiddenException(String message, String requiredPermission) {
        super(ErrorCode.FORBIDDEN, message, null, Map.of("requiredPermission", requiredPermission));
        this.requiredPermission = requiredPermission;
    }

    public Optional<String> getRequiredPermission() {
        return Optional.ofNullable(requiredPermission);
    }
}

// Global exception handler (for Spring/Jakarta EE)
// CUSTOMIZE: Adapt to your framework
/*
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ErrorDetails> handleApplicationException(
            ApplicationException ex,
            HttpServletRequest request) {

        ErrorDetails details = ex.getDetails().withPath(request.getRequestURI());

        HttpStatus status = switch (ex.getErrorCode()) {
            case VALIDATION_ERROR -> HttpStatus.BAD_REQUEST;
            case NOT_FOUND -> HttpStatus.NOT_FOUND;
            case UNAUTHORIZED -> HttpStatus.UNAUTHORIZED;
            case FORBIDDEN -> HttpStatus.FORBIDDEN;
            case CONFLICT -> HttpStatus.CONFLICT;
            case RATE_LIMITED -> HttpStatus.TOO_MANY_REQUESTS;
            default -> HttpStatus.INTERNAL_SERVER_ERROR;
        };

        return ResponseEntity.status(status).body(details);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorDetails> handleGenericException(
            Exception ex,
            HttpServletRequest request) {

        // Log the full stack trace for internal errors
        log.error("Unhandled exception", ex);

        ErrorDetails details = ErrorDetails.of(ErrorCode.INTERNAL_ERROR)
            .withPath(request.getRequestURI());

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(details);
    }
}
*/

// CUSTOMIZE: Example usage
// throw new NotFoundException("User", "123");
// throw new ValidationException("Invalid input", Map.of("email", "Invalid email format"));
// throw new ApplicationException(ErrorCode.INSUFFICIENT_FUNDS, "Cannot complete transaction")
//     .withContext(Map.of("accountId", accountId, "requested", amount));
