# Plan: Fix tracks.md Format Inconsistency

**Spec:** [spec.md](./spec.md)
**Issue:** https://github.com/rbarcante/claude-conductor/issues/46

---

## Phase 1: Diagnose & Write Failing Tests [checkpoint: ]

- [ ] Task: Read `scripts/lib/tracks_parser.py` and `scripts/commands/newtrack.py` in full to confirm exact format written vs. parsed
- [ ] Task: Write failing test — `TracksParser` parses table-format `tracks.md` correctly (maps ID, description, status to `Track` objects)
- [ ] Task: Write failing test — `TracksParser` correctly handles a `tracks.md` with both checkbox and table entries (mixed format)
- [ ] Task: Write failing test — `newtrack register` writes checkbox-format entry (confirm or catch regression)
- [ ] Task: Run tests and confirm RED phase — all new tests fail as expected
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

---

## Phase 2: Fix the Reader — `TracksParser` [checkpoint: ]

- [ ] Task: Update `TracksParser.parse_tracks_registry()` to detect and parse Markdown table format rows
- [ ] Task: Map table column values (`ID`, `Title`, `Status`, `Created`) to `Track` object fields
- [ ] Task: Map status strings (`in-progress`, `pending`, `completed`) to internal status enum/constants
- [ ] Task: Run tests — confirm reader tests go GREEN, no regression on checkbox-format tests
- [ ] Task: Verify coverage ≥ 80% for `tracks_parser.py`
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

---

## Phase 3: Fix the Writer — `newtrack register` & `setup` [checkpoint: ]

- [ ] Task: Confirm `_create_track_entry` in `newtrack.py` produces canonical checkbox format; fix if it emits table format
- [ ] Task: Confirm `setup scaffold` writes the correct checkbox-compatible `tracks.md` template; fix if needed
- [ ] Task: Run full test suite — all tests GREEN
- [ ] Task: Run `conductor --json status` end-to-end smoke test (setup → newtrack → status shows non-empty tracks)
- [ ] Task: Verify coverage ≥ 80% for `newtrack.py` and `setup.py` writer paths
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
