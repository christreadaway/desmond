# Desmond — Business Product Spec
**Version:** 1.5 | **Date:** 2026-02-16 | **Repo:** github.com/christreadaway/desmond

---

## 1. Problem Statement
Apple's iMessage database is locked in a SQLite file on macOS with no built-in export or analytics capability. Users can't search their full message history efficiently, can't analyze communication patterns, and can't pipe their messaging data into other tools. For someone building a personal CRM or interaction analytics system, the raw iMessage data is the foundation — but extracting it requires navigating macOS security permissions, understanding the chat.db schema, and handling contact resolution from Apple's Address Book.

## 2. Solution
A macOS toolkit for exporting, syncing, and analyzing iMessage history. Desmond reads the local iMessage database (~/Library/Messages/chat.db), resolves phone numbers to contact names via the macOS Address Book, and exports structured conversation data. It serves as the data ingestion layer for PersonalCRM and other downstream analytics projects.

## 3. Target Users
- **Personal Analytics Enthusiasts** — People who want to analyze their communication patterns
- **Developers Building on iMessage Data** — Using Desmond as a data pipeline component
- **Digital Archivists** — People who want searchable backups of their message history
- **PersonalCRM Users** — Desmond provides the raw data that PersonalCRM visualizes

## 4. Core Features

### iMessage Export
- **Full Export** — `python3 imessage_exporter.py --full` extracts all messages from chat.db
- **Contact Resolution** — Maps phone numbers and email addresses to real names via macOS Address Book
- **Group Chat Support** — Exports group conversations with all participant names
- **Attachment Metadata** — Tracks attachment types and file references

### iCloud Sync
- **desmond.sh** — Shell script that uses AppleScript to click the iCloud Sync button in Messages.app
- **Ensures Fresh Data** — Syncs latest messages before export

### Output Format
- Structured export to ~/Downloads/iMessages_Export/
- Per-conversation files with timestamps, sender, and message content
- Contact lookup table for number-to-name resolution

### macOS Permissions Required
- **Full Disk Access** — Read ~/Library/Messages/chat.db
- **Accessibility** — AppleScript UI automation for sync button
- **Contacts** — Read Address Book for name resolution

## 5. Tech Stack
- **Language:** Python 3
- **Database:** SQLite (reading Apple's chat.db)
- **Automation:** AppleScript via shell scripts
- **Platform:** macOS only (requires Apple's Messages.app and Address Book)

## 6. Data & Privacy
- **100% Local** — All data stays on the user's Mac
- **Read-Only** — Never modifies the iMessage database
- **No Cloud** — No data transmitted externally
- **Export files are local** — Stored in ~/Downloads/

## 7. Current Status
- **Working:** iMessage export with contact resolution (macOS)
- **Working:** Shell scripts made executable
- **Working:** Python syntax verified
- **Repository:** Public on GitHub
- **Known Limitation:** macOS-only; requires manual permission grants in System Preferences
- **Desmond-lite v3** — Planned lighter version for simpler use cases, not yet built

## 8. Business Model
- **Open Source** — Free infrastructure tool
- **Enables Other Products** — Data pipeline for PersonalCRM (analytics) and ParentPoint (text message mining)

## 9. Success Metrics
- Successful message exports across different macOS versions
- Contact resolution accuracy
- Downstream data quality in PersonalCRM
- Community adoption (GitHub stars, forks)

## 10. Open Questions / Next Steps
- Desmond-lite v3 (simpler, focused export tool)
- Incremental export (only new messages since last run)
- Windows/Linux support via iCloud web scraping
- Direct integration with PersonalCRM data ingestion
- Attachment export (photos, videos, documents)
- Group chat analytics preprocessing
- Integration with ParentPoint for parent text mining
