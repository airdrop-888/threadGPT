"""
Test your ThreadsGPT setup with a test post
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

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
        
        # Create test post
        test_content = "🤖 Test post from ThreadsGPT!\n\nIf you see this, the scheduler is working! ✅\n\n#ThreadsGPT #Automation"
        
        # Schedule for 2 minutes from now (quick test)
        test_time = datetime.now(scheduler.timezone) + timedelta(minutes=2)
        
        print(f"\n[INFO] Scheduling test post for: {test_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"[INFO] Content: {test_content[:50]}...")
        
        # Confirm
        print("\n" + "="*60)
        confirm = input("Schedule this test post? (yes/no): ").lower().strip()
        
        if confirm not in ['yes', 'y']:
            print("\n[CANCELLED] Test post not scheduled")
            return 0
        
        # Schedule the post
        post_id = scheduler.schedule_post(
            content=test_content,
            post_time=test_time.strftime('%Y-%m-%d %H:%M')
        )
        
        print("\n[SUCCESS] Test post scheduled!")
        print(f"[INFO] Post ID: {post_id}")
        print(f"[INFO] Will post in ~2 minutes at {test_time.strftime('%H:%M')}")
        
        print("\n" + "="*60)
        print("Next steps:")
        print("="*60)
        print("1. Wait 2 minutes")
        print("2. Check your Threads account")
        print("3. If post appears → SUCCESS! ✅")
        print("4. If not → Check config.yaml cookies")
        
        print("\nView schedule:")
        print("  python main.py schedule")
        
        scheduler.shutdown()
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nDid you setup config.yaml?")
        print("Run: python setup_cookies.py")
        return 1
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
