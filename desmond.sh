#!/bin/bash
#
# DESMOND
# "See you in another life, brother."
#
# Inspired by Desmond Hume from Lost, who pushed the button
# every 108 minutes to save the world.
#
# This Desmond pushes Sync Now every 15 seconds to save your messages.
#
# To stop it: press Control + C
#

echo ""
echo "  ██████╗ ███████╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗██████╗ "
echo "  ██╔══██╗██╔════╝██╔════╝████╗ ████║██╔═══██╗████╗  ██║██╔══██╗"
echo "  ██║  ██║█████╗  ███████╗██╔████╔██║██║   ██║██╔██╗ ██║██║  ██║"
echo "  ██║  ██║██╔══╝  ╚════██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║  ██║"
echo "  ██████╔╝███████╗███████║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██████╔╝"
echo "  ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ "
echo ""
echo "  \"We have to push the button.\""
echo "  \"4 8 15 16 23 42\""
echo ""
echo "  Pushing Sync Now every 15 seconds."
echo "  Message count check every 3 minutes."
echo ""
echo "  Press Control + C to stop (but then who will save the world?)"
echo ""

count=0

while true; do
    count=$((count + 1))
    timestamp=$(date "+%H:%M:%S")
    
    echo "[$timestamp] Push #$count - \"I'll see you in another life, brother.\""
    
    # Click the Sync Now button
    osascript <<EOF
        tell application "Messages" to activate
        delay 0.3
        tell application "System Events"
            tell process "Messages"
                keystroke "," using command down
                delay 0.5
                try
                    click button "Sync Now" of group 1 of group 1 of window "iMessage"
                    delay 0.2
                end try
            end tell
        end tell
EOF
    
    # Every 12 cycles (3 minutes), check message count
    if [ $((count % 12)) -eq 0 ]; then
        echo ""
        echo "[$timestamp] ====== THE NUMBERS ======"
        
        msg_count=$(sqlite3 ~/Library/Messages/chat.db "SELECT COUNT(*) FROM message;" 2>/dev/null)
        conv_count=$(sqlite3 ~/Library/Messages/chat.db "SELECT COUNT(DISTINCT chat_id) FROM chat_message_join;" 2>/dev/null)
        
        echo "[$timestamp] Messages on Mac: $msg_count"
        echo "[$timestamp] Conversations: $conv_count"
        echo "[$timestamp] ==========================="
        echo ""
    fi
    
    sleep 15
done
