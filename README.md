# Desmond

**"We have to push the button."**

A simple Mac utility that forces iCloud Messages to keep syncing. Inspired by Desmond Hume from *Lost*, who pushed the button every 108 minutes to save the world.

Except Desmond pushes every 15 seconds.

---

## What It Does

If you've ever tried to sync your full iMessage history to a Mac via iCloud, you know the pain. Apple's sync loves to pause, stall, and give up randomly.

Desmond fixes that by:
- Clicking the "Sync Now" button in Messages settings every 15 seconds
- Reporting your message count every 3 minutes so you can watch it climb

**This runs locally on your Mac. Nothing is uploaded anywhere.**

---

## Requirements

- macOS
- Messages in iCloud enabled (on both iPhone and Mac)
- Terminal with **Accessibility** permissions (so it can click the button)
- Terminal with **Full Disk Access** (so it can count your messages)

---

## Setup

### 1. Grant Terminal permissions

**Full Disk Access:**
- System Settings → Privacy & Security → Full Disk Access
- Click + → Add Terminal (in Applications → Utilities)

**Accessibility:**
- System Settings → Privacy & Security → Accessibility
- Click + → Add Terminal

### 2. Download and run

```bash
cd ~/Downloads
chmod +x desmond.sh
./desmond.sh
```

You'll see Desmond start pushing the button and reporting your message count.

### 3. Stop it

Press `Control + C` in Terminal when your sync is complete.

---

## Example Output

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
