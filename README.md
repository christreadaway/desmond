# Desmond

**"We have to push the button."**

A Mac toolkit that forces iCloud Messages to sync, then exports your texts to files you can use with Claude AI. Inspired by Desmond Hume from *Lost*, who pushed the button every 108 minutes to save the world.

Except this Desmond pushes every 15 seconds.

---

## What's Included

**desmond.sh** — Forces iCloud Messages to keep syncing by clicking "Sync Now" every 15 seconds. Reports your message count every 3 minutes.

**imessage_exporter.py** — Exports your messages to clean markdown files, organized by contact and date. Runs automatically every hour once set up.

**This runs locally on your Mac. Nothing is uploaded anywhere.**

---

## Requirements

- macOS
- Messages in iCloud enabled (on both iPhone and Mac)
- Terminal with **Full Disk Access** (to read your messages)
- Terminal with **Accessibility** permissions (to click the Sync Now button)
- Terminal with **Contacts** access (to show names instead of phone numbers)

---

## Setup

### 1. Grant Terminal permissions

Open **System Settings → Privacy & Security** and add Terminal to:

- **Full Disk Access** (to read messages)
- **Accessibility** (to click Sync Now)

**For Contacts access**, the permission screen may be blank until an app requests it. Run this in Terminal to trigger the prompt:

```bash
osascript -e 'tell application "Contacts" to get name of first person'
```

Click **OK** when the popup appears. Then Terminal will show up in Privacy & Security → Contacts.

Restart Terminal after granting permissions.

### 2. Force your messages to sync

If your iCloud Messages sync keeps pausing or stalling:

```bash
cd ~/Downloads
chmod +x desmond.sh
./desmond.sh
```

Desmond will:
- Click Sync Now every 15 seconds
- Show you how many new messages arrived
- Automatically stop when no new messages arrive for ~1 minute

**Optional:** If you know how many messages you have (check iPhone → Settings → [Your Name] → iCloud → Messages), you can set a target:

```bash
./desmond.sh 344254
```

Desmond will stop when it reaches that number.

### 3. Export your messages

Once your messages are synced, run the exporter:

```bash
python3 imessage_exporter.py --full
```

Your messages will be saved to:

```
~/Downloads/iMessages_Export/
├── INDEX.md                    # Overview of all conversations
├── John Smith/
│   ├── 2024-01-15.md
│   ├── 2024-01-16.md
│   └── ...
├── Mom/
│   ├── 2023-12-25.md
│   └── ...
└── ...
```

Each markdown file contains your conversation for that day, formatted like:

```
# Messages with John Smith - 2024-01-15

**09:32 - John Smith:** Hey, are we still on for lunch?

**09:35 - Me:** Yeah, noon works. Same place?
```

### 4. Set up automatic exports (optional)

To export new messages every hour automatically:

```bash
chmod +x setup_imessage_exporter.sh
./setup_imessage_exporter.sh
```

This installs a background job that runs hourly.

---

## Using with Claude

Once exported, you can:

- Upload specific conversation files to Claude for context
- Upload `INDEX.md` to show Claude what conversations exist
- Search the export folder locally, then share relevant files

---

## Example Output (desmond.sh)

```
  ██████╗ ███████╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗██████╗ 
  ██╔══██╗██╔════╝██╔════╝████╗ ████║██╔═══██╗████╗  ██║██╔══██╗
  ██║  ██║█████╗  ███████╗██╔████╔██║██║   ██║██╔██╗ ██║██║  ██║
  ██║  ██║██╔══╝  ╚════██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║  ██║
  ██████╔╝███████╗███████║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██████╔╝
  ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 

  "We have to push the button."
  "4 8 15 16 23 42"

[15:44:08] ====== STARTING ======
[15:44:08] Messages on Mac: 142847
[15:44:08] Conversations: 89
[15:44:08] ========================

[15:44:23] Push #2 - +312 new messages (total: 143159)
[15:44:38] Push #3 - +287 new messages (total: 143446)
...
[15:52:08] Push #31 - No new messages (check 1/4)
[15:52:23] Push #32 - No new messages (check 2/4)
[15:52:38] Push #33 - No new messages (check 3/4)
[15:52:53] Push #34 - No new messages (check 4/4)

[15:52:53] ====== SYNC APPEARS COMPLETE ======
[15:52:53] No new messages for 4 checks.
[15:52:53] Final count: 344254 messages in 127 conversations

[15:52:53] "See you in another life, brother."
```

---

## Why Does iCloud Sync Keep Pausing?

Apple prioritizes battery life over sync speed. Large message syncs often stall unless:
- Device is plugged in
- Device is awake
- You're actively babysitting it

Desmond does the babysitting for you.

---

## License

MIT — do whatever you want with it.

---

## Support

If Desmond saved your sanity (and your messages), consider buying me a coffee:

☕ [Patreon](https://www.patreon.com/c/christreadaway)

---

*"See you in another life, brother."*
