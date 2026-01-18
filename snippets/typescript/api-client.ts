/**
 * USE: When building a type-safe HTTP client for API communication
 * REQUIRES: fetch API (Node.js 18+ or browser), TypeScript 4.5+
 * PATTERN: Error Handling, Configuration
 */

// CUSTOMIZE: Define your API response types
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

// CUSTOMIZE: Add your specific error codes
type ErrorCode = 'NETWORK_ERROR' | 'TIMEOUT' | 'UNAUTHORIZED' | 'NOT_FOUND' | 'SERVER_ERROR';

class ApiClientError extends Error {
  constructor(
    public readonly code: ErrorCode,
    message: string,
    public readonly statusCode?: number,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
}

// CUSTOMIZE: Configure for your API
const defaultConfig: ApiClientConfig = {
  baseUrl: 'https://api.example.com', // CUSTOMIZE: Your API base URL
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  config: ApiClientConfig = defaultConfig
): Promise<ApiResponse<T>> {
  const url = `${config.baseUrl}${endpoint}`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), config.timeout);

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...config.headers,
        ...options.headers,
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({})) as ApiError;
      throw new ApiClientError(
        mapStatusToErrorCode(response.status),
        errorBody.message || `HTTP ${response.status}`,
        response.status,
        errorBody.details
      );
    }

    const data = await response.json() as T;
    return { data, status: response.status };
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof ApiClientError) {
      throw error;
    }

    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiClientError('TIMEOUT', 'Request timed out');
    }

    throw new ApiClientError(
      'NETWORK_ERROR',
      error instanceof Error ? error.message : 'Network request failed'
    );
  }
}

function mapStatusToErrorCode(status: number): ErrorCode {
  if (status === 401 || status === 403) return 'UNAUTHORIZED';
  if (status === 404) return 'NOT_FOUND';
  if (status >= 500) return 'SERVER_ERROR';
  return 'NETWORK_ERROR';
}

// Convenience methods
export const apiClient = {
  get: <T>(endpoint: string, config?: ApiClientConfig) =>
    apiRequest<T>(endpoint, { method: 'GET' }, config),

  post: <T>(endpoint: string, body: unknown, config?: ApiClientConfig) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    }, config),

  put: <T>(endpoint: string, body: unknown, config?: ApiClientConfig) =>
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    }, config),

  delete: <T>(endpoint: string, config?: ApiClientConfig) =>
    apiRequest<T>(endpoint, { method: 'DELETE' }, config),
};

// CUSTOMIZE: Example usage
// interface User { id: string; name: string; email: string; }
// const { data: user } = await apiClient.get<User>('/users/123');
// const { data: newUser } = await apiClient.post<User>('/users', { name: 'John', email: 'john@example.com' });

export { ApiClientError, ApiClientConfig, ApiResponse, ErrorCode };
