/**
 * USE: When loading and validating configuration from environment variables
 * REQUIRES: TypeScript 4.5+, Node.js (process.env)
 * PATTERN: Configuration, Validation
 */

// Configuration validation error
class ConfigError extends Error {
  constructor(
    public readonly key: string,
    message: string,
    public readonly value?: unknown
  ) {
    super(`Configuration error for "${key}": ${message}`);
    this.name = 'ConfigError';
  }
}

// Environment variable reader with type coercion
type EnvReader<T> = {
  required: () => T;
  optional: (defaultValue: T) => T;
  optionalNullable: () => T | undefined;
};

function getString(key: string): EnvReader<string> {
  const value = process.env[key];

  return {
    required: () => {
      if (value === undefined || value === '') {
        throw new ConfigError(key, 'Required environment variable is not set');
      }
      return value;
    },
    optional: (defaultValue: string) => value ?? defaultValue,
    optionalNullable: () => value,
  };
}

function getNumber(key: string): EnvReader<number> {
  const rawValue = process.env[key];

  const parse = (): number | undefined => {
    if (rawValue === undefined || rawValue === '') return undefined;
    const num = Number(rawValue);
    if (Number.isNaN(num)) {
      throw new ConfigError(key, `Expected a number, got "${rawValue}"`);
    }
    return num;
  };

  return {
    required: () => {
      const value = parse();
      if (value === undefined) {
        throw new ConfigError(key, 'Required environment variable is not set');
      }
      return value;
    },
    optional: (defaultValue: number) => parse() ?? defaultValue,
    optionalNullable: () => parse(),
  };
}

function getBoolean(key: string): EnvReader<boolean> {
  const rawValue = process.env[key];

  const parse = (): boolean | undefined => {
    if (rawValue === undefined || rawValue === '') return undefined;
    const lower = rawValue.toLowerCase();
    if (['true', '1', 'yes', 'on'].includes(lower)) return true;
    if (['false', '0', 'no', 'off'].includes(lower)) return false;
    throw new ConfigError(key, `Expected a boolean, got "${rawValue}"`);
  };

  return {
    required: () => {
      const value = parse();
      if (value === undefined) {
        throw new ConfigError(key, 'Required environment variable is not set');
      }
      return value;
    },
    optional: (defaultValue: boolean) => parse() ?? defaultValue,
    optionalNullable: () => parse(),
  };
}

function getEnum<T extends string>(key: string, allowedValues: readonly T[]): EnvReader<T> {
  const rawValue = process.env[key];

  const parse = (): T | undefined => {
    if (rawValue === undefined || rawValue === '') return undefined;
    if (!allowedValues.includes(rawValue as T)) {
      throw new ConfigError(
        key,
        `Expected one of [${allowedValues.join(', ')}], got "${rawValue}"`
      );
    }
    return rawValue as T;
  };

  return {
    required: () => {
      const value = parse();
      if (value === undefined) {
        throw new ConfigError(key, 'Required environment variable is not set');
      }
      return value;
    },
    optional: (defaultValue: T) => parse() ?? defaultValue,
    optionalNullable: () => parse(),
  };
}

function getUrl(key: string): EnvReader<string> {
  const rawValue = process.env[key];

  const parse = (): string | undefined => {
    if (rawValue === undefined || rawValue === '') return undefined;
    try {
      new URL(rawValue);
      return rawValue;
    } catch {
      throw new ConfigError(key, `Expected a valid URL, got "${rawValue}"`);
    }
  };

  return {
    required: () => {
      const value = parse();
      if (value === undefined) {
        throw new ConfigError(key, 'Required environment variable is not set');
      }
      return value;
    },
    optional: (defaultValue: string) => parse() ?? defaultValue,
    optionalNullable: () => parse(),
  };
}

// CUSTOMIZE: Define your application configuration
const Environment = ['development', 'staging', 'production', 'test'] as const;
type Environment = typeof Environment[number];

interface AppConfig {
  // Application
  env: Environment;
  port: number;
  host: string;
  logLevel: 'debug' | 'info' | 'warn' | 'error';

  // Database
  databaseUrl: string;
  databasePoolSize: number;

  // External services
  apiBaseUrl: string;
  apiTimeout: number;

  // Feature flags
  featureNewDashboard: boolean;
  featureAnalytics: boolean;
}

// CUSTOMIZE: Load your configuration
function loadConfig(): AppConfig {
  return {
    // Application
    env: getEnum('NODE_ENV', Environment).optional('development'),
    port: getNumber('PORT').optional(3000),
    host: getString('HOST').optional('0.0.0.0'),
    logLevel: getEnum('LOG_LEVEL', ['debug', 'info', 'warn', 'error'] as const).optional('info'),

    // Database
    databaseUrl: getString('DATABASE_URL').required(),
    databasePoolSize: getNumber('DATABASE_POOL_SIZE').optional(10),

    // External services
    apiBaseUrl: getUrl('API_BASE_URL').required(),
    apiTimeout: getNumber('API_TIMEOUT_MS').optional(30000),

    // Feature flags
    featureNewDashboard: getBoolean('FEATURE_NEW_DASHBOARD').optional(false),
    featureAnalytics: getBoolean('FEATURE_ANALYTICS').optional(true),
  };
}

// Singleton config instance
let configInstance: AppConfig | null = null;

function getConfig(): AppConfig {
  if (!configInstance) {
    configInstance = loadConfig();
  }
  return configInstance;
}

// Reset config (useful for testing)
function resetConfig(): void {
  configInstance = null;
}

// Validate all required config at startup
function validateConfig(): void {
  try {
    loadConfig();
    console.log('Configuration validated successfully');
  } catch (error) {
    if (error instanceof ConfigError) {
      console.error(`Configuration validation failed: ${error.message}`);
      process.exit(1);
    }
    throw error;
  }
}

export {
  loadConfig,
  getConfig,
  resetConfig,
  validateConfig,
  getString,
  getNumber,
  getBoolean,
  getEnum,
  getUrl,
  ConfigError,
  AppConfig,
  Environment,
};
