/**
 * USE: When implementing structured error handling with custom error types
 * REQUIRES: TypeScript 4.5+
 * PATTERN: Error Handling
 */

// Base application error with structured context
class AppError extends Error {
  public readonly timestamp: Date;
  public readonly requestId?: string;

  constructor(
    public readonly code: string,
    message: string,
    public readonly userMessage: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>,
    public readonly cause?: Error
  ) {
    super(message);
    this.name = 'AppError';
    this.timestamp = new Date();

    // Capture stack trace, excluding constructor
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AppError);
    }
  }

  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      userMessage: this.userMessage,
      statusCode: this.statusCode,
      context: this.context,
      timestamp: this.timestamp.toISOString(),
      requestId: this.requestId,
    };
  }
}

// CUSTOMIZE: Add domain-specific error types
class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly field: string,
    public readonly value?: unknown
  ) {
    super(
      'VALIDATION_ERROR',
      message,
      `Invalid value for ${field}`,
      400,
      { field, value }
    );
    this.name = 'ValidationError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string | number) {
    super(
      'NOT_FOUND',
      `${resource} with id ${id} not found`,
      `${resource} not found`,
      404,
      { resource, id }
    );
    this.name = 'NotFoundError';
  }
}

class UnauthorizedError extends AppError {
  constructor(reason: string = 'Invalid credentials') {
    super(
      'UNAUTHORIZED',
      reason,
      'Please log in to continue',
      401
    );
    this.name = 'UnauthorizedError';
  }
}

class ForbiddenError extends AppError {
  constructor(action: string, resource?: string) {
    super(
      'FORBIDDEN',
      `Not permitted to ${action}${resource ? ` on ${resource}` : ''}`,
      'You do not have permission to perform this action',
      403,
      { action, resource }
    );
    this.name = 'ForbiddenError';
  }
}

class ConflictError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(
      'CONFLICT',
      message,
      'This operation conflicts with existing data',
      409,
      context
    );
    this.name = 'ConflictError';
  }
}

// Type guard for AppError
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

// Error handler for Express-style middleware
// CUSTOMIZE: Adapt for your framework (Fastify, Koa, etc.)
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    requestId?: string;
  };
}

function handleError(error: unknown, requestId?: string): {
  statusCode: number;
  body: ErrorResponse;
} {
  // Log the full error for debugging
  console.error('[Error]', {
    requestId,
    error: error instanceof Error ? {
      name: error.name,
      message: error.message,
      stack: error.stack,
      ...(isAppError(error) ? error.toJSON() : {}),
    } : error,
  });

  if (isAppError(error)) {
    return {
      statusCode: error.statusCode,
      body: {
        error: {
          code: error.code,
          message: error.userMessage,
          requestId,
        },
      },
    };
  }

  // Unknown error - don't expose internal details
  return {
    statusCode: 500,
    body: {
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred. Please try again later.',
        requestId,
      },
    },
  };
}

// Async error wrapper for route handlers
type AsyncHandler<T> = (...args: unknown[]) => Promise<T>;

function catchAsync<T>(fn: AsyncHandler<T>): AsyncHandler<T> {
  return async (...args: unknown[]): Promise<T> => {
    try {
      return await fn(...args);
    } catch (error) {
      // Re-throw AppErrors as-is, wrap others
      if (isAppError(error)) {
        throw error;
      }
      throw new AppError(
        'INTERNAL_ERROR',
        error instanceof Error ? error.message : 'Unknown error',
        'An unexpected error occurred',
        500,
        undefined,
        error instanceof Error ? error : undefined
      );
    }
  };
}

export {
  AppError,
  ValidationError,
  NotFoundError,
  UnauthorizedError,
  ForbiddenError,
  ConflictError,
  isAppError,
  handleError,
  catchAsync,
};
