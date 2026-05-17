"""
Quick Validation Script
Run this to verify all Python files are syntactically correct.

Usage: python validate.py
"""

import py_compile
import os
from pathlib import Path

files_to_check = [
    'main.py',
    'config.py',
    'models.py',
    'schemas.py',
    'auth_utils.py',
    'auth_routes.py',
    'task_routes.py',
]

print("🔍 Validating Python files...\n")

errors = []
for filename in files_to_check:
    filepath = Path(filename)
    if not filepath.exists():
        errors.append(f"❌ {filename} - FILE NOT FOUND")
        continue
    
    try:
        py_compile.compile(str(filepath), doraise=True)
        print(f"✅ {filename}")
    except py_compile.PyCompileError as e:
        errors.append(f"❌ {filename} - SYNTAX ERROR\n   {str(e)}")

print("\n" + "="*50)

if errors:
    print("⚠️  VALIDATION ISSUES FOUND:\n")
    for error in errors:
        print(error)
else:
    print("✅ ALL FILES VALID - Ready to run!")
    print("\nNext step: pip install -r requirements.txt")
    print("Then: python main.py")
