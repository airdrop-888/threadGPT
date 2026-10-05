"""
ThreadsGPT Smart Scheduler
Intelligent post scheduling with optimal timing
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import pytz


class Scheduler:
    """Smart scheduling system for Threads posts"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config = self._load_config(config_file)
        self.queue_file = Path("data/post_queue.json")
        self.scheduler = BackgroundScheduler()
        self.timezone = pytz.timezone(self.config.get('scheduler', {}).get('timezone', 'UTC'))
        
        # Create queue file if doesn't exist
        if not self.queue_file.exists():
            self._save_queue([])
        
        # Start scheduler
        self.scheduler.start()
    
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration"""
        config_path = Path(config_file)
        if not config_path.exists():
            # Return default config
            return {
                'scheduler': {
                    'fallback_times': ['09:00', '12:00', '19:00', '21:00'],
                    'timezone': 'Asia/Jakarta',
                    'auto_detect_best_time': True
                },
                'limits': {
                    'posts_per_day': 5,
                    'min_delay_between_posts': 3600
                }
            }
        
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_queue(self) -> List[Dict]:
        """Load post queue from file"""
        if not self.queue_file.exists():
            return []
        
        with open(self.queue_file, 'r') as f:
            return json.load(f)
    
    def _save_queue(self, queue: List[Dict]):
        """Save post queue to file"""
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2, default=str)
    
    def schedule_post(self, content: str, post_time: str = 'auto', 
                     media: Optional[List[str]] = None) -> str:
        """
        Schedule a new post
        
        Args:
            content: Post content
            post_time: Time to post ('auto' or 'HH:MM')
            media: List of media file paths
            
        Returns:
            Post ID
        """
        queue = self._load_queue()
        
        # Generate post ID
        post_id = f"post_{int(time.time() * 1000)}"
        
        # Determine posting time
        if post_time == 'auto':
            scheduled_time = self._get_optimal_time()
        else:
            scheduled_time = self._parse_time(post_time)
        
        # Check limits
        if not self._check_daily_limit(scheduled_time):
            raise ValueError("Daily post limit reached!")
        
        # Create post entry
        post = {
            'id': post_id,
            'content': content,
            'media': media or [],
            'scheduled_time': scheduled_time.isoformat(),
            'status': 'scheduled',
            'created_at': datetime.now(self.timezone).isoformat(),
            'attempts': 0
        }
        
        queue.append(post)
        self._save_queue(queue)
        
        # Schedule with APScheduler
        self.scheduler.add_job(
            func=self._execute_post,
            trigger=DateTrigger(run_date=scheduled_time),
            args=[post_id],
            id=post_id,
            replace_existing=True
        )
        
        return post_id
    
    def _get_optimal_time(self) -> datetime:
        """
        Get optimal posting time
        
        Returns:
            Datetime object for next optimal time
        """
        # Get fallback times from config
        fallback_times = self.config.get('scheduler', {}).get('fallback_times', ['19:00'])
        
        # TODO: Implement smart time detection based on analytics
        # For now, use fallback times
        
        now = datetime.now(self.timezone)
        
        for time_str in fallback_times:
            hour, minute = map(int, time_str.split(':'))
            scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if scheduled <= now:
                scheduled += timedelta(days=1)
            
            # Check if this time slot is available
            if self._is_time_slot_available(scheduled):
                return scheduled
        
        # If all slots taken, schedule for next day
        return now.replace(hour=19, minute=0, second=0, microsecond=0) + timedelta(days=1)
    
    def _parse_time(self, time_str: str) -> datetime:
        """Parse time string to datetime.
        
        Supports:
            - 'HH:MM'            e.g. '19:00'
            - 'YYYY-MM-DD HH:MM' e.g. '2026-10-05 18:53'
        """
        now = datetime.now(self.timezone)
        
        # Full datetime string: 'YYYY-MM-DD HH:MM'
        if len(time_str) > 5:
            try:
                naive = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                scheduled = self.timezone.localize(naive)
                return scheduled
            except ValueError:
                pass
        
        # Time only: 'HH:MM'
        try:
            hour, minute = map(int, time_str.split(':'))
            scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has already passed today, schedule for tomorrow
            if scheduled <= now:
                scheduled += timedelta(days=1)
            
            return scheduled
        except ValueError:
            raise ValueError(
                f"Invalid time format: '{time_str}'\n"
                "Use 'HH:MM' (e.g. '19:00') or 'YYYY-MM-DD HH:MM' (e.g. '2026-10-07 09:00')"
            )
    
    def _is_time_slot_available(self, target_time: datetime) -> bool:
        """Check if time slot is available"""
        queue = self._load_queue()
        min_delay = self.config.get('limits', {}).get('min_delay_between_posts', 3600)
        
        for post in queue:
            if post['status'] != 'scheduled':
                continue
            
            post_time = datetime.fromisoformat(post['scheduled_time'])
            time_diff = abs((target_time - post_time).total_seconds())
            
            if time_diff < min_delay:
                return False
        
        return True
    
    def _check_daily_limit(self, target_time: datetime) -> bool:
        """Check if daily posting limit reached"""
        queue = self._load_queue()
        daily_limit = self.config.get('limits', {}).get('posts_per_day', 5)
        
        target_date = target_time.date()
        posts_on_date = sum(
            1 for post in queue
            if datetime.fromisoformat(post['scheduled_time']).date() == target_date
            and post['status'] == 'scheduled'
        )
        
        return posts_on_date < daily_limit
    
    def _execute_post(self, post_id: str):
        """
        Execute a scheduled post by calling the real Threads API.

        Args:
            post_id: ID of the post to send
        """
        queue = self._load_queue()

        # Find post in queue
        post = next((p for p in queue if p['id'] == post_id), None)
        if not post:
            print(f"[ERROR] Post {post_id} not found in queue!")
            return

        print(f"[INFO] Executing post: {post_id}")
        print(f"[INFO] Content: {post['content'][:60]}...")

        try:
            from src.core.api_client import ThreadsAPI

            api = ThreadsAPI()
            result = api.create_post(
                text=post['content'],
                media_paths=post.get('media') or None
            )

            if result.get('success'):
                post['status']    = 'posted'
                post['posted_at'] = datetime.now(self.timezone).isoformat()
                self._save_queue(queue)
                print(f"[SUCCESS] Post {post_id} published!")

            else:
                error = result.get('error', 'Unknown error')
                print(f"[ERROR] Failed to publish post: {error}")
                post['status']  = 'failed'
                post['error']   = error
                post['attempts'] = post.get('attempts', 0) + 1
                self._save_queue(queue)

                # Auto-retry up to 3 times (30 min gap)
                if post['attempts'] < 3:
                    retry_time = datetime.now(self.timezone) + timedelta(minutes=30)
                    self.scheduler.add_job(
                        func=self._execute_post,
                        trigger=DateTrigger(run_date=retry_time),
                        args=[post_id],
                        id=f"{post_id}_retry_{post['attempts']}",
                        replace_existing=True
                    )
                    print(f"[INFO] Retry scheduled in 30 minutes.")

        except Exception as e:
            print(f"[ERROR] Exception while posting: {e}")
            post['status']   = 'failed'
            post['error']    = str(e)
            post['attempts'] = post.get('attempts', 0) + 1
            self._save_queue(queue)


    
    def get_queue(self) -> List[Dict]:
        """Get all scheduled posts"""
        queue = self._load_queue()
        return [p for p in queue if p['status'] == 'scheduled']
    
    def cancel_post(self, post_id: str) -> bool:
        """
        Cancel a scheduled post
        
        Args:
            post_id: Post ID to cancel
            
        Returns:
            True if cancelled successfully
        """
        queue = self._load_queue()
        
        post = next((p for p in queue if p['id'] == post_id), None)
        if not post:
            return False
        
        # Remove from scheduler
        try:
            self.scheduler.remove_job(post_id)
        except:
            pass
        
        # Update status
        post['status'] = 'cancelled'
        self._save_queue(queue)
        
        return True
    
    def reschedule_post(self, post_id: str, new_time: str) -> bool:
        """
        Reschedule a post
        
        Args:
            post_id: Post ID to reschedule
            new_time: New time ('auto' or 'HH:MM')
            
        Returns:
            True if rescheduled successfully
        """
        queue = self._load_queue()
        
        post = next((p for p in queue if p['id'] == post_id), None)
        if not post or post['status'] != 'scheduled':
            return False
        
        # Cancel old schedule
        try:
            self.scheduler.remove_job(post_id)
        except:
            pass
        
        # Determine new time
        if new_time == 'auto':
            scheduled_time = self._get_optimal_time()
        else:
            scheduled_time = self._parse_time(new_time)
        
        # Update post
        post['scheduled_time'] = scheduled_time.isoformat()
        self._save_queue(queue)
        
        # Reschedule
        self.scheduler.add_job(
            func=self._execute_post,
            trigger=DateTrigger(run_date=scheduled_time),
            args=[post_id],
            id=post_id,
            replace_existing=True
        )
        
        return True
    
    def get_next_optimal_slots(self, count: int = 5) -> List[str]:
        """
        Get next N optimal time slots
        
        Args:
            count: Number of slots to return
            
        Returns:
            List of time strings
        """
        slots = []
        current = datetime.now(self.timezone)
        
        while len(slots) < count:
            current += timedelta(hours=2)  # Check every 2 hours
            if self._is_time_slot_available(current):
                slots.append(current.strftime('%Y-%m-%d %H:%M'))
        
        return slots
    
    def shutdown(self):
        """Shutdown scheduler"""
        self.scheduler.shutdown()


if __name__ == "__main__":
    # Test scheduler
    print("Testing ThreadsGPT Scheduler...")
    
    try:
        scheduler = Scheduler()
        print("✓ Scheduler initialized")
        
        # Get queue
        queue = scheduler.get_queue()
        print(f"✓ Current queue: {len(queue)} posts")
        
        # Get optimal slots
        slots = scheduler.get_next_optimal_slots(3)
        print(f"✓ Next optimal slots: {slots}")
        
        scheduler.shutdown()
        
    except Exception as e:
        print(f"✗ Error: {e}")
