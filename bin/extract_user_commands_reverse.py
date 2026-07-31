#!/usr/bin/env python3
"""
Transcript User Command Extractor Engine
Parses transcript.jsonl and extracts past user requests starting from the 2nd user input
in reverse chronological order.
"""

import os
import sys
import json

LOG_PATH = r"C:\Users\Monica Fugazi\.gemini\antigravity-cli\brain\5bdfa022-0fd2-4afc-9168-629c81a5ab4f\.system_generated\logs\transcript.jsonl"

def main():
    print("==========================================================================")
    print("      USER COMMAND HISTORY EXTRACTOR (REVERSE CHRONOLOGICAL ORDER)        ")
    print("==========================================================================")

    if not os.path.exists(LOG_PATH):
        print("Transcript log not found.")
        return

    user_requests = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT" and data.get("source") == "USER_EXPLICIT":
                    content = data.get("content", "")
                    if "<USER_REQUEST>" in content:
                        req = content.split("<USER_REQUEST>")[1].split("</USER_REQUEST>")[0].strip()
                        user_requests.append(req)
            except Exception:
                pass

    print(f"Total Explicit User Requests Recorded: {len(user_requests)}\n")
    print("Listing user commands starting from 2nd request in REVERSE order:\n")

    # Reverse order, starting from 2nd (index -2 down to 0)
    for idx, req in enumerate(reversed(user_requests[:-1]), 1):
        print(f"  [{idx}] {req}")

    print("\n==========================================================================")

if __name__ == "__main__":
    main()
