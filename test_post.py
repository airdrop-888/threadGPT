"""
Test your ThreadsGPT setup with a test post
"""

import sys
import io
from pathlib import Path
from datetime import datetime, timedelta

# Fix Windows console encoding for non-ASCII chars
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.scheduler import Scheduler


def main():
    """Test schedule with a test post"""
    print("="*60)
    print("ThreadsGPT - Test Post")
    print("="*60)

    try:
        # Initialize scheduler
        scheduler = Scheduler()
        print("\n[OK] Scheduler initialized")

        # Test content (plain text, safe for any encoding)
        test_content = (
            "Test post from ThreadsGPT!\n\n"
            "If you see this, the scheduler is working!\n\n"
            "#ThreadsGPT #Automation"
        )

        # Schedule for 2 minutes from now
        test_time = datetime.now(scheduler.timezone) + timedelta(minutes=2)
        test_time_str = test_time.strftime('%Y-%m-%d %H:%M')

        print(f"\n[INFO] Scheduled for : {test_time_str}")
        print(f"[INFO] Content       : {test_content.splitlines()[0]}")

        # Confirm
        print("\n" + "="*60)
        confirm = input("Schedule this test post? (yes/no): ").lower().strip()

        if confirm not in ['yes', 'y']:
            print("\n[CANCELLED] No post scheduled.")
            return 0

        # Schedule the post
        post_id = scheduler.schedule_post(
            content=test_content,
            post_time=test_time_str
        )

        print("\n[SUCCESS] Test post scheduled!")
        print(f"[INFO] Post ID  : {post_id}")
        print(f"[INFO] Posts at : {test_time.strftime('%H:%M')} (in ~2 minutes)")
        print("\n" + "="*60)
        print("Next steps:")
        print("  1. Wait 2 minutes")
        print("  2. Check your Threads account")
        print("  3. Post appears = SUCCESS!")
        print("  4. No post = Check cookies in config.yaml")
        print("\nView schedule:")
        print("  python main.py schedule")

        scheduler.shutdown()
        return 0

    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nSetup config.yaml first:")
        print("  copy config.example.yaml config.yaml")
        print("  python setup_cookies.py")
        return 1

    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
