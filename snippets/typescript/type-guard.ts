/**
 * USE: When validating unknown data at runtime boundaries (API responses, user input)
 * REQUIRES: TypeScript 4.5+
 * PATTERN: Validation
 */

// Primitive type guards
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isNumber(value: unknown): value is number {
  return typeof value === 'number' && !Number.isNaN(value);
}

function isBoolean(value: unknown): value is boolean {
  return typeof value === 'boolean';
}

function isNull(value: unknown): value is null {
  return value === null;
}

function isUndefined(value: unknown): value is undefined {
  return value === undefined;
}

function isNullish(value: unknown): value is null | undefined {
  return value === null || value === undefined;
}

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isArray(value: unknown): value is unknown[] {
  return Array.isArray(value);
}

function isFunction(value: unknown): value is (...args: unknown[]) => unknown {
  return typeof value === 'function';
}

// Array type guard with element validation
function isArrayOf<T>(
  value: unknown,
  elementGuard: (element: unknown) => element is T
): value is T[] {
  return isArray(value) && value.every(elementGuard);
}

// Object with specific properties
function hasProperty<K extends string>(
  obj: unknown,
  key: K
): obj is Record<K, unknown> {
  return isObject(obj) && key in obj;
}

function hasProperties<K extends string>(
  obj: unknown,
  keys: K[]
): obj is Record<K, unknown> {
  return isObject(obj) && keys.every(key => key in obj);
}

// CUSTOMIZE: Create domain-specific type guards

// Example: User type guard
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
  roles?: string[];
}

function isUser(value: unknown): value is User {
  if (!isObject(value)) return false;

  return (
    hasProperties(value, ['id', 'name', 'email', 'createdAt']) &&
    isString(value.id) &&
    isString(value.name) &&
    isString(value.email) &&
    isString(value.createdAt) &&
    (isUndefined(value.roles) || isArrayOf(value.roles, isString))
  );
}

// Example: API response type guard
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

function isApiResponse<T>(
  value: unknown,
  dataGuard: (data: unknown) => data is T
): value is ApiResponse<T> {
  if (!isObject(value)) return false;
  if (!hasProperty(value, 'success') || !isBoolean(value.success)) return false;
  if (!hasProperty(value, 'data') || !dataGuard(value.data)) return false;
  if (hasProperty(value, 'error') && !isString(value.error)) return false;

  return true;
}

// Assertion functions (throw on failure)
function assertIsString(value: unknown, name = 'value'): asserts value is string {
  if (!isString(value)) {
    throw new TypeError(`Expected ${name} to be a string, got ${typeof value}`);
  }
}

function assertIsNumber(value: unknown, name = 'value'): asserts value is number {
  if (!isNumber(value)) {
    throw new TypeError(`Expected ${name} to be a number, got ${typeof value}`);
  }
}

function assertIsObject(value: unknown, name = 'value'): asserts value is Record<string, unknown> {
  if (!isObject(value)) {
    throw new TypeError(`Expected ${name} to be an object, got ${typeof value}`);
  }
}

// Safe parsing utilities
function parseJsonSafe<T>(
  json: string,
  guard: (value: unknown) => value is T
): T | null {
  try {
    const parsed: unknown = JSON.parse(json);
    return guard(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

// Result type for validation
type ValidationResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function validate<T>(
  value: unknown,
  guard: (value: unknown) => value is T,
  errorMessage: string
): ValidationResult<T> {
  if (guard(value)) {
    return { success: true, data: value };
  }
  return { success: false, error: errorMessage };
}

export {
  // Primitives
  isString,
  isNumber,
  isBoolean,
  isNull,
  isUndefined,
  isNullish,
  isObject,
  isArray,
  isFunction,
  // Compound
  isArrayOf,
  hasProperty,
  hasProperties,
  // Assertions
  assertIsString,
  assertIsNumber,
  assertIsObject,
  // Utilities
  parseJsonSafe,
  validate,
  // Domain-specific (customize these)
  isUser,
  isApiResponse,
  // Types
  ValidationResult,
  User,
  ApiResponse,
};
