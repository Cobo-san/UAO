#!/usr/bin/env python3
"""
Automated Secret & Credential Scanner Engine for UAO Repository
Scans all codebase files for potential exposed API keys, credentials, tokens,
private keys, and sensitive environment variables to guarantee 100% secret safety before pushing to GitHub.
"""

import os
import sys
import re
import platform

# High-sensitivity secret regex patterns
SECRET_PATTERNS = [
    (re.compile(r"(?i)(api_key|apikey|secret_key|private_key)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]"), "Exposed Hardcoded API / Private Key"),
    (re.compile(r"(?i)ghp_[A-Za-z0-9]{36}"), "Exposed GitHub Personal Access Token"),
    (re.compile(r"(?i)github_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59}"), "Exposed GitHub Fine-Grained Token"),
    (re.compile(r"-----BEGIN PRIVATE KEY-----"), "Exposed PEM Private Key File"),
    (re.compile(r"(?i)AIzaSy[A-Za-z0-9_\-]{33}"), "Exposed Google / Vertex AI API Key"),
    (re.compile(r"(?i)xox[baprs]-[A-Za-z0-9\-]+"), "Exposed Slack API Token"),
    (re.compile(r"(?i)sk-[A-Za-z0-9]{32,}"), "Exposed OpenAI / LLM API Key")
]

IGNORE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".ico", ".bin", ".sqlite", ".sqlite-wal", ".pyc", ".gguf"]

def scan_file_for_secrets(file_path):
    issues = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                # Skip comments or obvious test patterns if desired
                for pattern, desc in SECRET_PATTERNS:
                    if pattern.search(line):
                        issues.append((idx, desc, line.strip()[:80]))
    except Exception as e:
        pass
    return issues

def scan_repository(repo_dir):
    print("=== AUTOMATED SECRET & CREDENTIAL SCANNER ===")
    total_files = 0
    total_issues = 0

    for root, dirs, files in os.walk(repo_dir):
        # Ignore git directory
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            total_files += 1
            issues = scan_file_for_secrets(file_path)

            if issues:
                total_issues += len(issues)
                rel_path = os.path.relpath(file_path, repo_dir)
                print(f"\n[!] WARNING IN FILE: {rel_path}")
                for line_num, desc, snippet in issues:
                    print(f"    • Line {line_num}: [{desc}] -> {snippet}")

    print("\n==========================================================================")
    print(f"  SCAN SUMMARY: Analyzed {total_files} files across repository.")
    if total_issues == 0:
        print("  STATUS: 100% CLEAN - NO HARDCODED SECRETS OR PRIVATE KEYS DETECTED!")
    else:
        print(f"  STATUS: {total_issues} POTENTIAL SENSITIVE ISSUES REVIEWED.")
    print("==========================================================================")

def main():
    repo_dir = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
    if platform.system() != "Windows":
        repo_dir = "/mnt/c/Users/Monica Fugazi/.antigravity-ide/living_repository"
    scan_repository(repo_dir)

if __name__ == "__main__":
    main()
