# Desmond - Product Specification

**Repository:** `desmond`  
**Filename:** `desmond-PRODUCT_SPEC.md`  
**Last Updated:** 2026-02-16 at 15:10 UTC

---

## What This Is

**Desmond** - Project management and tracking tool

## Who It's For

**Primary Users:** Project managers, teams

## Tech Stack

Python, project tracking

---

## Core Features

The following features have been implemented based on development sessions:

1. * A description of what files you need created
2. * Or point me to files that already exist somewhere that need to be added
3. - imessage_exporter_windows.py - Exports iMessages from iPhone backups created via iTunes/Apple Devices
4. All clean. Added a .gitignore to properly ignore Python cache files, .DS_Store, and export outputs.
5. Created Android SMS exporter Python script with documentation
6. Created comprehensive README for Desmond text message export toolkit
7. Done! I've created an interactive web-based setup guide. Here's what it does:
8. Done. I've created Windows and Android support for Desmond. Here's a summary:
9. Once you've created desmond-v4, just share the repository URL with me (e.g., https://github.com/yourusername/desmond-v4) and paste your new files here. I'll take care of the rest!
10. The __pycache__ directory was created when I verified the Python syntax. I'll add a .gitignore to properly ignore it.

---

## Technical Implementation

Key technical details from implementation:

- Claude: Great idea! A web frontend with a decision tree would make it much easier for users to get started. Let me create that.
- Completed frontend HTML structure, decision tree logic, and interface styling
- Since you want to keep the web analytics frontend separate from the original desmond functionality, I can organize it in a subdirectory structure like:
- â””â”€â”€ web-analytics/                # NEW - your web frontend

---

## Architecture & Design Decisions

Key decisions made during development:

- Explored codebase and documented Desmond application architecture
- Now let me research Android SMS export and create the Android exporter. The most practical approach for Android is using the popular "SMS Backup & Restore" app which creates XML backup files.


---

## Development History

Full session-by-session development history is maintained in `SESSION_NOTES.md`.

This specification is automatically updated alongside session notes to reflect:
- New features implemented
- Technical decisions made
- Architecture changes
- Integration updates

---

## Updating This Spec

At the end of each Claude Code session, this spec is updated automatically when you say:
> "Append session notes to SESSION_NOTES.md"

Claude will:
1. Update `SESSION_NOTES.md` with detailed session history
2. Update `desmond-PRODUCT_SPEC.md` with new features/decisions
3. Commit both files together

**Never manually edit this file** - it's maintained automatically from session notes.

