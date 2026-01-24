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

---

## Setup

### 1. Grant Terminal permissions

**Full Disk Access:**
- System Settings → Privacy & Security → Full Disk Access
- Click + → Add Terminal (in Applications → Utilities)

**Accessibility:**
- System Settings → Privacy & Security → Accessibility
- Click + → Add Terminal

Restart Terminal after granting permissions.

### 2. Force your messages to sync

If your iCloud Messages sync keeps pausing or stalling:

```bash
cd ~/Downloads
chmod +x desmond.sh
./desmond.sh
```

Leave it running until your message count stops climbing. Press `Control + C` to stop.

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

[15:44:08] Push #1 - "I'll see you in another life, brother."
[15:44:23] Push #2 - "I'll see you in another life, brother."
...
[15:47:08] ====== THE NUMBERS ======
[15:47:08] Messages on Mac: 142847
[15:47:08] Conversations: 89
[15:47:08] ===========================
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
