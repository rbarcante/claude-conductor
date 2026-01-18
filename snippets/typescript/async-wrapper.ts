/**
 * USE: When executing async operations with retry logic, timeout, and error handling
 * REQUIRES: TypeScript 4.5+
 * PATTERN: Error Handling, Resilience
 */

interface RetryOptions {
  maxAttempts: number;
  baseDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  jitter: boolean;
}

interface TimeoutOptions {
  timeoutMs: number;
  timeoutError?: Error;
}

interface AsyncWrapperOptions {
  retry?: Partial<RetryOptions>;
  timeout?: TimeoutOptions;
  onRetry?: (attempt: number, error: Error, delayMs: number) => void;
}

// CUSTOMIZE: Default retry configuration
const defaultRetryOptions: RetryOptions = {
  maxAttempts: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
  jitter: true,
};

class TimeoutError extends Error {
  constructor(timeoutMs: number) {
    super(`Operation timed out after ${timeoutMs}ms`);
    this.name = 'TimeoutError';
  }
}

class RetryExhaustedError extends Error {
  constructor(
    public readonly attempts: number,
    public readonly lastError: Error
  ) {
    super(`All ${attempts} retry attempts exhausted`);
    this.name = 'RetryExhaustedError';
  }
}

// Calculate delay with exponential backoff and optional jitter
function calculateDelay(
  attempt: number,
  options: RetryOptions
): number {
  const exponentialDelay = options.baseDelayMs * Math.pow(options.backoffMultiplier, attempt - 1);
  const boundedDelay = Math.min(exponentialDelay, options.maxDelayMs);

  if (options.jitter) {
    // Add random jitter: 0-25% of the delay
    const jitterRange = boundedDelay * 0.25;
    return boundedDelay + Math.random() * jitterRange;
  }

  return boundedDelay;
}

// Sleep utility
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Wrap a promise with timeout
async function withTimeout<T>(
  promise: Promise<T>,
  options: TimeoutOptions
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(options.timeoutError ?? new TimeoutError(options.timeoutMs));
    }, options.timeoutMs);
  });

  return Promise.race([promise, timeoutPromise]);
}

// CUSTOMIZE: Define which errors are retryable
function isRetryableError(error: unknown): boolean {
  if (error instanceof Error) {
    // Network errors
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return true;
    }
    // Timeout errors are retryable
    if (error instanceof TimeoutError) {
      return true;
    }
    // CUSTOMIZE: Add your retryable error conditions
    // Example: HTTP 429 (rate limit), 503 (service unavailable)
    if ('statusCode' in error) {
      const status = (error as { statusCode: number }).statusCode;
      return status === 429 || status === 503 || status >= 500;
    }
  }
  return false;
}

// Main async wrapper with retry and timeout
async function withRetry<T>(
  operation: () => Promise<T>,
  options: AsyncWrapperOptions = {}
): Promise<T> {
  const retryOpts = { ...defaultRetryOptions, ...options.retry };
  let lastError: Error = new Error('No attempts made');

  for (let attempt = 1; attempt <= retryOpts.maxAttempts; attempt++) {
    try {
      // Apply timeout if configured
      const promise = operation();
      const result = options.timeout
        ? await withTimeout(promise, options.timeout)
        : await promise;

      return result;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Don't retry on last attempt or non-retryable errors
      const isLastAttempt = attempt === retryOpts.maxAttempts;
      const shouldRetry = !isLastAttempt && isRetryableError(error);

      if (!shouldRetry) {
        throw lastError;
      }

      const delayMs = calculateDelay(attempt, retryOpts);

      // Notify about retry
      if (options.onRetry) {
        options.onRetry(attempt, lastError, delayMs);
      }

      await sleep(delayMs);
    }
  }

  throw new RetryExhaustedError(retryOpts.maxAttempts, lastError);
}

// Convenience wrapper that returns Result type instead of throwing
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function trySafe<T>(
  operation: () => Promise<T>,
  options: AsyncWrapperOptions = {}
): Promise<Result<T>> {
  try {
    const data = await withRetry(operation, options);
    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error : new Error(String(error)),
    };
  }
}

// Batch operations with concurrency control
async function withConcurrency<T, R>(
  items: T[],
  operation: (item: T) => Promise<R>,
  maxConcurrency: number = 5
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];

  for (const item of items) {
    const promise = operation(item).then(result => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= maxConcurrency) {
      await Promise.race(executing);
      // Remove completed promises
      const completed = executing.filter(p =>
        Promise.race([p, Promise.resolve('pending')]).then(v => v !== 'pending')
      );
      executing.splice(0, executing.length, ...executing.filter(p => !completed.includes(p)));
    }
  }

  await Promise.all(executing);
  return results;
}

export {
  withRetry,
  withTimeout,
  trySafe,
  withConcurrency,
  sleep,
  calculateDelay,
  isRetryableError,
  TimeoutError,
  RetryExhaustedError,
  AsyncWrapperOptions,
  RetryOptions,
  TimeoutOptions,
  Result,
};
