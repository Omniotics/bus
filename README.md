# Omniotics Book Repo

This repository implements the **modular book** architecture for the Omniotics project.

## Purpose

The goal is to maintain a living manuscript built from small, composable ideas (**modules**). Each module captures a single concept with a summary, dependencies, claims and evidence. A **claim** is a falsifiable statement with a confidence level and supporting evidence.

## How to use this repo (for humans)

Speak in natural language about your ideas. The AI assistant will interpret your intent and translate it into actions in this repository. You do not need to remember file names or run scripts. Describe what you want to do (e.g. "expand the section on empathy and its relationship to LGBT safety") and the assistant will figure out which module needs to be edited or created.

## How the AI assistant should behave

1. **Interpret intent:** When reading a user request, identify what they want: add or update a module, create or update claims, reorganize chapters, adjust reader paths, record a design decision, etc.
2. **Plan and confirm:** Propose up to three steps in plain English. Wait for the user to approve one of them before making changes.
3. **Make changes in this repo:** Edit or create files under `modules/`, `claims/`, `chapters/`, `notes/`, etc. Follow the templates in `templates/`.
4. **Run checks:** Run `scripts/check.py` and `scripts/reader_paths.py --check` to ensure dependencies and reader paths are valid. If issues are found, report them and wait for direction.
5. **Open a Pull Request:** Never push directly to `main`. Open a PR with a clear description of what changed, attach the built book and graphs as artifacts, and request review.
6. **Update conversation log:** Append a summary of what happened in this session to `notes/conversation_log.md`.

## Files and directories

- `modules/`: atomic idea files with YAML front matter.
- `claims/`: falsifiable statements with evidence and confidence ratings.
- `chapters/`: files that assemble modules into manuscripts, plus `reader_paths.yml` listing curated reading orders.
- `templates/`: templates for modules, claims, and pull requests.
- `scripts/`: maintenance scripts (check dependencies, build books, generate graphs, build reader‑path specific books).
- `adrs/`: Architecture/Design Records for major framing decisions.
- `notes/`: conversation logs and scratch notes.
- `sources/`: bibliographies or reference materials.

See `SOW.md` for roles and responsibilities, and `STYLE.md` for tone and voice guidelines.