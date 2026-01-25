# Desmond

**"We have to push the button."**

A Mac toolkit that forces iCloud Messages to sync, then exports your entire text message history to AI-ready formats. Named after Desmond Hume from *Lost*, who pushed the button every 108 minutes to save the world.

---

## What's Included

**desmond.sh** — Forces iCloud Messages to sync by clicking "Sync Now" every 15 seconds. Automatically stops when sync is complete.

**imessage_exporter.py** — Exports your entire message history including:
- Text messages
- Photos, videos, audio messages
- Reactions (loved, liked, laughed, etc.)
- Special content (GamePigeon, Apple Pay, stickers, Digital Touch, etc.)
- Message effects (sent with balloons, confetti, invisible ink, etc.)

**Everything runs locally on your Mac. Nothing is uploaded anywhere.**

---

## What You Get

```
~/Downloads/iMessages_Export/
├── messages.json               # Full structured data for AI analysis
├── messages.csv                # Tabular format for spreadsheets
├── SUMMARY.md                  # Stats, top conversations, content breakdown
├── INDEX.md                    # List of all conversations
├── John Smith/
│   ├── 2024-01-15.md
│   └── ...
└── ...
```

### JSON/CSV Fields

Every message includes:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO format (2024-01-15T09:32:00) |
| `date`, `time` | Separate date and time |
| `year`, `month`, `day`, `hour` | For time analysis |
| `day_of_week` | Monday, Tuesday, etc. |
| `conversation` | Contact or group name |
| `conversation_type` | "direct" or "group" |
| `sender` | Who sent the message |
| `is_from_me` | true/false |
| `message_type` | "text", "attachment", "reaction", "special" |
| `text` | Message content or description |
| `has_attachment` | true/false |
| `attachment_types` | ["photo", "video", "audio", "file"] |
| `reaction` | "loved", "liked", "laughed", etc. |
| `special_content` | "GamePigeon game", "Apple Pay", etc. |
| `effect` | "sent with balloons", "sent gently", etc. |
| `char_count`, `word_count` | For analysis |

---

## Requirements

- macOS
- Messages in iCloud enabled (iPhone and Mac)
- Terminal with **Full Disk Access**
- Terminal with **Accessibility** (for Desmond to click Sync Now)
- Terminal with **Contacts** access (for name lookup)

---

## Setup

### 1. Grant Terminal Permissions

Open **System Settings → Privacy & Security** and add Terminal to:
- **Full Disk Access**
- **Accessibility**

For **Contacts** access, the permission screen may be blank until requested. Run this in Terminal to trigger the prompt:

```bash
osascript -e 'tell application "Contacts" to get name of first person'
```

Click **OK** when the popup appears.

Restart Terminal after granting permissions.

### 2. Sync Your Messages (if needed)

If your iCloud Messages sync keeps pausing:

```bash
cd ~/Downloads
chmod +x desmond.sh
./desmond.sh
```

Desmond will click Sync Now every 15 seconds and show your progress:

```
[15:44:08] ====== STARTING ======
[15:44:08] Messages on Mac: 142,847
[15:44:08] Conversations: 89
[15:44:08] ========================

[15:44:23] Push #2 - +312 new messages (total: 143,159)
[15:44:38] Push #3 - +287 new messages (total: 143,446)
...

[15:52:53] ====== SYNC APPEARS COMPLETE ======
[15:52:53] Final count: 346,476 messages
[15:52:53] "See you in another life, brother."
```

**Optional:** Set a target if you know your message count:

```bash
./desmond.sh 346000
```

### 3. Export Your Messages

```bash
python3 imessage_exporter.py --full
```

Output:

```
Running full export of all messages...
Loading contacts...
Loaded 1,084 contact mappings.
Exported 346,476 messages from 3,178 conversations.

Creating AI-ready exports...

Message breakdown:
  • Text messages:      304,500
  • Attachments only:   1,908
  • Text + attachment:  X
  • Reactions:          2,432
  • Special/app:        37,636
  • Total:              346,476

Created messages.json
Created messages.csv
Created SUMMARY.md
```

### 4. Automatic Exports (optional)

To run exports hourly in the background:

```bash
chmod +x setup_imessage_exporter.sh
./setup_imessage_exporter.sh
```

---

## Using with Claude

**For analysis and insights:**
- Upload `messages.json` — Claude can analyze patterns, relationships, timing, sentiment
- Upload `SUMMARY.md` — Quick overview when you just need context

**Example prompts:**
- "Who do I text the most?"
- "What time of day am I most active?"
- "Show me my messaging patterns by day of week"
- "Find all messages where I discussed [topic]"
- "How often do I play GamePigeon with [person]?"
- "What's the sentiment trend in my conversations with [person]?"

---

## Message Types Explained

| Type | What it captures |
|------|------------------|
| `text` | Regular text messages |
| `attachment` | Photos, videos, audio messages, files (no text) |
| `text_with_attachment` | Text message that also has media |
| `reaction` | Tapback reactions (❤️ loved, 👍 liked, 😂 laughed, etc.) |
| `special` | GamePigeon, Apple Pay, Digital Touch, stickers, handwriting, etc. |

---

## Why Does iCloud Sync Keep Pausing?

Apple prioritizes battery over sync speed. Large syncs stall unless:
- Device is plugged in
- Device is awake
- You're actively babysitting it

Desmond does the babysitting for you.

---

## License

MIT — do whatever you want with it.

---

## Support

If Desmond saved your sanity (and your messages):

☕ [Patreon](https://www.patreon.com/c/christreadaway)

---

*"See you in another life, brother."*
