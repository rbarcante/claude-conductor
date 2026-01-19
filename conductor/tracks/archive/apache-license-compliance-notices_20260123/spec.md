# Specification: Apache License Compliance Notices

## Overview

Add prominent modification notices to all files derived from the original Conductor for Gemini CLI project to comply with Apache License 2.0 Section 4(b): "You must cause any modified files to carry prominent notices stating that You changed the files."

## Background

The Claude Conductor project is derived from the [Conductor for Gemini CLI](https://github.com/gemini-cli-extensions/conductor) project, which is licensed under Apache 2.0. As a derivative work, we must:
1. Include a copy of the Apache 2.0 license (already present as LICENSE)
2. Add prominent modification notices to changed files
3. Retain original copyright and attribution notices

## Functional Requirements

### FR-1: License Header Format
Each modified file shall include the following header at the top of the file:

**For Markdown files:**
```markdown
<!--
  Copyright 2025 Ricardo Barcante

  Derived from Conductor for Gemini CLI (https://github.com/gemini-cli-extensions/conductor)
  Copyright 2024 Google LLC

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  NOTICE: This file has been modified from the original.
-->
```

**For Python files:**
```python
# Copyright 2025 Ricardo Barcante
#
# Derived from Conductor for Gemini CLI (https://github.com/gemini-cli-extensions/conductor)
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTICE: This file has been modified from the original.
```

**For JSON files:**
Since JSON does not support comments, add a `_license` field at the root level:
```json
{
  "_license": "Apache-2.0. Derived from Conductor for Gemini CLI. See LICENSE.",
  ...
}
```

### FR-2: Files Requiring Modification Notices

The following file categories derived from the original project require notices:

1. **Command files** (`commands/*.md`):
   - setup.md
   - implement.md
   - newTrack.md
   - status.md
   - revert.md

2. **Template files** (`templates/`):
   - workflow.md
   - code_styleguides/general.md
   - code_styleguides/typescript.md
   - code_styleguides/javascript.md
   - code_styleguides/python.md
   - code_styleguides/go.md

3. **Script files** (`scripts/`):
   - conductor_cli.py (and any other Python files)

4. **Configuration files**:
   - plugin.json (use _license field)

### FR-3: New/Original Files Exempt

Files created entirely new for this project (not derived) do NOT require the "derived from" notice:
- All files in `skills/`
- All files in `patterns/`
- All files in `protocols/`
- All files in `snippets/`
- All files in `conductor/tracks/`
- templates/decisions.md
- templates/code_styleguides/java.md
- commands/patterns.md
- commands/skills.md
- commands/snippet.md
- CLAUDE.md

## Acceptance Criteria

1. All files listed in FR-2 have the appropriate license header
2. Headers are placed at the very top of each file (before any content)
3. The format matches the file type (HTML comment for .md, # comments for .py)
4. JSON files have the _license field added
5. No functional changes to any files beyond adding headers
6. Git commit includes all modified files with clear message

## Out of Scope

- Modifying the LICENSE file itself
- Adding headers to auto-generated files
- Adding headers to third-party dependencies
- Creating a NOTICE file (optional enhancement for future)
