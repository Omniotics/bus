# Statement of Work (SOW)

This document defines the expected cadence, deliverables, and quality gates for the Omniotics modular book project.

## Roles

- **Author** (user): Generates ideas in natural language, reviews drafts, approves changes.
- **AI assistant**: Interprets requests, manages repository files, ensures structure is coherent, and runs checks. Provides summary and next steps after each session.
- **Reviewer**: Acts as quality gate (often the author). Reviews PRs and releases, approves or requests changes.

## Cadence

- **Daily or weekly**: Add or refine one module and associated claims. Keep modules under 3 pages and at most 5 dependencies.
- **Bi‑weekly**: Update reader paths to reflect new insights.
- **Monthly**: Prune the dependency graph and tag a release (e.g. `v0.1`, `v0.2`).
- **Quarterly**: Review overall architecture via ADRs.

## Deliverables

- New or updated modules with claims and dependencies.
- Updated reader paths.
- Built manuscript(s) under `build/` (book.md and path‑specific books).
- Graphs showing dependencies.
- ADRs for major framing changes.
- Conversation log updates.

## Quality gates

- No cycles in module dependencies.
- Each dependency must exist and not exceed 5 per module.
- All claims referenced in modules must exist.
- Each claim must have at least one evidence citation and a confidence level (low/medium/high).
- Reader paths must list existing modules and be buildable.
- PR must pass `scripts/check.py` and `scripts/reader_paths.py --check`.