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

#### Example 1: Schema-Based Config Validation

```
// Define configuration schema with types and defaults
configSchema = Schema({
    port: Number(default = 3000),
    environment: Enum(["development", "staging", "production"], default = "development"),
    database: {
        host: String(required = true),
        port: Number(default = 5432),
        name: String(required = true),
        user: String(required = true),
        password: String(required = true, secret = true)
    },
    redis: {
        url: String(format = "url", optional = true)
    },
    features: {
        newDashboard: Boolean(default = false)
    }
})

// Load and validate configuration from environment
function loadConfig():
    rawConfig = {
        port: env.get("PORT"),
        environment: env.get("NODE_ENV"),
        database: {
            host: env.get("DB_HOST"),
            port: env.get("DB_PORT"),
            name: env.get("DB_NAME"),
            user: env.get("DB_USER"),
            password: env.get("DB_PASSWORD")
        },
        redis: {
            url: env.get("REDIS_URL")
        },
        features: {
            newDashboard: env.get("FEATURE_NEW_DASHBOARD")
        }
    }

    result = configSchema.validate(rawConfig)

    if not result.success:
        log.error("Configuration validation failed:")
        log.error(result.errors)
        exit(1)

    return freeze(result.data)  // Make immutable

// Load once at startup
config = loadConfig()
```

#### Example 2: Environment-Specific Config Files

```
// config/default.config
defaultConfig = {
    api: {
        timeout: 5000,
        retries: 3
    },
    cache: {
        ttl: 3600
    }
}

// config/development.config
developmentConfig = {
    api: {
        timeout: 30000  // Longer for debugging
    },
    logging: {
        level: "debug"
    }
}

// config/production.config
productionConfig = {
    api: {
        timeout: 3000  // Stricter in prod
    },
    logging: {
        level: "info"
    }
}

// config/loader
function loadEnvironmentConfig():
    envConfigs = {
        "development": developmentConfig,
        "production": productionConfig
    }

    currentEnv = env.get("NODE_ENV") or "development"

    // Merge default with environment-specific config
    return deepMerge(defaultConfig, envConfigs[currentEnv] or {})

config = loadEnvironmentConfig()
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
```
stripe = new StripeClient("sk_live_abc123xyz")
dbPassword = "super_secret_password"
```

**Why it's problematic:**
- Secrets in version control are exposed forever
- Cannot rotate without code changes
- Same secret used across all environments

**Better approach:**
```
stripe = new StripeClient(env.get("STRIPE_SECRET_KEY"))
dbPassword = env.get("DB_PASSWORD")

// Validate at startup
if env.get("STRIPE_SECRET_KEY") is null:
    throw Error("STRIPE_SECRET_KEY is required")
```

### Anti-Pattern 2: Config at First Use

**What it looks like:**
```
// Somewhere deep in the codebase...
function sendEmail(to, subject, body):
    apiKey = env.get("SENDGRID_API_KEY")  // First check happens here!

    if apiKey is null:
        throw Error("SENDGRID_API_KEY not set")

    // Send email...
```

**Why it's problematic:**
- Errors discovered late, potentially in production
- Different code paths may have different config requirements
- Hard to know all required config upfront

**Better approach:**
```
// config module - loaded at startup
config = {
    sendgrid: {
        apiKey: requireEnv("SENDGRID_API_KEY")
    }
}

// email module
function sendEmail(to, subject, body):
    // Config already validated at startup
    client = new SendGridClient(config.sendgrid.apiKey)
    // Send email...
```

### Anti-Pattern 3: Logging Secrets

**What it looks like:**
```
print("Loaded config: " + toJson(config))
// Output: { dbHost: "localhost", dbPassword: "secret123", ... }
```

**Why it's problematic:**
- Secrets appear in logs, monitoring systems
- Log files may be accessible to many people
- Violates security compliance requirements

**Better approach:**
```
function safeLogConfig(config):
    sanitized = copy(config)
    sanitized.dbPassword = "[REDACTED]"

    for key in sanitized.apiKeys:
        sanitized.apiKeys[key] = "[REDACTED]"

    return sanitized

log.info("Loaded config: " + toJson(safeLogConfig(config)))
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
