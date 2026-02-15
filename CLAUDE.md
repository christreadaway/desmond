# Claude Code Instructions - Desmond

## About This Project
[Project description - based on transcripts, appears to be a Python project but specific purpose needs clarification]

## About Me (Chris Treadaway)
Product builder, not a coder. I bring requirements and vision — you handle implementation.

**Working with me:**
- Bias toward action - just do it, don't argue
- Make terminal commands dummy-proof (always start with `cd ~/desmond`)
- Minimize questions - make judgment calls and tell me what you chose
- I get interrupted frequently - always end sessions with a handoff note

## Tech Stack
- **Language:** Python
- **Framework:** [To be determined based on codebase]

## File Paths
- **Always use:** `~/desmond/path/to/file`
- **Never use:** `/Users/christreadaway/...`
- **Always start commands with:** `cd ~/desmond`

## PII Rules (CRITICAL)
❌ NEVER include:
- Real names → use [Name]
- Email addresses → use user@example.com
- File paths with /Users/christreadaway → use ~/
- API keys/tokens

✅ ALWAYS use placeholders

## Session End Routine
```markdown
## Session Handoff - [Date]

### What We Built
- [Feature 1]: [files modified]

### Current Status
✅ Working: [tested features]
❌ Broken: [known issues]
🚧 In Progress: [incomplete]

### Files Changed
- [file].py

### Current Branch
Branch: [branch-name]
Ready to merge: [Yes/No]

### Next Steps
1. [Priority 1]
2. [Priority 2]
```

## Git Branch Strategy
- Claude Code creates new branch per session
- Merge to main when stable
- Delete merged branches immediately

## Testing Approach
- [To be filled in based on project specifics]

## Current Status
Active project - last worked on Jan 25-Feb 3, 2026.

---
Last Updated: February 16, 2026
