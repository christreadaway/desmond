#!/usr/bin/env python3
"""
iMessage Exporter for Claude
Automatically exports your iMessages to readable markdown files.
"""

import sqlite3
import os
import json
import re
import glob
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
MESSAGES_DB = os.path.expanduser("~/Library/Messages/chat.db")
OUTPUT_DIR = os.path.expanduser("~/Downloads/iMessages_Export")
STATE_FILE = os.path.expanduser("~/Downloads/iMessages_Export/.export_state.json")

# Global contact lookup cache
CONTACTS_CACHE = {}

def load_contacts():
    """Load contacts from the Mac AddressBook database."""
    global CONTACTS_CACHE
    
    print("Loading contacts...")
    
    # Find all possible AddressBook database locations
    ab_sources = os.path.expanduser("~/Library/Application Support/AddressBook/Sources/")
    ab_root = os.path.expanduser("~/Library/Application Support/AddressBook/")
    
    db_files = []
    
    # Check Sources subdirectories
    if os.path.exists(ab_sources):
        db_files.extend(glob.glob(os.path.join(ab_sources, "*", "AddressBook-v22.abcddb")))
    
    # Check root AddressBook folder
    if os.path.exists(ab_root):
        root_db = os.path.join(ab_root, "AddressBook-v22.abcddb")
        if os.path.exists(root_db):
            db_files.append(root_db)
    
    if not db_files:
        print("Note: Could not find Contacts database. Using phone numbers/emails instead.")
        return
    
    for db_file in db_files:
        try:
            # Copy database to temp location to avoid lock issues
            temp_db = "/tmp/contacts_temp.db"
            subprocess.run(['cp', db_file, temp_db], check=True)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Get phone numbers with contact names
            try:
                cursor.execute("""
                    SELECT 
                        ZABCDRECORD.ZFIRSTNAME,
                        ZABCDRECORD.ZLASTNAME,
                        ZABCDPHONENUMBER.ZFULLNUMBER
                    FROM ZABCDRECORD
                    LEFT JOIN ZABCDPHONENUMBER ON ZABCDRECORD.Z_PK = ZABCDPHONENUMBER.ZOWNER
                    WHERE ZABCDPHONENUMBER.ZFULLNUMBER IS NOT NULL
                """)
                
                for row in cursor.fetchall():
                    first_name, last_name, phone = row
                    name_parts = [p for p in [first_name, last_name] if p]
                    if name_parts and phone:
                        name = " ".join(name_parts)
                        # Normalize phone number (remove all non-digits)
                        normalized_phone = re.sub(r'\D', '', phone)
                        # Store with last 10 digits as key (handles country code variations)
                        if len(normalized_phone) >= 10:
                            CONTACTS_CACHE[normalized_phone[-10:]] = name
                        if normalized_phone:
                            CONTACTS_CACHE[normalized_phone] = name
            except Exception as e:
                print(f"  Phone lookup error: {e}")
            
            # Get email addresses with contact names
            try:
                cursor.execute("""
                    SELECT 
                        ZABCDRECORD.ZFIRSTNAME,
                        ZABCDRECORD.ZLASTNAME,
                        ZABCDEMAILADDRESS.ZADDRESS
                    FROM ZABCDRECORD
                    LEFT JOIN ZABCDEMAILADDRESS ON ZABCDRECORD.Z_PK = ZABCDEMAILADDRESS.ZOWNER
                    WHERE ZABCDEMAILADDRESS.ZADDRESS IS NOT NULL
                """)
                
                for row in cursor.fetchall():
                    first_name, last_name, email = row
                    name_parts = [p for p in [first_name, last_name] if p]
                    if name_parts and email:
                        CONTACTS_CACHE[email.lower()] = " ".join(name_parts)
            except Exception as e:
                print(f"  Email lookup error: {e}")
            
            conn.close()
            
            # Clean up temp file
            os.remove(temp_db)
            
        except Exception as e:
            print(f"  Error reading {db_file}: {e}")
    
    print(f"Loaded {len(CONTACTS_CACHE)} contact mappings.")

def lookup_contact_name(identifier):
    """Look up a contact name from phone number or email."""
    if not identifier:
        return "Unknown"
    
    # Try direct match (for emails)
    if identifier.lower() in CONTACTS_CACHE:
        return CONTACTS_CACHE[identifier.lower()]
    
    # Try phone number lookup
    normalized = re.sub(r'\D', '', identifier)
    if normalized in CONTACTS_CACHE:
        return CONTACTS_CACHE[normalized]
    
    # Try last 10 digits
    if len(normalized) >= 10 and normalized[-10:] in CONTACTS_CACHE:
        return CONTACTS_CACHE[normalized[-10:]]
    
    # Return original identifier if no match
    return identifier

def get_contact_name(handle_id, cursor):
    """Get the phone number or email for a handle, then look up contact name."""
    cursor.execute("SELECT id FROM handle WHERE ROWID = ?", (handle_id,))
    result = cursor.fetchone()
    if result:
        return lookup_contact_name(result[0])
    return "Unknown"

def get_chat_participants(chat_id, cursor):
    """Get participant names for a group chat."""
    # First get the chat ROWID from the chat_identifier
    cursor.execute("SELECT ROWID FROM chat WHERE chat_identifier = ?", (chat_id,))
    chat_row = cursor.fetchone()
    if not chat_row:
        return None
    
    chat_rowid = chat_row[0]
    
    # Get all handles (participants) for this chat
    cursor.execute("""
        SELECT handle.id 
        FROM handle 
        JOIN chat_handle_join ON handle.ROWID = chat_handle_join.handle_id
        WHERE chat_handle_join.chat_id = ?
    """, (chat_rowid,))
    
    participants = []
    for row in cursor.fetchall():
        handle_id = row[0]
        name = lookup_contact_name(handle_id)
        # Only add if we got a real name (not the phone number back)
        if name and name != handle_id:
            participants.append(name)
        elif name:
            # Got phone number back, abbreviate it
            participants.append(name[-4:] if len(name) > 4 else name)
    
    if participants:
        # Limit to first 3 names to keep folder names reasonable
        if len(participants) > 3:
            return ", ".join(participants[:3]) + f" +{len(participants)-3}"
        return ", ".join(participants)
    
    return None

def convert_apple_time(apple_timestamp):
    """Convert Apple's timestamp format to readable datetime."""
    if apple_timestamp is None:
        return None
    # Apple uses nanoseconds since 2001-01-01
    unix_timestamp = apple_timestamp / 1_000_000_000 + 978307200
    return datetime.fromtimestamp(unix_timestamp)

def load_state():
    """Load the last export state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_message_rowid": 0}

def save_state(state):
    """Save the export state."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def export_messages(full_export=False):
    """Export messages to markdown files."""
    
    # Load contacts for name lookup
    load_contacts()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load state
    state = load_state()
    last_rowid = 0 if full_export else state.get("last_message_rowid", 0)
    
    # Connect to database
    conn = sqlite3.connect(MESSAGES_DB)
    cursor = conn.cursor()
    
    # Get messages
    query = """
    SELECT 
        message.ROWID,
        message.text,
        message.date,
        message.is_from_me,
        message.handle_id,
        chat.chat_identifier,
        chat.display_name
    FROM message
    LEFT JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    LEFT JOIN chat ON chat_message_join.chat_id = chat.ROWID
    WHERE message.ROWID > ?
    ORDER BY message.date ASC
    """
    
    cursor.execute(query, (last_rowid,))
    messages = cursor.fetchall()
    
    if not messages:
        print("No new messages to export.")
        return
    
    # Organize messages by conversation and date
    conversations = defaultdict(lambda: defaultdict(list))
    max_rowid = last_rowid
    
    for row in messages:
        rowid, text, date, is_from_me, handle_id, chat_id, display_name = row
        
        if text is None:
            continue
            
        max_rowid = max(max_rowid, rowid)
        
        # Get conversation identifier
        if display_name:
            conv_name = display_name
        elif chat_id:
            # First try to look up as a contact (for 1:1 chats)
            conv_name = lookup_contact_name(chat_id)
            # If we got back the same thing (no match), try getting group participants
            if conv_name == chat_id or conv_name.startswith("chat"):
                participants = get_chat_participants(chat_id, cursor)
                if participants:
                    conv_name = participants
                else:
                    conv_name = chat_id
        else:
            conv_name = get_contact_name(handle_id, cursor) if handle_id else "Unknown"
        
        # Clean up conversation name for filename
        conv_name_clean = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in str(conv_name))
        
        # Get date
        msg_datetime = convert_apple_time(date)
        if msg_datetime is None:
            continue
            
        date_str = msg_datetime.strftime("%Y-%m-%d")
        time_str = msg_datetime.strftime("%H:%M")
        
        # Determine sender - for group chats, get the actual sender's name
        if is_from_me:
            sender = "Me"
        else:
            sender = get_contact_name(handle_id, cursor) if handle_id else conv_name
        
        conversations[conv_name_clean][date_str].append({
            "time": time_str,
            "sender": sender,
            "text": text
        })
    
    # Write to files
    messages_written = 0
    
    for conv_name, dates in conversations.items():
        conv_dir = os.path.join(OUTPUT_DIR, conv_name)
        os.makedirs(conv_dir, exist_ok=True)
        
        for date_str, msgs in dates.items():
            filename = os.path.join(conv_dir, f"{date_str}.md")
            
            # Append to existing file or create new
            mode = 'a' if os.path.exists(filename) else 'w'
            
            with open(filename, mode) as f:
                if mode == 'w':
                    f.write(f"# Messages with {conv_name} - {date_str}\n\n")
                
                for msg in msgs:
                    f.write(f"**{msg['time']} - {msg['sender']}:** {msg['text']}\n\n")
                    messages_written += 1
    
    # Create a master index file
    create_index(OUTPUT_DIR)
    
    # Save state
    state["last_message_rowid"] = max_rowid
    state["last_export"] = datetime.now().isoformat()
    save_state(state)
    
    print(f"Exported {messages_written} messages from {len(conversations)} conversations.")
    conn.close()

def export_ai_ready(full_export=False):
    """Export messages to AI-ready JSON and CSV formats."""
    
    # Load contacts for name lookup
    load_contacts()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load state
    state = load_state()
    last_rowid = 0 if full_export else state.get("last_message_rowid", 0)
    
    # Connect to database
    conn = sqlite3.connect(MESSAGES_DB)
    cursor = conn.cursor()
    
    # Get messages with more metadata
    query = """
    SELECT 
        message.ROWID,
        message.text,
        message.date,
        message.is_from_me,
        message.handle_id,
        chat.chat_identifier,
        chat.display_name,
        chat.ROWID as chat_rowid
    FROM message
    LEFT JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    LEFT JOIN chat ON chat_message_join.chat_id = chat.ROWID
    WHERE message.ROWID > ?
    ORDER BY message.date ASC
    """
    
    cursor.execute(query, (last_rowid,))
    messages = cursor.fetchall()
    
    if not messages:
        print("No new messages to export.")
        return
    
    # Build structured data
    all_messages = []
    conversations_meta = {}
    
    for row in messages:
        rowid, text, date, is_from_me, handle_id, chat_id, display_name, chat_rowid = row
        
        if text is None:
            continue
        
        # Get timestamp
        msg_datetime = convert_apple_time(date)
        if msg_datetime is None:
            continue
        
        # Get conversation name
        if display_name:
            conv_name = display_name
            conv_type = "group"
        elif chat_id:
            conv_name = lookup_contact_name(chat_id)
            if conv_name == chat_id or conv_name.startswith("chat"):
                participants = get_chat_participants(chat_id, cursor)
                if participants:
                    conv_name = participants
                    conv_type = "group"
                else:
                    conv_name = chat_id
                    conv_type = "unknown"
            else:
                conv_type = "direct"
        else:
            conv_name = get_contact_name(handle_id, cursor) if handle_id else "Unknown"
            conv_type = "direct"
        
        # Get sender name
        if is_from_me:
            sender = "Me"
        else:
            sender = get_contact_name(handle_id, cursor) if handle_id else conv_name
        
        # Build message record
        msg_record = {
            "timestamp": msg_datetime.isoformat(),
            "date": msg_datetime.strftime("%Y-%m-%d"),
            "time": msg_datetime.strftime("%H:%M:%S"),
            "year": msg_datetime.year,
            "month": msg_datetime.month,
            "day": msg_datetime.day,
            "hour": msg_datetime.hour,
            "day_of_week": msg_datetime.strftime("%A"),
            "conversation": conv_name,
            "conversation_type": conv_type,
            "sender": sender,
            "is_from_me": bool(is_from_me),
            "text": text,
            "char_count": len(text),
            "word_count": len(text.split())
        }
        
        all_messages.append(msg_record)
        
        # Track conversation metadata
        if conv_name not in conversations_meta:
            conversations_meta[conv_name] = {
                "name": conv_name,
                "type": conv_type,
                "message_count": 0,
                "first_message": msg_datetime.isoformat(),
                "last_message": msg_datetime.isoformat()
            }
        conversations_meta[conv_name]["message_count"] += 1
        conversations_meta[conv_name]["last_message"] = msg_datetime.isoformat()
    
    conn.close()
    
    # Write JSON
    json_path = os.path.join(OUTPUT_DIR, "messages.json")
    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_messages": len(all_messages),
        "total_conversations": len(conversations_meta),
        "conversations": list(conversations_meta.values()),
        "messages": all_messages
    }
    
    with open(json_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"Created {json_path} ({len(all_messages)} messages)")
    
    # Write CSV
    csv_path = os.path.join(OUTPUT_DIR, "messages.csv")
    
    if all_messages:
        fieldnames = ["timestamp", "date", "time", "year", "month", "day", "hour", 
                      "day_of_week", "conversation", "conversation_type", "sender", 
                      "is_from_me", "text", "char_count", "word_count"]
        
        import csv
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_messages)
        
        print(f"Created {csv_path}")
    
    # Write a summary file for quick context
    summary_path = os.path.join(OUTPUT_DIR, "SUMMARY.md")
    with open(summary_path, 'w') as f:
        f.write("# iMessage Export Summary\n\n")
        f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Total Messages:** {len(all_messages):,}\n")
        f.write(f"**Total Conversations:** {len(conversations_meta)}\n\n")
        
        # Date range
        if all_messages:
            first_date = all_messages[0]["date"]
            last_date = all_messages[-1]["date"]
            f.write(f"**Date Range:** {first_date} to {last_date}\n\n")
        
        # Top conversations
        f.write("## Top 20 Conversations (by message count)\n\n")
        sorted_convos = sorted(conversations_meta.values(), key=lambda x: x["message_count"], reverse=True)[:20]
        for conv in sorted_convos:
            f.write(f"- **{conv['name']}**: {conv['message_count']:,} messages ({conv['type']})\n")
        
        f.write("\n## Files\n\n")
        f.write("- `messages.json` — Full structured data for AI analysis\n")
        f.write("- `messages.csv` — Tabular format for spreadsheets or analysis\n")
        f.write("- `SUMMARY.md` — This file\n")
        f.write("- Individual folders — Markdown files organized by contact and date\n")
    
    print(f"Created {summary_path}")

def create_index(output_dir):
    """Create an index file listing all conversations and recent activity."""
    index_path = os.path.join(output_dir, "INDEX.md")
    
    with open(index_path, 'w') as f:
        f.write("# iMessage Export Index\n\n")
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Conversations\n\n")
        
        for item in sorted(os.listdir(output_dir)):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # Count messages and get date range
                md_files = [f for f in os.listdir(item_path) if f.endswith('.md')]
                if md_files:
                    dates = sorted([f.replace('.md', '') for f in md_files])
                    f.write(f"- **{item}**: {len(md_files)} days of messages ({dates[0]} to {dates[-1]})\n")

def main():
    import sys
    
    full_export = "--full" in sys.argv
    
    if full_export:
        print("Running full export of all messages...")
    else:
        print("Exporting new messages since last run...")
    
    try:
        # Export markdown files (for human browsing)
        export_messages(full_export=full_export)
        
        # Export AI-ready JSON and CSV
        print("\nCreating AI-ready exports...")
        export_ai_ready(full_export=full_export)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure Terminal has Full Disk Access:")
        print("System Settings > Privacy & Security > Full Disk Access > Enable Terminal")

if __name__ == "__main__":
    main()
