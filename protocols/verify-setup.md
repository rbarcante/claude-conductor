# Verify Setup Protocol

> **Purpose:** Verify that the Conductor environment is properly set up before executing commands that depend on project context.
>
> This protocol ensures core project files exist before proceeding with track creation or implementation.

---

## Required Files

The following files must exist for Conductor to be considered "set up":

| File | Resolution Key | Purpose |
|------|----------------|---------|
| Product Definition | `product_definition` | Project vision, goals, and scope |
| Tech Stack | `tech_stack` | Technology decisions and architecture |
| Workflow | `workflow` | Task lifecycle and TDD methodology |

---

## Protocol Steps

### Step 1: Resolve File Paths

Using the **Universal File Resolution Protocol** (defined in CLAUDE.md):

1. Resolve the path for **Product Definition**
2. Resolve the path for **Tech Stack**
3. Resolve the path for **Workflow**

### Step 2: Verify Existence

For each resolved path, verify the file exists on disk.

### Step 3: Handle Results

**If ALL files exist:**
- Setup verification passes
- Proceed to the next section of the calling command

**If ANY file is missing:**
1. Identify which file(s) are missing
2. Announce: "Conductor is not set up. Missing: `<file_list>`. Please run `/conductor:setup` to set up the environment."
3. **HALT** - Do not proceed with the command

---

## Example Usage

```
Checking Conductor setup...
✓ Product Definition: conductor/product.md
✓ Tech Stack: conductor/tech-stack.md
✓ Workflow: conductor/workflow.md
Setup verified. Proceeding...
```

Or on failure:

```
Checking Conductor setup...
✓ Product Definition: conductor/product.md
✗ Tech Stack: NOT FOUND
✗ Workflow: NOT FOUND

Conductor is not set up. Please run `/conductor:setup` to set up the environment.
[HALT]
```
