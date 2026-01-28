# Codebase Analysis Protocol

**Version:** 1.0.0
**Purpose:** Analyze existing codebase patterns for documentation generation
**Scope:** Conductor setup command, brownfield project initialization, CLAUDE.md generation

---

## Overview

This protocol defines the algorithm for detecting established patterns, conventions, and architecture decisions in an existing codebase. The output is used to generate Progressive Disclosure documentation (CLAUDE.md and conductor/docs/) that helps AI assistants understand and follow existing project conventions.

**Key Principle:** Use heuristics and file pattern analysis, not AST parsing. This ensures cross-language compatibility and reasonable performance.

---

## Analysis Categories

The protocol analyzes six categories of patterns:

| Category | Output File | Description |
|----------|-------------|-------------|
| Code Conventions | `code-conventions.md` | Naming, imports, file organization |
| Architecture | `architecture.md` | Design patterns, layer organization |
| Testing | `testing.md` | Test patterns, framework usage |
| Annotations | `annotations.md` | Decorators, annotations, documentation |
| API Patterns | `api-patterns.md` | REST/GraphQL conventions, error handling |
| Configuration | `configuration.md` | Config files, env vars, build setup |

---

## Detection Algorithms

### Category 1: Code Conventions

#### 1.1 File Naming Convention Detection

**Algorithm:**

```
1. Sample files from directories: src/, lib/, app/, components/, services/, utils/
2. Exclude: node_modules, vendor, venv, __pycache__, target, build, dist
3. For each file, classify naming style:
   - kebab-case: user-profile.ts, api-client.js
   - camelCase: userProfile.ts, apiClient.js
   - PascalCase: UserProfile.ts, ApiClient.js
   - snake_case: user_profile.py, api_client.py
4. Calculate percentage for each style
5. Report dominant style (>60% of files) with HIGH confidence
6. Report secondary styles (>20% of files) with MEDIUM confidence
```

**Detection Patterns:**

| Pattern | Regex | Example |
|---------|-------|---------|
| kebab-case | `^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z]+$` | `user-profile.ts` |
| camelCase | `^[a-z][a-zA-Z0-9]*\.[a-z]+$` | `userProfile.ts` |
| PascalCase | `^[A-Z][a-zA-Z0-9]*\.[a-z]+$` | `UserProfile.ts` |
| snake_case | `^[a-z][a-z0-9]*(_[a-z0-9]+)*\.[a-z]+$` | `user_profile.py` |

**Output:**

```json
{
  "category": "naming_conventions",
  "file_naming": {
    "dominant": "kebab-case",
    "confidence": "HIGH",
    "distribution": {
      "kebab-case": 75,
      "PascalCase": 20,
      "other": 5
    },
    "examples": [
      "src/components/user-profile.tsx",
      "src/services/api-client.ts"
    ]
  }
}
```

#### 1.2 Directory Structure Detection

**Algorithm:**

```
1. Scan root and first two levels of directories
2. Match against known structural patterns:
   - Feature-based: features/, modules/
   - Type-based: components/, services/, utils/, models/
   - Layer-based: presentation/, domain/, data/, infrastructure/
   - Rails-style: app/controllers/, app/models/, app/views/
3. Record matched patterns with confidence
4. Extract example paths for documentation
```

**Known Structure Patterns:**

| Pattern Name | Indicator Directories | Confidence Boost |
|--------------|----------------------|------------------|
| Feature-based | `features/`, `modules/`, `domains/` | +20 |
| Component-based | `components/`, `ui/`, `views/` | +15 |
| Service-layer | `services/`, `repositories/`, `use-cases/` | +15 |
| Clean Architecture | `domain/`, `application/`, `infrastructure/` | +25 |
| Hexagonal | `adapters/`, `ports/`, `core/` | +25 |
| MVC | `controllers/`, `models/`, `views/` | +20 |
| MVVM | `viewmodels/`, `views/`, `models/` | +20 |

**Output:**

```json
{
  "directory_structure": {
    "pattern": "feature-based",
    "confidence": "HIGH",
    "key_directories": [
      "src/features/",
      "src/shared/",
      "src/core/"
    ],
    "examples": [
      "src/features/auth/",
      "src/features/dashboard/",
      "src/shared/components/"
    ]
  }
}
```

#### 1.3 Import Pattern Detection

**Algorithm:**

```
1. Sample first 50 lines of 20 code files
2. Detect import statements by language:
   - JS/TS: import ... from '...' or require('...')
   - Python: import ... or from ... import ...
   - Go: import "..." or import (...)
   - Java: import ...;
3. Classify import paths:
   - Relative: ./module, ../utils
   - Absolute: @/components, ~/services
   - Path alias: paths configured in tsconfig/jsconfig
   - Package: external packages
4. Calculate percentages for each type
```

**Detection Patterns:**

| Language | Import Pattern | Classification |
|----------|---------------|----------------|
| JS/TS | `from '\.\./` | Relative |
| JS/TS | `from '@/` | Absolute (alias) |
| JS/TS | `from '~/` | Absolute (alias) |
| JS/TS | `from '[a-z]` | Package |
| Python | `from \.` | Relative |
| Python | `from [a-z]` | Package/Absolute |

**Output:**

```json
{
  "import_patterns": {
    "dominant": "absolute_aliases",
    "confidence": "HIGH",
    "alias_format": "@/",
    "distribution": {
      "absolute_aliases": 70,
      "relative": 20,
      "packages": 10
    },
    "examples": [
      "import { Button } from '@/components/ui'",
      "import { api } from '@/services/api-client'"
    ]
  }
}
```

#### 1.4 Module Organization Detection

**Algorithm:**

```
1. Check for barrel files (index.ts, index.js, __init__.py, mod.rs)
2. Analyze export patterns:
   - Named exports: export { A, B, C }
   - Default exports: export default
   - Re-exports: export * from './module'
3. Detect co-location patterns:
   - Component + test + style in same folder
   - Feature folders with internal organization
```

**Barrel File Detection:**

| File | Language | Pattern |
|------|----------|---------|
| `index.ts` | TypeScript | `export * from` or `export { ... } from` |
| `index.js` | JavaScript | Same as TS |
| `__init__.py` | Python | `from .module import` |
| `mod.rs` | Rust | `pub mod` |
| `package.json` (exports) | Node | `"exports": { ... }` |

**Output:**

```json
{
  "module_organization": {
    "barrel_exports": true,
    "confidence": "HIGH",
    "barrel_pattern": "named_reexports",
    "co_location": {
      "detected": true,
      "pattern": "component_folder",
      "contents": ["component", "test", "styles", "types"]
    },
    "examples": [
      "src/components/Button/index.ts",
      "src/components/Button/Button.tsx",
      "src/components/Button/Button.test.tsx"
    ]
  }
}
```

---

### Category 2: Architecture Patterns

#### 2.1 Design Pattern Detection

**Algorithm:**

```
1. Scan for pattern indicators in code:
   - Class/function names containing pattern keywords
   - File names matching pattern conventions
   - Import patterns suggesting dependency injection
2. Cross-reference with framework conventions
3. Assign confidence based on indicator density
```

**Pattern Indicators:**

| Pattern | File Indicators | Code Indicators |
|---------|-----------------|-----------------|
| Repository | `*Repository.ts`, `*Repo.py` | `interface.*Repository`, `class.*Repository` |
| Factory | `*Factory.ts`, `factory.py` | `create*()`, `build*()` |
| Singleton | `instance`, `getInstance` | `private static instance` |
| Observer | `*Observer`, `*Listener` | `subscribe()`, `notify()`, `emit()` |
| Strategy | `*Strategy.ts` | `interface.*Strategy`, `execute()` |
| Adapter | `*Adapter.ts` | `adapt()`, `convert()` |
| Facade | `*Facade.ts`, `*Service.ts` | Aggregates multiple dependencies |
| Builder | `*Builder.ts` | `.with*()` method chains |
| Command | `*Command.ts`, `*Handler.ts` | `execute()`, `handle()` |
| Decorator | `*Decorator.ts` | `@decorator`, wrapper functions |

**Detection Commands:**

```bash
# Find Repository pattern
grep -r "Repository" --include="*.ts" --include="*.py" --include="*.java" -l

# Find Factory pattern
grep -r "Factory\|create.*=\|build.*=" --include="*.ts" --include="*.py" -l

# Find Observer pattern
grep -r "subscribe\|notify\|emit\|addEventListener" --include="*.ts" --include="*.js" -l
```

**Output:**

```json
{
  "design_patterns": [
    {
      "pattern": "Repository",
      "confidence": "HIGH",
      "occurrences": 8,
      "examples": [
        "src/repositories/UserRepository.ts",
        "src/repositories/OrderRepository.ts"
      ]
    },
    {
      "pattern": "Factory",
      "confidence": "MEDIUM",
      "occurrences": 3,
      "examples": [
        "src/factories/ConnectionFactory.ts"
      ]
    }
  ]
}
```

#### 2.2 Layer Organization Detection

**Algorithm:**

```
1. Analyze directory structure for layer indicators
2. Check import directions (dependencies should flow inward)
3. Detect domain isolation patterns
```

**Layer Patterns:**

| Architecture | Directory Structure | Import Direction |
|--------------|--------------------|--------------------|
| Clean Architecture | `domain/`, `application/`, `infrastructure/`, `presentation/` | Inward (infra → app → domain) |
| Hexagonal | `core/`, `adapters/`, `ports/` | Ports define interfaces, adapters implement |
| Onion | `core/`, `services/`, `infrastructure/` | Outside depends on inside |
| N-Tier | `presentation/`, `business/`, `data/` | Top depends on bottom |
| MVC | `models/`, `views/`, `controllers/` | Controllers use models and views |
| MVVM | `models/`, `views/`, `viewmodels/` | Views bind to ViewModels |

**Output:**

```json
{
  "layer_organization": {
    "architecture": "Clean Architecture",
    "confidence": "HIGH",
    "layers": [
      {"name": "domain", "path": "src/domain/"},
      {"name": "application", "path": "src/application/"},
      {"name": "infrastructure", "path": "src/infrastructure/"},
      {"name": "presentation", "path": "src/presentation/"}
    ],
    "dependency_direction": "inward",
    "examples": [
      "src/application/use-cases/CreateUser.ts imports from src/domain/entities/User.ts"
    ]
  }
}
```

#### 2.3 Dependency Injection Detection

**Algorithm:**

```
1. Search for DI container indicators:
   - Framework-specific: @Injectable, @Inject, providers array
   - Manual DI: Constructor injection patterns
   - Service locator: get(), resolve()
2. Analyze constructor parameters for dependency patterns
```

**DI Indicators:**

| Framework/Pattern | Indicators |
|-------------------|------------|
| NestJS | `@Injectable()`, `@Inject()`, `providers: []` |
| Angular | `@Injectable()`, `providers`, `inject()` |
| Spring | `@Autowired`, `@Component`, `@Service` |
| .NET Core | `services.Add*()`, `[Inject]` |
| Manual Constructor DI | Constructor params match class fields |
| InversifyJS | `@injectable()`, `container.bind()` |
| TSyringe | `@injectable()`, `@inject()`, `container.resolve()` |

**Output:**

```json
{
  "dependency_injection": {
    "detected": true,
    "pattern": "framework_di",
    "framework": "NestJS",
    "confidence": "HIGH",
    "indicators": [
      "@Injectable() decorator",
      "Module providers array",
      "Constructor injection"
    ],
    "examples": [
      "src/services/UserService.ts uses @Injectable()",
      "src/modules/app.module.ts defines providers"
    ]
  }
}
```

#### 2.4 State Management Detection (Frontend)

**Algorithm:**

```
1. Check for state management libraries in dependencies
2. Search for store/state patterns in code
3. Identify state organization approach
```

**State Management Patterns:**

| Library | File Indicators | Code Indicators |
|---------|-----------------|-----------------|
| Redux | `store.ts`, `*Slice.ts`, `*Reducer.ts` | `createSlice`, `configureStore`, `useSelector` |
| Zustand | `*Store.ts` | `create()`, `useStore` |
| MobX | `*Store.ts` | `@observable`, `makeAutoObservable` |
| Recoil | `*Atom.ts`, `*Selector.ts` | `atom()`, `selector()`, `useRecoilState` |
| Jotai | `*Atom.ts` | `atom()`, `useAtom` |
| Pinia | `*Store.ts` | `defineStore()`, `useStore` |
| Vuex | `store/`, `modules/` | `createStore()`, `useStore()` |
| Context API | `*Context.tsx`, `*Provider.tsx` | `createContext`, `useContext` |

**Output:**

```json
{
  "state_management": {
    "library": "Redux Toolkit",
    "confidence": "HIGH",
    "pattern": "slice_per_feature",
    "indicators": [
      "createSlice usage",
      "configureStore setup",
      "Feature-based slice organization"
    ],
    "examples": [
      "src/store/slices/authSlice.ts",
      "src/store/slices/userSlice.ts"
    ]
  }
}
```

---

### Category 3: Testing Patterns

#### 3.1 Test File Naming Convention

**Algorithm:**

```
1. Search for test files using common patterns
2. Count occurrences of each naming convention
3. Determine dominant convention
```

**Test File Patterns:**

| Convention | Pattern | Examples |
|------------|---------|----------|
| `.test.` suffix | `*.test.ts`, `*.test.js` | `User.test.ts` |
| `.spec.` suffix | `*.spec.ts`, `*.spec.js` | `User.spec.ts` |
| `_test` suffix | `*_test.py`, `*_test.go` | `user_test.py`, `user_test.go` |
| `Test` prefix | `Test*.java` | `TestUser.java` |
| `__tests__` directory | `__tests__/*.ts` | `__tests__/User.ts` |
| `test/` directory | `test/**/*.ts` | `test/user.ts` |
| `tests/` directory | `tests/**/*.py` | `tests/test_user.py` |

**Output:**

```json
{
  "test_naming": {
    "convention": ".test.ts suffix",
    "confidence": "HIGH",
    "test_count": 45,
    "distribution": {
      ".test.ts": 40,
      ".spec.ts": 5
    },
    "examples": [
      "src/services/UserService.test.ts",
      "src/utils/helpers.test.ts"
    ]
  }
}
```

#### 3.2 Test Framework Detection

**Algorithm:**

```
1. Check package.json/requirements.txt for test dependencies
2. Search for framework-specific imports and patterns
3. Detect assertion library usage
```

**Framework Indicators:**

| Framework | Dependencies | Code Patterns |
|-----------|--------------|---------------|
| Jest | `jest`, `@types/jest` | `describe()`, `it()`, `expect()`, `test()` |
| Vitest | `vitest` | `describe()`, `it()`, `expect()`, `vi.mock()` |
| Mocha | `mocha` | `describe()`, `it()` + assertion library |
| Pytest | `pytest` | `def test_*`, `@pytest.fixture` |
| Go testing | stdlib | `func Test*`, `t.Run()`, `t.Error()` |
| JUnit | `junit`, `junit-jupiter` | `@Test`, `@BeforeEach`, `assertEquals()` |
| xUnit | `xunit` | `[Fact]`, `[Theory]`, `Assert.*` |
| RSpec | `rspec` | `describe`, `it`, `expect().to` |

**Output:**

```json
{
  "test_framework": {
    "primary": "Vitest",
    "confidence": "HIGH",
    "assertion_library": "built-in",
    "features_detected": [
      "snapshot testing",
      "mocking with vi.mock",
      "concurrent tests"
    ],
    "examples": [
      "vi.mock() usage in tests",
      "expect().toMatchSnapshot()"
    ]
  }
}
```

#### 3.3 Mocking Pattern Detection

**Algorithm:**

```
1. Search for mock-related imports and function calls
2. Identify mocking approach (manual vs library)
3. Detect mock file locations
```

**Mocking Patterns:**

| Pattern | Indicators |
|---------|------------|
| Manual mocks | `__mocks__/`, `mocks/` directories |
| Jest mocks | `jest.mock()`, `jest.spyOn()` |
| Vitest mocks | `vi.mock()`, `vi.spyOn()` |
| Mockito | `@Mock`, `when().thenReturn()` |
| unittest.mock | `patch()`, `MagicMock()` |
| gomock | `//go:generate mockgen` |
| Sinon | `sinon.stub()`, `sinon.spy()` |

**Output:**

```json
{
  "mocking_patterns": {
    "approach": "inline_mocks",
    "library": "vitest",
    "confidence": "HIGH",
    "patterns_found": [
      "vi.mock() for module mocking",
      "vi.spyOn() for method spying",
      "Manual mock implementations in __mocks__/"
    ],
    "mock_locations": [
      "src/__mocks__/",
      "Inline vi.mock() calls"
    ],
    "examples": [
      "vi.mock('@/services/api')",
      "const spy = vi.spyOn(service, 'method')"
    ]
  }
}
```

#### 3.4 Test Organization Detection

**Algorithm:**

```
1. Analyze test directory structure
2. Identify test type separation (unit, integration, e2e)
3. Detect test grouping strategy
```

**Organization Patterns:**

| Pattern | Directory Structure |
|---------|---------------------|
| Co-located | Tests next to source files |
| Centralized | All tests in `test/` or `tests/` |
| Type-separated | `unit/`, `integration/`, `e2e/` |
| Feature-grouped | `tests/features/auth/`, `tests/features/users/` |

**Output:**

```json
{
  "test_organization": {
    "pattern": "co-located",
    "confidence": "HIGH",
    "test_types": {
      "unit": "*.test.ts (co-located)",
      "integration": "tests/integration/",
      "e2e": "tests/e2e/"
    },
    "examples": [
      "src/services/UserService.test.ts (unit)",
      "tests/integration/auth.test.ts",
      "tests/e2e/login.spec.ts"
    ]
  }
}
```

---

### Category 4: Annotations and Decorators

#### 4.1 Custom Decorator/Annotation Detection

**Algorithm:**

```
1. Search for decorator definitions and usages
2. Separate framework decorators from custom ones
3. Document decorator purposes based on naming and usage
```

**Decorator Detection Patterns:**

| Language | Definition Pattern | Usage Pattern |
|----------|-------------------|---------------|
| TypeScript | `function decoratorName(target: any)` | `@decoratorName` |
| Python | `def decorator_name(func)` | `@decorator_name` |
| Java | `@interface AnnotationName` | `@AnnotationName` |
| C# | `[AttributeUsage]` class | `[AttributeName]` |

**Framework Decorators to Exclude:**

| Framework | Common Decorators |
|-----------|-------------------|
| NestJS | `@Controller`, `@Injectable`, `@Get`, `@Post` |
| Angular | `@Component`, `@Input`, `@Output` |
| TypeORM | `@Entity`, `@Column`, `@PrimaryGeneratedColumn` |
| Spring | `@Autowired`, `@Component`, `@RequestMapping` |
| Django | `@login_required`, `@permission_required` |

**Output:**

```json
{
  "custom_decorators": [
    {
      "name": "@Cacheable",
      "file": "src/decorators/cache.ts",
      "purpose": "Method-level caching",
      "confidence": "HIGH",
      "usage_count": 12,
      "examples": [
        "@Cacheable({ ttl: 3600 })",
        "Applied to service methods"
      ]
    },
    {
      "name": "@Validate",
      "file": "src/decorators/validate.ts",
      "purpose": "Input validation",
      "confidence": "HIGH",
      "usage_count": 8,
      "examples": [
        "@Validate(userSchema)",
        "Applied to controller methods"
      ]
    }
  ]
}
```

#### 4.2 Documentation Annotation Detection

**Algorithm:**

```
1. Search for documentation comment patterns
2. Analyze documentation style and completeness
3. Identify custom documentation tags
```

**Documentation Patterns:**

| Language | Pattern | Example |
|----------|---------|---------|
| TypeScript/JS | JSDoc `/** ... */` | `@param`, `@returns`, `@example` |
| Python | Docstrings `"""..."""` | Google, NumPy, or Sphinx style |
| Go | GoDoc `// FunctionName ...` | Package and function comments |
| Java | Javadoc `/** ... */` | `@param`, `@return`, `@throws` |
| Rust | Doc comments `///` | `# Examples`, `# Panics` |
| C# | XML comments `///` | `<summary>`, `<param>`, `<returns>` |

**Output:**

```json
{
  "documentation_annotations": {
    "style": "JSDoc",
    "confidence": "HIGH",
    "coverage": {
      "public_functions": "85%",
      "classes": "90%",
      "interfaces": "75%"
    },
    "custom_tags": [
      "@internal - marks private API",
      "@deprecated - marks deprecated code",
      "@see - links to related code"
    ],
    "examples": [
      "/**\n * Creates a new user\n * @param data - User creation data\n * @returns The created user\n */"
    ]
  }
}
```

---

### Category 5: API Patterns

#### 5.1 REST Endpoint Convention Detection

**Algorithm:**

```
1. Search for route/endpoint definitions
2. Analyze URL patterns and HTTP method usage
3. Detect versioning strategy
```

**Route Detection Patterns:**

| Framework | Pattern |
|-----------|---------|
| Express | `app.get()`, `router.post()`, `@Get()` |
| FastAPI | `@app.get()`, `@router.post()` |
| NestJS | `@Get()`, `@Post()`, `@Controller()` |
| Spring | `@GetMapping`, `@PostMapping`, `@RequestMapping` |
| Go (Gin) | `r.GET()`, `r.POST()`, `router.Handle()` |
| Django | `path()`, `urlpatterns` |
| Rails | `resources :users`, `get '/path'` |

**Naming Patterns to Detect:**

| Convention | Example | Pattern |
|------------|---------|---------|
| Plural nouns | `/users`, `/orders` | Collection endpoints |
| Nested resources | `/users/:id/orders` | Relationship modeling |
| Kebab-case | `/user-profiles` | Multi-word resources |
| snake_case | `/user_profiles` | Multi-word resources |
| Version prefix | `/api/v1/users` | API versioning |
| Query params | `/users?status=active` | Filtering |

**Output:**

```json
{
  "rest_conventions": {
    "resource_naming": "plural_nouns",
    "case_style": "kebab-case",
    "confidence": "HIGH",
    "versioning": {
      "strategy": "url_prefix",
      "format": "/api/v1/"
    },
    "patterns": [
      "Plural nouns for collections",
      "Nested routes for relationships",
      "Query params for filtering"
    ],
    "examples": [
      "GET /api/v1/users",
      "GET /api/v1/users/:id/orders",
      "POST /api/v1/orders"
    ]
  }
}
```

#### 5.2 Response Format Detection

**Algorithm:**

```
1. Search for response structure definitions (DTOs, schemas)
2. Analyze actual response building code
3. Detect error response patterns
```

**Response Pattern Indicators:**

| Pattern | Indicators |
|---------|------------|
| Envelope pattern | `{ data: ..., meta: ..., errors: ... }` |
| Direct response | Return entity directly |
| HAL | `_links`, `_embedded` |
| JSON:API | `data`, `included`, `relationships` |
| Custom wrapper | Project-specific wrapper class |

**Output:**

```json
{
  "response_format": {
    "pattern": "envelope",
    "confidence": "HIGH",
    "structure": {
      "success": "{ data: T, meta?: { ... } }",
      "error": "{ error: { code: string, message: string, details?: any } }"
    },
    "pagination": {
      "style": "cursor-based",
      "fields": ["cursor", "limit", "hasMore"]
    },
    "examples": [
      "{ data: [...users], meta: { total: 100, cursor: 'abc' } }",
      "{ error: { code: 'NOT_FOUND', message: 'User not found' } }"
    ]
  }
}
```

#### 5.3 Error Handling Convention Detection

**Algorithm:**

```
1. Search for error handling middleware/interceptors
2. Analyze exception/error class definitions
3. Detect error code patterns
```

**Error Pattern Indicators:**

| Pattern | Code Indicators |
|---------|-----------------|
| Custom exceptions | `class *Exception extends Error`, `class *Error extends` |
| Error codes | `enum ErrorCode`, `const ERROR_CODES` |
| HTTP status mapping | `HttpStatus`, status code constants |
| Error middleware | `errorHandler()`, `@Catch()`, `@ExceptionHandler` |

**Output:**

```json
{
  "error_handling": {
    "pattern": "custom_exceptions",
    "confidence": "HIGH",
    "error_classes": [
      "ValidationError",
      "NotFoundError",
      "UnauthorizedError"
    ],
    "error_codes": {
      "format": "SCREAMING_SNAKE_CASE",
      "examples": ["VALIDATION_ERROR", "NOT_FOUND", "UNAUTHORIZED"]
    },
    "http_mapping": {
      "ValidationError": 400,
      "NotFoundError": 404,
      "UnauthorizedError": 401
    },
    "examples": [
      "throw new ValidationError('Invalid email')",
      "catch (error) { next(error) }"
    ]
  }
}
```

---

### Category 6: Configuration Patterns

#### 6.1 Configuration File Detection

**Algorithm:**

```
1. Scan for configuration files by extension and name
2. Analyze configuration structure and format
3. Detect environment-specific configurations
```

**Configuration Files:**

| File Pattern | Type | Purpose |
|--------------|------|---------|
| `config/*.ts`, `config/*.js` | Code | App configuration |
| `*.config.ts`, `*.config.js` | Code | Tool configuration |
| `.env`, `.env.*` | Env | Environment variables |
| `config/*.yaml`, `config/*.yml` | YAML | App configuration |
| `settings.json`, `config.json` | JSON | Static configuration |
| `appsettings.json` | JSON | .NET configuration |
| `application.yml` | YAML | Spring configuration |

**Output:**

```json
{
  "configuration_files": {
    "primary_format": "TypeScript",
    "confidence": "HIGH",
    "files": [
      {
        "path": "src/config/app.config.ts",
        "purpose": "Application settings"
      },
      {
        "path": "src/config/database.config.ts",
        "purpose": "Database connection"
      }
    ],
    "environment_configs": [
      ".env",
      ".env.development",
      ".env.production"
    ]
  }
}
```

#### 6.2 Environment Variable Pattern Detection

**Algorithm:**

```
1. Parse .env files and environment variable usage
2. Detect naming conventions
3. Identify required vs optional variables
```

**Environment Variable Patterns:**

| Pattern | Example | Convention |
|---------|---------|------------|
| SCREAMING_SNAKE | `DATABASE_URL` | Standard |
| Prefixed | `APP_DATABASE_URL` | Namespaced |
| Nested dots | `database.url` | Hierarchical |

**Output:**

```json
{
  "environment_variables": {
    "naming_convention": "SCREAMING_SNAKE_CASE",
    "prefix": "APP_",
    "confidence": "HIGH",
    "categories": {
      "database": ["DATABASE_URL", "DATABASE_POOL_SIZE"],
      "auth": ["JWT_SECRET", "SESSION_TTL"],
      "external": ["STRIPE_API_KEY", "SENDGRID_KEY"]
    },
    "validation": {
      "detected": true,
      "library": "zod",
      "file": "src/config/env.ts"
    },
    "examples": [
      "APP_DATABASE_URL=postgresql://...",
      "APP_JWT_SECRET=secret"
    ]
  }
}
```

#### 6.3 Build Tool Configuration Detection

**Algorithm:**

```
1. Identify build tool from manifest files
2. Analyze build configuration structure
3. Detect build scripts and targets
```

**Build Tool Indicators:**

| Tool | Configuration Files |
|------|---------------------|
| Vite | `vite.config.ts` |
| Webpack | `webpack.config.js` |
| Rollup | `rollup.config.js` |
| esbuild | `esbuild.config.js`, build scripts |
| Next.js | `next.config.js` |
| Turbopack | `turbo.json` |
| Make | `Makefile` |
| Gradle | `build.gradle`, `build.gradle.kts` |
| Maven | `pom.xml` |

**Output:**

```json
{
  "build_tools": {
    "primary": "Vite",
    "confidence": "HIGH",
    "config_file": "vite.config.ts",
    "features": [
      "TypeScript support",
      "Path aliases",
      "Environment variable handling"
    ],
    "scripts": {
      "dev": "vite",
      "build": "vite build",
      "preview": "vite preview"
    }
  }
}
```

#### 6.4 CI/CD Pipeline Detection

**Algorithm:**

```
1. Search for CI/CD configuration files
2. Analyze pipeline stages and steps
3. Identify deployment targets
```

**CI/CD Files:**

| File/Directory | Platform |
|----------------|----------|
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `.travis.yml` | Travis CI |
| `azure-pipelines.yml` | Azure DevOps |
| `bitbucket-pipelines.yml` | Bitbucket |
| `.drone.yml` | Drone CI |

**Output:**

```json
{
  "ci_cd": {
    "platform": "GitHub Actions",
    "confidence": "HIGH",
    "workflows": [
      {
        "name": "CI",
        "file": ".github/workflows/ci.yml",
        "triggers": ["push", "pull_request"],
        "stages": ["lint", "test", "build"]
      },
      {
        "name": "Deploy",
        "file": ".github/workflows/deploy.yml",
        "triggers": ["push to main"],
        "stages": ["build", "deploy"]
      }
    ],
    "deployment_targets": ["Vercel", "AWS"]
  }
}
```

---

## Confidence Scoring

### Per-Category Confidence

Each category calculates confidence independently:

| Level | Score | Criteria |
|-------|-------|----------|
| **HIGH** | 80-100 | Multiple strong indicators, consistent patterns |
| **MEDIUM** | 50-79 | Some indicators found, minor inconsistencies |
| **LOW** | 20-49 | Few indicators, patterns unclear |
| **UNCERTAIN** | <20 | Insufficient data for reliable detection |

### Scoring Algorithm

```
For each category:
  indicators_found = count matching patterns
  consistency_score = measure pattern consistency (0-1)
  coverage_score = files_with_pattern / total_relevant_files

  category_score = (
    indicators_found * 10 +
    consistency_score * 40 +
    coverage_score * 50
  )

  confidence = map_to_level(category_score)
```

### Overall Analysis Confidence

```
overall_confidence = weighted_average(category_confidences)

where weights are:
  - Code Conventions: 1.0
  - Architecture: 1.0
  - Testing: 0.8
  - Annotations: 0.6
  - API Patterns: 0.8
  - Configuration: 0.7
```

---

## Output Format

The protocol produces a JSON analysis result:

```json
{
  "analyzed_at": "2026-01-28T10:30:00Z",
  "overall_confidence": "HIGH",
  "overall_score": 85,
  "categories": {
    "code_conventions": {
      "confidence": "HIGH",
      "score": 90,
      "patterns": { /* ... */ }
    },
    "architecture": {
      "confidence": "HIGH",
      "score": 85,
      "patterns": { /* ... */ }
    },
    "testing": {
      "confidence": "MEDIUM",
      "score": 70,
      "patterns": { /* ... */ }
    },
    "annotations": {
      "confidence": "LOW",
      "score": 40,
      "patterns": { /* ... */ }
    },
    "api_patterns": {
      "confidence": "HIGH",
      "score": 88,
      "patterns": { /* ... */ }
    },
    "configuration": {
      "confidence": "HIGH",
      "score": 82,
      "patterns": { /* ... */ }
    }
  },
  "summary": {
    "total_files_analyzed": 245,
    "patterns_detected": 32,
    "high_confidence_patterns": 24,
    "recommendations": [
      "Consider documenting the Cacheable decorator usage",
      "Test coverage detection was limited - ensure tests follow consistent naming"
    ]
  }
}
```

---

## Integration with Setup Command

### Execution Flow

```
1. Stack Detection Protocol completes
2. Codebase Analysis Protocol begins
3. Analysis runs for each category
4. Results aggregated into single JSON structure
5. User presented with consolidated review
6. Approved categories generate documentation
```

### Handoff to Documentation Generation

After analysis, pass results to documentation generation:

```
Input: Analysis JSON result
Output:
  - CLAUDE.md (progressive disclosure format)
  - conductor/docs/code-conventions.md
  - conductor/docs/architecture.md
  - conductor/docs/testing.md
  - conductor/docs/api-patterns.md
  - conductor/docs/configuration.md
  - conductor/docs/annotations.md (if applicable)
```

---

## Performance Considerations

### File Sampling Strategy

For large codebases (>1000 files per category):

```
1. Sample first 100 files by modification date (most recently modified)
2. Sample 50 files from each major directory
3. Sample files matching key patterns (e.g., *Service.ts, *Controller.ts)
4. Maximum 500 files per category
```

### Large File Handling

For files >500 lines:

```
1. Read first 100 lines (imports, class definitions)
2. Read last 50 lines (exports, module patterns)
3. Search middle section for specific patterns only if needed
```

### Timeout Protection

```
- Maximum 60 seconds for complete analysis
- 10 seconds per category maximum
- Early termination with partial results if timeout approaches
```

---

## Fallback Behavior

### When Analysis Fails

```
1. Return partial results with notes
2. Mark failed categories as "UNCERTAIN"
3. Continue with successfully analyzed categories
4. Add recommendation to manually review failed categories
```

### When No Patterns Detected

```
1. Return empty category with UNCERTAIN confidence
2. Do not generate documentation for empty categories
3. Add note suggesting this may be a new project or unusual structure
```

---

## Appendix: Detection Commands Reference

### Code Conventions
```bash
# File naming analysis
find src -type f -name "*.ts" -o -name "*.js" | head -100

# Import pattern analysis
grep -h "^import\|^from" src/**/*.ts | head -50

# Barrel file detection
find src -name "index.ts" -o -name "index.js"
```

### Architecture
```bash
# Repository pattern
grep -rl "Repository" --include="*.ts" src/

# Layer directories
ls -d src/*/ 2>/dev/null | grep -E "domain|application|infrastructure|presentation"
```

### Testing
```bash
# Test files
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*_test.go"

# Test framework usage
grep -r "describe\|it\|test\|expect" --include="*.test.ts" | head -20
```

### Annotations
```bash
# Decorator definitions
grep -r "function.*decorator\|@[A-Z]" --include="*.ts" src/

# Custom decorators
grep -rh "^export function [a-z].*target" --include="*.ts" src/decorators/
```

### API Patterns
```bash
# Route definitions
grep -r "@Get\|@Post\|app\.get\|router\." --include="*.ts" src/

# Response patterns
grep -r "return.*data:\|res\.json" --include="*.ts" src/
```

### Configuration
```bash
# Config files
find . -name "*.config.ts" -o -name "*.config.js" -o -name ".env*"

# CI/CD
ls -la .github/workflows/ .gitlab-ci.yml Jenkinsfile 2>/dev/null
```
