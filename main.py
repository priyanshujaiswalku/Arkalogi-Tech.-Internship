"""
Arkalogi Internship Portfolio - Priyanshu Kumar
Main Unified Application Entry Point

To launch the complete integrated web portal:
    python main.py
"""

import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import the integrated application
from web_portal.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print(" 💼 ARKALOGI BACKEND INTERNSHIP PORTFOLIO - PRIYANSHU KUMAR")
    print("=" * 70)
    print(f"[*] Starting Unified Web Portal on http://127.0.0.1:{port}")
    print(f"[*] Access all Tasks (Task 01 to Task 09) via the web interface.")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=True)