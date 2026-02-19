#!/bin/bash
# Desmond - Android SMS Exporter for macOS
# Exports your SMS/MMS from Android backup files to AI-ready formats

echo ""
echo "============================================================"
echo "  Desmond - Android SMS Exporter"
echo '  "We have to push the button."'
echo "============================================================"
echo ""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo ""
    echo "On macOS, Python 3 should be pre-installed."
    echo "If not, install it via Homebrew: brew install python3"
    exit 1
fi

# Run the exporter
python3 "$SCRIPT_DIR/android_sms_exporter.py" "$@"
