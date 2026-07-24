#!/usr/bin/env python3
"""
Test Suite for POSIX Sandbox Path Validation Engine
Validates path normalization, backslash handling, drive letter conversion,
and boundary verification across Windows and Linux platforms.
"""

import sys
import unittest
from sandbox_path_validator import normalize_to_posix_path, convert_windows_to_wsl_posix, validate_sandbox_path

class TestSandboxPosixPaths(unittest.TestCase):

    def test_normalize_windows_backslashes(self):
        win_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\bin\app.py"
        posix = normalize_to_posix_path(win_path)
        self.assertEqual(posix, "C:/Users/Monica Fugazi/.antigravity-ide/living_repository/bin/app.py")

    def test_convert_to_wsl_posix(self):
        win_path = r"C:\AI_Dedicated_Storage_1TB\models"
        wsl = convert_windows_to_wsl_posix(win_path)
        self.assertEqual(wsl, "/mnt/c/AI_Dedicated_Storage_1TB/models")

    def test_sandbox_boundary_validation(self):
        valid_path = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository\scripts\build.py"
        sandbox_root = r"C:\Users\Monica Fugazi\.antigravity-ide\living_repository"
        result = validate_sandbox_path(valid_path, sandbox_root)
        self.assertTrue(result["is_valid_sandbox_path"])
        self.assertTrue(result["posix_path"].startswith("C:/Users/Monica Fugazi/.antigravity-ide/living_repository"))

if __name__ == "__main__":
    unittest.main()
