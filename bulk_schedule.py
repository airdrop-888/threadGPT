"""
Bulk Schedule Posts from CSV
Schedule multiple posts at once from a CSV file
"""

import csv
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.scheduler import Scheduler


def load_posts_from_csv(csv_file):
    """Load posts from CSV file"""
    posts = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is line 1)
                # Validate required fields
                if not row.get('content'):
                    print(f"[WARNING] Line {row_num}: Missing content, skipping")
                    continue
                
                # Parse datetime
                date = row.get('date', '').strip()
                time = row.get('time', '').strip()
                
                if not date or not time:
                    print(f"[WARNING] Line {row_num}: Missing date or time, skipping")
                    continue
                
                # Combine date and time
                try:
                    scheduled_time = f"{date} {time}"
                    # Validate format
                    datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M')
                except ValueError:
                    print(f"[ERROR] Line {row_num}: Invalid date/time format. Use YYYY-MM-DD HH:MM")
                    continue
                
                # Get media (optional)
                media = row.get('media', '').strip()
                media_list = [media] if media else None
                
                # Get hashtags (optional)
                hashtags = row.get('hashtags', '').strip()
                content = row['content']
                
                # Add hashtags to content if provided
                if hashtags:
                    # Split by comma or space
                    tag_list = [tag.strip() for tag in hashtags.replace(',', ' ').split()]
                    # Ensure # prefix
                    tag_list = [f"#{tag.lstrip('#')}" for tag in tag_list if tag]
                    content = f"{content}\n\n{' '.join(tag_list)}"
                
                posts.append({
                    'content': content,
                    'scheduled_time': scheduled_time,
                    'media': media_list,
                    'line': row_num
                })
        
        return posts
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {csv_file}")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return []


def schedule_posts(posts):
    """Schedule all posts"""
    scheduler = Scheduler()
    
    scheduled = 0
    failed = 0
    
    for post in posts:
        try:
            # Convert to datetime object for scheduler
            dt = datetime.strptime(post['scheduled_time'], '%Y-%m-%d %H:%M')
            
            post_id = scheduler.schedule_post(
                content=post['content'],
                post_time=post['scheduled_time'],
                media=post['media']
            )
            
            print(f"[OK] Line {post['line']}: Scheduled as {post_id}")
            scheduled += 1
            
        except ValueError as e:
            print(f"[ERROR] Line {post['line']}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] Line {post['line']}: {e}")
            failed += 1
    
    return scheduled, failed


def main():
    """Main entry point"""
    print("="*60)
    print("ThreadsGPT - Bulk Scheduler")
    print("="*60)
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\nUsage: python bulk_schedule.py <csv_file>")
        print("\nExample:")
        print("  python bulk_schedule.py schedule.csv")
        print("\nCSV Format:")
        print("  date,time,content,media,hashtags")
        print("  2024-10-07,09:00,\"Post content\",image.jpg,tech ai")
        print("\nSee schedule.example.csv for template")
        return 1
    
    csv_file = sys.argv[1]
    
    # Check if file exists
    if not Path(csv_file).exists():
        print(f"\n[ERROR] File not found: {csv_file}")
        print("\nCreate a CSV file with this format:")
        print("  date,time,content,media,hashtags")
        return 1
    
    print(f"\n[INFO] Reading from: {csv_file}")
    
    # Load posts
    posts = load_posts_from_csv(csv_file)
    
    if not posts:
        print("\n[ERROR] No valid posts found in CSV")
        return 1
    
    print(f"[INFO] Found {len(posts)} posts to schedule")
    
    # Confirm
    print("\n" + "="*60)
    print("Preview:")
    print("="*60)
    for i, post in enumerate(posts[:5], 1):  # Show first 5
        content_preview = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
        print(f"{i}. {post['scheduled_time']} - {content_preview}")
    
    if len(posts) > 5:
        print(f"... and {len(posts) - 5} more")
    
    print("\n" + "="*60)
    
    # Ask confirmation
    confirm = input("\nSchedule these posts? (yes/no): ").lower().strip()
    
    if confirm not in ['yes', 'y']:
        print("\n[CANCELLED] No posts scheduled")
        return 0
    
    # Schedule posts
    print("\n[INFO] Scheduling posts...")
    scheduled, failed = schedule_posts(posts)
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"[OK] Successfully scheduled: {scheduled}")
    if failed > 0:
        print(f"[ERROR] Failed: {failed}")
    
    print("\nNext steps:")
    print("  python main.py schedule  # View all scheduled posts")
    print("  python main.py status    # Check system status")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
