---
name: "Configuration"
category: "Infrastructure"
tags:
  - configuration
  - environment
  - secrets
  - settings
activation:
  keywords:
    - config
    - configuration
    - environment
    - env
    - settings
    - secrets
    - dotenv
    - variables
  file_patterns:
    - "**/config*.{js,ts,py,go,rs,java,kt,json,yaml,yml}"
    - "**/.env*"
    - "**/settings*.{js,ts,py,go,rs,java,kt}"
    - "**/*Config.java"
    - "**/*Configuration.java"
    - "**/*Properties.java"
    - "**/application.properties"
    - "**/application.yml"
version: "1.0"
last_updated: "2026-01-19"
---

# Configuration

> Manage application configuration with environment-aware settings, secure secrets handling, and validation.

---

## AI Quick Reference

### When to Apply
- Setting up a new application or service
- Adding environment-specific behavior (dev/staging/prod)
- Managing secrets (API keys, database credentials)
- Making behavior configurable without code changes

### Core Principles
1. **Environment Variables for Secrets**: Never commit secrets to code
2. **Fail Fast**: Validate config at startup, not at first use
3. **Typed Configuration**: Use schemas/types, not raw strings
4. **Sensible Defaults**: Dev should work out-of-box, prod requires explicit config
5. **Layered Config**: Base → Environment → Local overrides

### Quick Implementation Checklist
- [ ] Create config schema with types and validation
- [ ] Load from environment variables (12-factor app)
- [ ] Validate all required config at startup
- [ ] Provide sensible defaults for development
- [ ] Document all config options
- [ ] Never log secret values

### Code Pattern (Pseudocode)
```
// Define config schema with defaults
configSchema = {
    port: { type: number, default: 3000, env: 'PORT' },
    database: {
        host: { type: string, required: true, env: 'DB_HOST' },
        port: { type: number, default: 5432, env: 'DB_PORT' },
        password: { type: string, required: true, env: 'DB_PASSWORD', secret: true }
    },
    logLevel: { type: enum['debug','info','warn','error'], default: 'info', env: 'LOG_LEVEL' }
}

// Load and validate at startup
function loadConfig() {
    config = {}
    errors = []

    for (key, schema in configSchema) {
        value = env[schema.env] ?? schema.default
        if (schema.required && !value) {
            errors.push(`Missing required config: ${key}`)
        }
        config[key] = parseValue(value, schema.type)
    }

    if (errors.length > 0) {
        throw new ConfigError(errors)
    }

    return freeze(config)  // Immutable
}
```

### Key Decisions
| Decision Point | Recommended Choice | Rationale |
|----------------|-------------------|-----------|
| Config source | Environment variables | 12-factor, container-friendly |
| Secrets storage | Vault/KMS/Secret Manager | Rotation, audit, access control |
| Schema validation | At startup | Fail fast, clear errors |
| Config mutability | Immutable after load | Prevents runtime confusion |

---

## Human Documentation

### Overview

Configuration management is about separating what changes between environments from the code itself. Good configuration practices enable:

- Running the same code in dev, staging, and production
- Secure handling of sensitive credentials
- Easy onboarding for new developers
- Clear documentation of available options
- Quick diagnosis of misconfiguration issues

### Detailed Explanation

#### Concept 1: Configuration Layers

Configuration should be loaded in layers, with later layers overriding earlier ones:

```
1. Default values (in code)
   ↓
2. Config file (config.yaml, config.json)
   ↓
3. Environment variables (DB_HOST, API_KEY)
   ↓
4. Command-line arguments (--port=8080)
   ↓
5. Runtime overrides (for testing)
```

This allows:
- Sensible defaults for development
- File-based config for complex settings
- Environment-based config for deployment
- CLI args for one-off overrides

#### Concept 2: Secrets vs Settings

Not all configuration is equal:

| Type | Examples | Storage | Can Log? |
|------|----------|---------|----------|
| **Settings** | Port, log level, feature flags | Config files, env vars | Yes |
| **Secrets** | API keys, passwords, tokens | Secret managers, encrypted env | Never |
| **Infrastructure** | Database host, service URLs | Config files, env vars | Yes |

Secrets require special handling:
- Never commit to version control
- Use secret managers (AWS Secrets Manager, HashiCorp Vault)
- Rotate regularly
- Audit access
- Inject at runtime, not build time

#### Concept 3: Configuration Validation

All configuration should be validated at application startup:

```typescript
// Good: Validate at startup
const config = loadConfig(); // Throws if invalid

// Bad: Validate at first use
function getDatabase() {
    const host = process.env.DB_HOST; // Might be missing!
    return connect(host);
}
```

Validation should check:
- Required values are present
- Types are correct (number is actually a number)
- Values are within valid ranges
- Dependencies are satisfied (if A then B required)

### Implementation Examples

#### Example 1: Typed Config with Zod (TypeScript)

```typescript
import { z } from 'zod';

// Define schema
const configSchema = z.object({
    port: z.coerce.number().default(3000),
    nodeEnv: z.enum(['development', 'staging', 'production']).default('development'),
    database: z.object({
        host: z.string().min(1),
        port: z.coerce.number().default(5432),
        name: z.string().min(1),
        user: z.string().min(1),
        password: z.string().min(1),
    }),
    redis: z.object({
        url: z.string().url().optional(),
    }).optional(),
    features: z.object({
        newDashboard: z.coerce.boolean().default(false),
    }),
});

type Config = z.infer<typeof configSchema>;

// Load from environment
function loadConfig(): Config {
    const result = configSchema.safeParse({
        port: process.env.PORT,
        nodeEnv: process.env.NODE_ENV,
        database: {
            host: process.env.DB_HOST,
            port: process.env.DB_PORT,
            name: process.env.DB_NAME,
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
        },
        redis: process.env.REDIS_URL ? { url: process.env.REDIS_URL } : undefined,
        features: {
            newDashboard: process.env.FEATURE_NEW_DASHBOARD,
        },
    });

    if (!result.success) {
        console.error('Configuration validation failed:');
        console.error(result.error.format());
        process.exit(1);
    }

    return Object.freeze(result.data);
}

export const config = loadConfig();
```

#### Example 2: Environment-Specific Config Files

```typescript
// config/default.ts
export default {
    api: {
        timeout: 5000,
        retries: 3,
    },
    cache: {
        ttl: 3600,
    },
};

// config/development.ts
export default {
    api: {
        timeout: 30000, // Longer for debugging
    },
    logging: {
        level: 'debug',
    },
};

// config/production.ts
export default {
    api: {
        timeout: 3000, // Stricter in prod
    },
    logging: {
        level: 'info',
    },
};

// config/index.ts
import defaultConfig from './default';
import devConfig from './development';
import prodConfig from './production';

const envConfigs = {
    development: devConfig,
    production: prodConfig,
};

const env = process.env.NODE_ENV || 'development';
export const config = deepMerge(defaultConfig, envConfigs[env] || {});
```

### Best Practices

1. **Use .env.example**: Commit a template file showing all required environment variables (without actual values).

2. **Validate Early**: Check all configuration at startup. Don't wait for first use to discover missing values.

3. **Type Your Config**: Use TypeScript, Zod, or similar to get compile-time safety and IDE autocomplete.

4. **Document Each Option**: Every config option should have a comment explaining its purpose and valid values.

5. **Provide Development Defaults**: Developers should be able to run the app locally without setting up secrets (use dev databases, mock services).

### Trade-offs and Considerations

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Environment variables | Simple, container-native | Flat structure, no types | Secrets, simple config |
| Config files (JSON/YAML) | Hierarchical, readable | Must manage per environment | Complex settings |
| Secret managers | Secure, audited, rotatable | Added complexity, cost | Production secrets |
| Feature flags service | Dynamic, targeted | External dependency | Gradual rollouts |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Hardcoded Secrets

**What it looks like:**
```javascript
const stripe = new Stripe('sk_live_abc123xyz');
const dbPassword = 'super_secret_password';
```

**Why it's problematic:**
- Secrets in version control are exposed forever
- Cannot rotate without code changes
- Same secret used across all environments

**Better approach:**
```javascript
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const dbPassword = process.env.DB_PASSWORD;

// Validate at startup
if (!process.env.STRIPE_SECRET_KEY) {
    throw new Error('STRIPE_SECRET_KEY is required');
}
```

### Anti-Pattern 2: Config at First Use

**What it looks like:**
```javascript
// Somewhere deep in the codebase...
function sendEmail(to, subject, body) {
    const apiKey = process.env.SENDGRID_API_KEY; // First check!
    if (!apiKey) {
        throw new Error('SENDGRID_API_KEY not set');
    }
    // ...
}
```

**Why it's problematic:**
- Errors discovered late, potentially in production
- Different code paths may have different config requirements
- Hard to know all required config upfront

**Better approach:**
```javascript
// config.ts - loaded at startup
export const config = {
    sendgrid: {
        apiKey: requireEnv('SENDGRID_API_KEY'),
    },
};

// email.ts
import { config } from './config';

function sendEmail(to, subject, body) {
    // Config already validated
    const client = new SendGrid(config.sendgrid.apiKey);
    // ...
}
```

### Anti-Pattern 3: Logging Secrets

**What it looks like:**
```javascript
console.log('Loaded config:', config);
// Output: { dbHost: 'localhost', dbPassword: 'secret123', ... }
```

**Why it's problematic:**
- Secrets appear in logs, monitoring systems
- Log files may be accessible to many people
- Violates security compliance requirements

**Better approach:**
```javascript
function safeLogConfig(config) {
    return {
        ...config,
        dbPassword: '[REDACTED]',
        apiKeys: Object.keys(config.apiKeys).reduce((acc, key) => {
            acc[key] = '[REDACTED]';
            return acc;
        }, {}),
    };
}

console.log('Loaded config:', safeLogConfig(config));
```

---

## Related Patterns

- [Logging](./logging.md) - Never log configuration secrets
- [Validation](./validation.md) - Validate configuration values

---

## References

- [12-Factor App - Config](https://12factor.net/config) - Store config in environment
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) - Security best practices
- [Zod Documentation](https://zod.dev/) - TypeScript schema validation
