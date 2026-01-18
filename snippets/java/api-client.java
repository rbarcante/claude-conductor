/**
 * USE: When building a type-safe HTTP client for API communication
 * REQUIRES: Java 11+ (HttpClient), Jackson or Gson for JSON parsing
 * PATTERN: Error Handling, Configuration
 */

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

// CUSTOMIZE: Define your API response types
public record ApiResponse<T>(T data, int status, String message) {}

// CUSTOMIZE: Add your specific error codes
public enum ErrorCode {
    NETWORK_ERROR,
    TIMEOUT,
    UNAUTHORIZED,
    NOT_FOUND,
    SERVER_ERROR,
    PARSE_ERROR
}

public class ApiClientException extends RuntimeException {
    private final ErrorCode code;
    private final Integer statusCode;
    private final Map<String, Object> details;

    public ApiClientException(ErrorCode code, String message) {
        this(code, message, null, null);
    }

    public ApiClientException(ErrorCode code, String message, Integer statusCode, Map<String, Object> details) {
        super(message);
        this.code = code;
        this.statusCode = statusCode;
        this.details = details;
    }

    public ErrorCode getCode() { return code; }
    public Optional<Integer> getStatusCode() { return Optional.ofNullable(statusCode); }
    public Map<String, Object> getDetails() { return details != null ? details : Map.of(); }
}

// CUSTOMIZE: Configure for your API
public record ApiClientConfig(
    String baseUrl,
    Duration timeout,
    Map<String, String> headers
) {
    public ApiClientConfig {
        Objects.requireNonNull(baseUrl, "baseUrl cannot be null");
        timeout = timeout != null ? timeout : Duration.ofSeconds(30);
        headers = headers != null ? headers : Map.of();
    }

    public static ApiClientConfig defaultConfig() {
        return new ApiClientConfig(
            "https://api.example.com", // CUSTOMIZE: Your API base URL
            Duration.ofSeconds(30),
            Map.of("Content-Type", "application/json")
        );
    }
}

public class ApiClient {
    private final HttpClient httpClient;
    private final ApiClientConfig config;
    // CUSTOMIZE: Inject your JSON parser (Jackson ObjectMapper, Gson, etc.)
    // private final ObjectMapper objectMapper;

    public ApiClient(ApiClientConfig config) {
        this.config = Objects.requireNonNull(config, "config cannot be null");
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(config.timeout())
            .build();
    }

    public <T> CompletableFuture<ApiResponse<T>> getAsync(String endpoint, Class<T> responseType) {
        HttpRequest request = buildRequest(endpoint, "GET", null);
        return executeAsync(request, responseType);
    }

    public <T> CompletableFuture<ApiResponse<T>> postAsync(String endpoint, String body, Class<T> responseType) {
        HttpRequest request = buildRequest(endpoint, "POST", body);
        return executeAsync(request, responseType);
    }

    public <T> CompletableFuture<ApiResponse<T>> putAsync(String endpoint, String body, Class<T> responseType) {
        HttpRequest request = buildRequest(endpoint, "PUT", body);
        return executeAsync(request, responseType);
    }

    public <T> CompletableFuture<ApiResponse<T>> deleteAsync(String endpoint, Class<T> responseType) {
        HttpRequest request = buildRequest(endpoint, "DELETE", null);
        return executeAsync(request, responseType);
    }

    private HttpRequest buildRequest(String endpoint, String method, String body) {
        var builder = HttpRequest.newBuilder()
            .uri(URI.create(config.baseUrl() + endpoint))
            .timeout(config.timeout());

        // Add headers
        config.headers().forEach(builder::header);

        // Set method and body
        var bodyPublisher = body != null
            ? HttpRequest.BodyPublishers.ofString(body)
            : HttpRequest.BodyPublishers.noBody();

        return switch (method) {
            case "GET" -> builder.GET().build();
            case "POST" -> builder.POST(bodyPublisher).build();
            case "PUT" -> builder.PUT(bodyPublisher).build();
            case "DELETE" -> builder.DELETE().build();
            default -> throw new IllegalArgumentException("Unsupported method: " + method);
        };
    }

    private <T> CompletableFuture<ApiResponse<T>> executeAsync(HttpRequest request, Class<T> responseType) {
        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString())
            .thenApply(response -> handleResponse(response, responseType))
            .exceptionally(this::handleException);
    }

    private <T> ApiResponse<T> handleResponse(HttpResponse<String> response, Class<T> responseType) {
        int status = response.statusCode();

        if (status >= 200 && status < 300) {
            // CUSTOMIZE: Parse JSON response using your preferred library
            // T data = objectMapper.readValue(response.body(), responseType);
            T data = null; // Replace with actual parsing
            return new ApiResponse<>(data, status, "Success");
        }

        ErrorCode errorCode = mapStatusToErrorCode(status);
        throw new ApiClientException(errorCode, "HTTP " + status, status, null);
    }

    private <T> ApiResponse<T> handleException(Throwable ex) {
        if (ex.getCause() instanceof ApiClientException ace) {
            throw ace;
        }

        if (ex.getCause() instanceof java.net.http.HttpTimeoutException) {
            throw new ApiClientException(ErrorCode.TIMEOUT, "Request timed out");
        }

        throw new ApiClientException(
            ErrorCode.NETWORK_ERROR,
            ex.getMessage() != null ? ex.getMessage() : "Network request failed"
        );
    }

    private ErrorCode mapStatusToErrorCode(int status) {
        if (status == 401 || status == 403) return ErrorCode.UNAUTHORIZED;
        if (status == 404) return ErrorCode.NOT_FOUND;
        if (status >= 500) return ErrorCode.SERVER_ERROR;
        return ErrorCode.NETWORK_ERROR;
    }
}

// CUSTOMIZE: Example usage
// public record User(String id, String name, String email) {}
//
// var client = new ApiClient(ApiClientConfig.defaultConfig());
// client.getAsync("/users/123", User.class)
//     .thenAccept(response -> System.out.println("User: " + response.data()))
//     .exceptionally(ex -> {
//         System.err.println("Error: " + ex.getMessage());
//         return null;
//     });
