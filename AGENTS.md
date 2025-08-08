# Agent Behaviour Contract

This file provides a contract for the AI assistant interacting with this repository.

## Responsibilities

- **Interpret natural language:** The assistant reads the user's statements and determines whether to create or update modules, claims, reader paths, or ADRs.
- **Plan before acting:** Suggest up to three possible actions and wait for the user to approve one before making changes. Plans should be described in everyday language without requiring the user to reference file names or scripts.
- **Operate on the repository:** When approved, edit or create files under the appropriate directories. Use templates in `templates/` as a starting point when creating new modules or claims.
- **Run validation:** After making changes, run `scripts/check.py` and `scripts/reader_paths.py --check`. If validation fails, halt and ask for guidance.
- **Communicate clearly:** Summarize what has been done and what problems were found. Update `notes/conversation_log.md` with a short recap of the conversation and actions taken.
- **Open pull requests:** Do not push directly to `main`. Create a branch, commit changes, and open a pull request using the template in `templates/PR_TEMPLATE.md`. Tag the appropriate reviewers.

## Natural Language Triggers

The assistant should interpret phrases such as:

- "I want to expand the section on X" → likely update a module.
- "This claim feels weak" → open an RFC to strengthen a claim; suggest sources.
- "We need a new perspective on Y" → create a new module with dependencies on related modules.
- "How do these ideas connect?" → run the graph script and provide insights or suggest refactors.

The assistant should avoid asking the user to reference file names or scripts unless absolutely necessary.