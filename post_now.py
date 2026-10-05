"""
ThreadsGPT - Post Now (Instant)
Test posting directly to Threads without waiting for scheduler
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    print("="*60)
    print("ThreadsGPT - Post Now (Instant Test)")
    print("="*60)

    # Validate config
    try:
        from src.core.api_client import ThreadsAPI
        api = ThreadsAPI()
        print("\n[OK] Config loaded")
        print(f"[OK] User ID: {api.cookies_cfg['ds_user_id']}")
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        return 1
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        return 1

    # Get post content from user
    print("\n" + "="*60)
    print("Enter your post content below.")
    print("(Press Enter twice when done)")
    print("="*60 + "\n")

    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)

    content = "\n".join(lines).strip()

    if not content:
        print("\n[ERROR] Content cannot be empty!")
        return 1

    print(f"\n[INFO] Content ({len(content)} chars):")
    print("-"*40)
    print(content[:200])
    print("-"*40)

    # Confirm
    confirm = input("\nPost this to Threads NOW? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y']:
        print("\n[CANCELLED]")
        return 0

    # Post!
    print("\n[INFO] Posting to Threads...")
    result = api.create_post(text=content)

    if result.get('success'):
        print("\n[SUCCESS] Post published to Threads!")
        print("Check your Threads account now.")
        return 0
    else:
        print(f"\n[FAILED] Could not post: {result.get('error')}")
        print("\nPossible causes:")
        print("  - Cookies expired -> get fresh cookies from browser")
        print("  - Wrong sessionid -> copy again from F12 > Application > Cookies")
        return 1


if __name__ == "__main__":
    sys.exit(main())
