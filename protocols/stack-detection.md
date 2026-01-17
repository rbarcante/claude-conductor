# Stack Detection Protocol

**Version:** 1.0.0
**Purpose:** Automatically detect and profile the technology stack of a project
**Scope:** Conductor setup command, brownfield project initialization

---

## Overview

This protocol defines the algorithm and process for detecting a project's technology stack through static analysis of manifest files, file extensions, and dependency patterns. The output is a structured JSON profile that can be used to pre-populate `tech-stack.md` and activate relevant skills.

---

## Detection Algorithm

### Step 1: Scan for Manifest Files

Scan the project root (and up to 2 levels deep for monorepos) for the following manifest file signatures:

| Manifest File | Primary Technology | Ecosystem |
|---------------|-------------------|-----------|
| `package.json` | Node.js/JavaScript | npm/yarn |
| `package-lock.json` | Node.js | npm |
| `yarn.lock` | Node.js | yarn |
| `pnpm-lock.yaml` | Node.js | pnpm |
| `pom.xml` | Java | Maven |
| `build.gradle` | Java/Kotlin | Gradle |
| `build.gradle.kts` | Kotlin | Gradle |
| `requirements.txt` | Python | pip |
| `pyproject.toml` | Python | Poetry/pip |
| `setup.py` | Python | setuptools |
| `Pipfile` | Python | pipenv |
| `go.mod` | Go | Go modules |
| `go.sum` | Go | Go modules |
| `Cargo.toml` | Rust | Cargo |
| `Cargo.lock` | Rust | Cargo |
| `composer.json` | PHP | Composer |
| `Gemfile` | Ruby | Bundler |
| `Gemfile.lock` | Ruby | Bundler |
| `pubspec.yaml` | Dart | pub |
| `*.csproj` | C# | .NET |
| `*.fsproj` | F# | .NET |
| `*.sln` | .NET | Visual Studio |
| `CMakeLists.txt` | C/C++ | CMake |
| `Makefile` | C/C++/Generic | Make |
| `tsconfig.json` | TypeScript | TypeScript |
| `deno.json` | TypeScript/Deno | Deno |
| `mix.exs` | Elixir | Mix |
| `rebar.config` | Erlang | Rebar |
| `stack.yaml` | Haskell | Stack |
| `*.cabal` | Haskell | Cabal |
| `build.sbt` | Scala | sbt |
| `project.clj` | Clojure | Leiningen |
| `deps.edn` | Clojure | deps.edn |

### Step 2: Analyze File Extensions

Count files by extension to determine language distribution:

| Extensions | Language | Weight |
|------------|----------|--------|
| `.js`, `.jsx`, `.mjs`, `.cjs` | JavaScript | 1.0 |
| `.ts`, `.tsx`, `.mts`, `.cts` | TypeScript | 1.0 |
| `.py`, `.pyi` | Python | 1.0 |
| `.go` | Go | 1.0 |
| `.rs` | Rust | 1.0 |
| `.java` | Java | 1.0 |
| `.kt`, `.kts` | Kotlin | 1.0 |
| `.rb`, `.erb` | Ruby | 1.0 |
| `.php` | PHP | 1.0 |
| `.cs` | C# | 1.0 |
| `.fs`, `.fsx` | F# | 1.0 |
| `.dart` | Dart | 1.0 |
| `.swift` | Swift | 1.0 |
| `.c`, `.h` | C | 1.0 |
| `.cpp`, `.hpp`, `.cc`, `.hh` | C++ | 1.0 |
| `.ex`, `.exs` | Elixir | 1.0 |
| `.erl`, `.hrl` | Erlang | 1.0 |
| `.hs` | Haskell | 1.0 |
| `.scala`, `.sc` | Scala | 1.0 |
| `.clj`, `.cljs`, `.cljc` | Clojure | 1.0 |
| `.vue` | Vue.js | 0.8 |
| `.svelte` | Svelte | 0.8 |
| `.astro` | Astro | 0.8 |

**Exclusions:** Skip directories: `node_modules`, `vendor`, `venv`, `.venv`, `__pycache__`, `target`, `build`, `dist`, `.git`, `.svn`, `bin`, `obj`.

### Step 3: Detect Frameworks

Parse manifest files to identify frameworks from dependencies:

#### JavaScript/TypeScript Frameworks

**Frontend Frameworks** (check `dependencies` and `devDependencies` in `package.json`):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `react`, `react-dom` | React | Frontend |
| `next` | Next.js | Frontend/Fullstack |
| `vue` | Vue.js | Frontend |
| `nuxt` | Nuxt.js | Frontend/Fullstack |
| `@angular/core` | Angular | Frontend |
| `svelte` | Svelte | Frontend |
| `@sveltejs/kit` | SvelteKit | Frontend/Fullstack |
| `solid-js` | Solid.js | Frontend |
| `preact` | Preact | Frontend |
| `astro` | Astro | Frontend |
| `gatsby` | Gatsby | Frontend |
| `remix` | Remix | Frontend/Fullstack |

**Backend Frameworks** (check `dependencies` in `package.json`):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `express` | Express.js | Backend |
| `fastify` | Fastify | Backend |
| `@nestjs/core` | NestJS | Backend |
| `koa` | Koa | Backend |
| `hapi`, `@hapi/hapi` | Hapi | Backend |
| `hono` | Hono | Backend |
| `elysia` | Elysia | Backend |

**Build Tools** (check `devDependencies` in `package.json`):

| Dependency Pattern | Tool | Category |
|--------------------|------|----------|
| `webpack` | Webpack | Bundler |
| `vite` | Vite | Bundler |
| `esbuild` | esbuild | Bundler |
| `rollup` | Rollup | Bundler |
| `parcel` | Parcel | Bundler |
| `turbo` | Turborepo | Monorepo |
| `nx` | Nx | Monorepo |
| `lerna` | Lerna | Monorepo |

**Testing Frameworks** (check `devDependencies` in `package.json`):

| Dependency Pattern | Tool | Category |
|--------------------|------|----------|
| `jest` | Jest | Testing |
| `vitest` | Vitest | Testing |
| `mocha` | Mocha | Testing |
| `cypress` | Cypress | E2E Testing |
| `playwright`, `@playwright/test` | Playwright | E2E Testing |
| `puppeteer` | Puppeteer | E2E Testing |

#### Python Frameworks

**Check** `requirements.txt`, `pyproject.toml` (`[tool.poetry.dependencies]` or `[project.dependencies]`), or `setup.py`:

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `django` | Django | Backend/Fullstack |
| `flask` | Flask | Backend |
| `fastapi` | FastAPI | Backend |
| `starlette` | Starlette | Backend |
| `tornado` | Tornado | Backend |
| `pyramid` | Pyramid | Backend |
| `aiohttp` | aiohttp | Backend |
| `pytest` | pytest | Testing |
| `unittest` | unittest | Testing |
| `celery` | Celery | Task Queue |
| `pandas` | pandas | Data Science |
| `numpy` | numpy | Scientific |
| `tensorflow`, `keras` | TensorFlow | ML/AI |
| `torch`, `pytorch` | PyTorch | ML/AI |
| `scikit-learn`, `sklearn` | scikit-learn | ML |

#### Java Frameworks

**Check** `pom.xml` (`<dependencies>`) or `build.gradle` (`dependencies` block):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `spring-boot` | Spring Boot | Backend |
| `spring-webflux` | Spring WebFlux | Backend |
| `quarkus` | Quarkus | Backend |
| `micronaut` | Micronaut | Backend |
| `hibernate` | Hibernate | ORM |
| `junit` | JUnit | Testing |
| `mockito` | Mockito | Testing |

#### Go Frameworks

**Check** `go.mod` (`require` block):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `github.com/gin-gonic/gin` | Gin | Backend |
| `github.com/labstack/echo` | Echo | Backend |
| `github.com/gofiber/fiber` | Fiber | Backend |
| `github.com/gorilla/mux` | Gorilla Mux | Router |
| `github.com/go-chi/chi` | Chi | Router |
| `gorm.io/gorm` | GORM | ORM |
| `github.com/stretchr/testify` | Testify | Testing |

#### Ruby Frameworks

**Check** `Gemfile`:

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `rails` | Ruby on Rails | Backend/Fullstack |
| `sinatra` | Sinatra | Backend |
| `hanami` | Hanami | Backend |
| `rspec` | RSpec | Testing |
| `sidekiq` | Sidekiq | Background Jobs |

#### PHP Frameworks

**Check** `composer.json` (`require` block):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `laravel/framework` | Laravel | Backend/Fullstack |
| `symfony/` | Symfony | Backend |
| `slim/slim` | Slim | Backend |
| `phpunit/phpunit` | PHPUnit | Testing |

#### Rust Frameworks

**Check** `Cargo.toml` (`[dependencies]`):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `actix-web` | Actix Web | Backend |
| `axum` | Axum | Backend |
| `rocket` | Rocket | Backend |
| `warp` | Warp | Backend |
| `tokio` | Tokio | Async Runtime |
| `diesel` | Diesel | ORM |
| `sqlx` | SQLx | Database |

#### Dart/Flutter Frameworks

**Check** `pubspec.yaml` (`dependencies`):

| Dependency Pattern | Framework | Category |
|--------------------|-----------|----------|
| `flutter` | Flutter | Mobile/Desktop |
| `shelf` | Shelf | Backend |

### Step 4: Detect Infrastructure & Tools

Scan for configuration files that indicate infrastructure patterns:

| File/Directory | Technology | Category |
|----------------|-----------|----------|
| `Dockerfile`, `docker-compose.yml` | Docker | Containerization |
| `kubernetes/`, `k8s/`, `*.yaml` (with k8s markers) | Kubernetes | Orchestration |
| `.github/workflows/` | GitHub Actions | CI/CD |
| `.gitlab-ci.yml` | GitLab CI | CI/CD |
| `Jenkinsfile` | Jenkins | CI/CD |
| `.circleci/` | CircleCI | CI/CD |
| `terraform/`, `*.tf` | Terraform | IaC |
| `pulumi/`, `Pulumi.yaml` | Pulumi | IaC |
| `serverless.yml` | Serverless Framework | IaC |
| `.eslintrc*`, `eslint.config.*` | ESLint | Linting |
| `.prettierrc*`, `prettier.config.*` | Prettier | Formatting |
| `tailwind.config.*` | Tailwind CSS | Styling |
| `.env`, `.env.*` | Environment Variables | Config |
| `prisma/schema.prisma` | Prisma | ORM |
| `drizzle.config.*` | Drizzle | ORM |

### Step 5: Calculate Confidence Score

**Confidence Levels:**

| Level | Score Range | Criteria |
|-------|-------------|----------|
| **HIGH** | 85-100% | Manifest file found AND framework dependencies detected AND file extensions match |
| **MEDIUM** | 60-84% | Manifest file found AND (framework detected OR significant file extension count) |
| **LOW** | 30-59% | Only file extensions OR partial manifest (e.g., lockfile without manifest) |
| **UNCERTAIN** | <30% | Minimal signals, manual verification strongly recommended |

**Scoring Algorithm:**

```
Base Score = 0

IF manifest_file_found:
    Base Score += 40

IF framework_detected:
    Base Score += 30

IF file_extension_count > 5 AND matches_manifest_ecosystem:
    Base Score += 20

IF config_files_found (tsconfig, eslint, docker, etc.):
    Base Score += 10

Final Score = min(Base Score, 100)
```

**Confidence Assignment:**
- Score >= 85: `"HIGH"`
- Score >= 60: `"MEDIUM"`
- Score >= 30: `"LOW"`
- Score < 30: `"UNCERTAIN"`

---

## Detection Process

### Protocol Execution Steps

```
1. INITIALIZE
   - Set working directory to project root
   - Initialize empty stack profile
   - Set confidence score to 0

2. SCAN MANIFEST FILES
   - Search for manifest files (Step 1 table)
   - For each found manifest:
     a. Parse file contents
     b. Extract ecosystem identifier
     c. Add to manifest_files list
     d. Increment confidence score (+40 for first manifest)

3. ANALYZE FILE EXTENSIONS
   - Recursively scan project (excluding blacklisted dirs)
   - Count files by extension
   - Map extensions to languages (Step 2 table)
   - Determine primary language (highest count)
   - Add all detected languages to languages list

4. DETECT FRAMEWORKS
   - For each manifest file:
     a. Parse dependency declarations
     b. Match against framework patterns (Step 3 tables)
     c. Add matched frameworks to frameworks list
     d. Increment confidence score (+30 if any framework found)

5. DETECT INFRASTRUCTURE
   - Scan for infrastructure config files (Step 4 table)
   - Add detected tools to build_tools or infra list
   - Increment confidence score (+10 for infrastructure detection)

6. CALCULATE FINAL CONFIDENCE
   - Apply scoring algorithm (Step 5)
   - Assign confidence level string

7. GENERATE PROFILE
   - Compile all detected information into JSON profile
   - Add timestamp
   - Add any notes or warnings

8. RETURN PROFILE
   - Output JSON stack profile
   - If confidence is LOW or UNCERTAIN, add note recommending verification
```

---

## Output Format

The protocol produces a JSON stack profile with the following schema:

```json
{
  "detected_at": "2026-01-20T10:30:00Z",
  "confidence": "HIGH",
  "confidence_score": 90,
  "primary_language": "TypeScript",
  "languages": [
    {
      "name": "TypeScript",
      "file_count": 45,
      "percentage": 75
    },
    {
      "name": "JavaScript",
      "file_count": 10,
      "percentage": 17
    },
    {
      "name": "CSS",
      "file_count": 5,
      "percentage": 8
    }
  ],
  "frameworks": [
    {
      "name": "React",
      "version": "18.2.0",
      "category": "Frontend"
    },
    {
      "name": "Express.js",
      "version": "4.18.2",
      "category": "Backend"
    }
  ],
  "build_tools": [
    {
      "name": "Vite",
      "version": "5.0.0",
      "category": "Bundler"
    },
    {
      "name": "ESLint",
      "category": "Linting"
    }
  ],
  "testing_frameworks": [
    {
      "name": "Vitest",
      "version": "1.0.0"
    }
  ],
  "infrastructure": [
    {
      "name": "Docker",
      "category": "Containerization"
    },
    {
      "name": "GitHub Actions",
      "category": "CI/CD"
    }
  ],
  "manifest_files": [
    "package.json",
    "tsconfig.json"
  ],
  "package_manager": "npm",
  "monorepo": false,
  "notes": []
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `detected_at` | string (ISO 8601) | Yes | Timestamp of detection |
| `confidence` | enum | Yes | `HIGH`, `MEDIUM`, `LOW`, or `UNCERTAIN` |
| `confidence_score` | number | Yes | Numeric score 0-100 |
| `primary_language` | string | Yes | Most prevalent language |
| `languages` | array | Yes | All detected languages with counts |
| `frameworks` | array | Yes | Detected frameworks with versions when available |
| `build_tools` | array | Yes | Build tools, bundlers, task runners |
| `testing_frameworks` | array | No | Testing tools |
| `infrastructure` | array | No | CI/CD, containers, IaC tools |
| `manifest_files` | array | Yes | List of found manifest files |
| `package_manager` | string | No | Detected package manager |
| `monorepo` | boolean | No | Whether project appears to be a monorepo |
| `notes` | array | Yes | Warnings, recommendations, or observations |

---

## Fallback Behavior

### When Confidence is LOW or UNCERTAIN

1. **Add Warning Note:**
   ```json
   {
     "notes": [
       "Low confidence detection. Manual verification recommended.",
       "Consider running stack detection again after adding project dependencies."
     ]
   }
   ```

2. **Prompt User for Verification:**
   - Display detected stack to user
   - Ask for confirmation or corrections
   - Allow manual override of any field

3. **Accept User Input:**
   - Store user-provided corrections
   - Use corrected values for tech-stack.md generation

### When No Stack is Detected

1. **Return Minimal Profile:**
   ```json
   {
     "detected_at": "2026-01-20T10:30:00Z",
     "confidence": "UNCERTAIN",
     "confidence_score": 0,
     "primary_language": "Unknown",
     "languages": [],
     "frameworks": [],
     "build_tools": [],
     "manifest_files": [],
     "notes": [
       "No technology stack detected. This may be a new project or use an unsupported technology.",
       "Please manually specify your technology stack."
     ]
   }
   ```

2. **Trigger Manual Input Flow:**
   - Ask user to specify primary language
   - Ask for frameworks being used
   - Proceed with user-provided information

### Conflict Resolution

When multiple conflicting signals are detected:

1. **Manifest Files Take Precedence:**
   - If `package.json` exists, JavaScript/TypeScript ecosystem is primary
   - File extensions are secondary evidence

2. **Most Specific Wins:**
   - `tsconfig.json` + `.ts` files = TypeScript (not JavaScript)
   - Framework-specific configs override generic detection

3. **Add Note for Ambiguity:**
   ```json
   {
     "notes": [
       "Multiple ecosystems detected. Project may be polyglot or in transition."
     ]
   }
   ```

---

## Integration Points

### With Setup Command

The stack detection protocol is invoked during the `conductor:setup` command:

1. After project inception dialog
2. Before tech-stack.md generation
3. Results pre-populate tech-stack template

### With Skill Activation

The stack profile is used for skill matching:

1. `primary_language` matches skill activation rules
2. `frameworks` array matches framework-specific skills
3. Skills can specify required confidence level

### With Tech-Stack.md

The profile maps to tech-stack.md sections:

| Profile Field | Tech-Stack Section |
|---------------|-------------------|
| `primary_language` | Primary Language |
| `languages` | Languages |
| `frameworks` | Frameworks |
| `build_tools` | Build & Development |
| `testing_frameworks` | Testing |
| `infrastructure` | Infrastructure |

---

## Appendix: Extension Reference

### Complete File Extension Mapping

```
JavaScript:     .js, .jsx, .mjs, .cjs
TypeScript:     .ts, .tsx, .mts, .cts, .d.ts
Python:         .py, .pyi, .pyw
Go:             .go
Rust:           .rs
Java:           .java
Kotlin:         .kt, .kts
Ruby:           .rb, .erb, .rake
PHP:            .php, .phtml
C#:             .cs
F#:             .fs, .fsx, .fsi
Dart:           .dart
Swift:          .swift
C:              .c, .h
C++:            .cpp, .hpp, .cc, .hh, .cxx, .hxx
Objective-C:    .m, .mm
Elixir:         .ex, .exs
Erlang:         .erl, .hrl
Haskell:        .hs, .lhs
Scala:          .scala, .sc
Clojure:        .clj, .cljs, .cljc, .edn
Lua:            .lua
Perl:           .pl, .pm
R:              .r, .R
Shell:          .sh, .bash, .zsh
PowerShell:     .ps1, .psm1
SQL:            .sql
HTML:           .html, .htm
CSS:            .css
SCSS/Sass:      .scss, .sass
Less:           .less
Vue:            .vue
Svelte:         .svelte
Astro:          .astro
Markdown:       .md, .mdx
JSON:           .json
YAML:           .yml, .yaml
TOML:           .toml
XML:            .xml
```

### Excluded Directories

```
node_modules/
vendor/
venv/
.venv/
env/
__pycache__/
.pytest_cache/
target/
build/
dist/
out/
.git/
.svn/
.hg/
bin/
obj/
.idea/
.vscode/
*.egg-info/
.tox/
.nox/
coverage/
.nyc_output/
```
