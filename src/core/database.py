"""
ThreadsGPT Database Layer
Store and manage historical data using SQLite
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class Database:
    """Database manager for ThreadsGPT"""
    
    def __init__(self, db_path: str = "data/threadsgpt.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dicts
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()
        
        # Account stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                followers INTEGER,
                following INTEGER,
                posts_count INTEGER,
                engagement_rate REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                content TEXT,
                likes INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                reposts INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                posted_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'published',
                metadata TEXT
            )
        """)
        
        # Scheduled posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                media TEXT,
                scheduled_time TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'scheduled',
                attempts INTEGER DEFAULT 0,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                posted_at TIMESTAMP
            )
        """)
        
        # Viral posts tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viral_posts (
                id TEXT PRIMARY KEY,
                username TEXT,
                content TEXT,
                engagement INTEGER,
                likes INTEGER,
                replies INTEGER,
                reposts INTEGER,
                viral_score REAL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Analytics snapshots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_type TEXT,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Activity log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                details TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_username ON posts(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_posted_at ON posts(posted_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scheduled_status ON scheduled_posts(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_created ON activity_log(created_at)")
        
        self.conn.commit()
    
    # Account Stats Methods
    def save_account_stats(self, username: str, stats: Dict):
        """Save account statistics snapshot"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO account_stats 
            (username, followers, following, posts_count, engagement_rate)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            stats.get('followers', 0),
            stats.get('following', 0),
            stats.get('posts', 0),
            stats.get('engagement_rate', 0.0)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_account_history(self, username: str, days: int = 30) -> List[Dict]:
        """Get account stats history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM account_stats
            WHERE username = ?
            AND recorded_at >= datetime('now', '-' || ? || ' days')
            ORDER BY recorded_at DESC
        """, (username, days))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # Posts Methods
    def save_post(self, post_data: Dict):
        """Save a post to database"""
        cursor = self.conn.cursor()
        
        metadata = {k: v for k, v in post_data.items() 
                   if k not in ['id', 'username', 'content', 'likes', 'replies', 
                               'reposts', 'views', 'engagement_rate', 'posted_at']}
        
        cursor.execute("""
            INSERT OR REPLACE INTO posts
            (id, username, content, likes, replies, reposts, views, 
             engagement_rate, posted_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post_data.get('id'),
            post_data.get('username'),
            post_data.get('content'),
            post_data.get('likes', 0),
            post_data.get('replies', 0),
            post_data.get('reposts', 0),
            post_data.get('views', 0),
            post_data.get('engagement_rate', 0.0),
            post_data.get('posted_at'),
            json.dumps(metadata)
        ))
        self.conn.commit()
    
    def get_posts(self, username: Optional[str] = None, 
                  limit: int = 50, 
                  order_by: str = 'posted_at') -> List[Dict]:
        """Get posts from database"""
        cursor = self.conn.cursor()
        
        if username:
            cursor.execute(f"""
                SELECT * FROM posts
                WHERE username = ?
                ORDER BY {order_by} DESC
                LIMIT ?
            """, (username, limit))
        else:
            cursor.execute(f"""
                SELECT * FROM posts
                ORDER BY {order_by} DESC
                LIMIT ?
            """, (limit,))
        
        posts = [dict(row) for row in cursor.fetchall()]
        
        # Parse metadata JSON
        for post in posts:
            if post.get('metadata'):
                try:
                    post['metadata'] = json.loads(post['metadata'])
                except:
                    pass
        
        return posts
    
    def get_top_posts(self, limit: int = 10, metric: str = 'engagement_rate') -> List[Dict]:
        """Get top performing posts"""
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT * FROM posts
            ORDER BY {metric} DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def update_post_metrics(self, post_id: str, metrics: Dict):
        """Update post engagement metrics"""
        cursor = self.conn.cursor()
        
        set_clause = ", ".join([f"{key} = ?" for key in metrics.keys()])
        values = list(metrics.values()) + [post_id]
        
        cursor.execute(f"""
            UPDATE posts
            SET {set_clause}
            WHERE id = ?
        """, values)
        self.conn.commit()
    
    # Scheduled Posts Methods
    def save_scheduled_post(self, post_data: Dict):
        """Save scheduled post"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO scheduled_posts
            (id, content, media, scheduled_time, status, attempts)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            post_data['id'],
            post_data['content'],
            json.dumps(post_data.get('media', [])),
            post_data['scheduled_time'],
            post_data.get('status', 'scheduled'),
            post_data.get('attempts', 0)
        ))
        self.conn.commit()
    
    def get_scheduled_posts(self, status: str = 'scheduled') -> List[Dict]:
        """Get scheduled posts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM scheduled_posts
            WHERE status = ?
            ORDER BY scheduled_time ASC
        """, (status,))
        
        posts = [dict(row) for row in cursor.fetchall()]
        
        for post in posts:
            if post.get('media'):
                try:
                    post['media'] = json.loads(post['media'])
                except:
                    pass
        
        return posts
    
    def update_scheduled_post_status(self, post_id: str, status: str, 
                                    error: Optional[str] = None):
        """Update scheduled post status"""
        cursor = self.conn.cursor()
        
        if status == 'posted':
            cursor.execute("""
                UPDATE scheduled_posts
                SET status = ?, posted_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, post_id))
        elif status == 'failed':
            cursor.execute("""
                UPDATE scheduled_posts
                SET status = ?, error = ?, attempts = attempts + 1
                WHERE id = ?
            """, (status, error, post_id))
        else:
            cursor.execute("""
                UPDATE scheduled_posts
                SET status = ?
                WHERE id = ?
            """, (status, post_id))
        
        self.conn.commit()
    
    # Viral Posts Methods
    def save_viral_post(self, post_data: Dict):
        """Save detected viral post"""
        cursor = self.conn.cursor()
        
        metadata = {k: v for k, v in post_data.items()
                   if k not in ['id', 'username', 'content', 'engagement', 
                               'likes', 'replies', 'reposts', 'viral_score']}
        
        cursor.execute("""
            INSERT OR REPLACE INTO viral_posts
            (id, username, content, engagement, likes, replies, reposts, 
             viral_score, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post_data.get('id'),
            post_data.get('username'),
            post_data.get('content'),
            post_data.get('engagement', 0),
            post_data.get('likes', 0),
            post_data.get('replies', 0),
            post_data.get('reposts', 0),
            post_data.get('viral_score', 0.0),
            json.dumps(metadata)
        ))
        self.conn.commit()
    
    def get_viral_posts(self, limit: int = 50, min_score: float = 7.0) -> List[Dict]:
        """Get viral posts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM viral_posts
            WHERE viral_score >= ?
            ORDER BY detected_at DESC
            LIMIT ?
        """, (min_score, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # Analytics Methods
    def save_analytics_snapshot(self, snapshot_type: str, data: Dict):
        """Save analytics snapshot"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO analytics_snapshots (snapshot_type, data)
            VALUES (?, ?)
        """, (snapshot_type, json.dumps(data)))
        self.conn.commit()
    
    def get_analytics_snapshots(self, snapshot_type: str, days: int = 30) -> List[Dict]:
        """Get analytics snapshots"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM analytics_snapshots
            WHERE snapshot_type = ?
            AND created_at >= datetime('now', '-' || ? || ' days')
            ORDER BY created_at DESC
        """, (snapshot_type, days))
        
        snapshots = [dict(row) for row in cursor.fetchall()]
        
        for snapshot in snapshots:
            if snapshot.get('data'):
                try:
                    snapshot['data'] = json.loads(snapshot['data'])
                except:
                    pass
        
        return snapshots
    
    # Activity Log Methods
    def log_activity(self, action_type: str, details: str, status: str = 'success'):
        """Log an activity"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO activity_log (action_type, details, status)
            VALUES (?, ?, ?)
        """, (action_type, details, status))
        self.conn.commit()
    
    def get_activity_log(self, limit: int = 100, 
                        action_type: Optional[str] = None) -> List[Dict]:
        """Get activity log"""
        cursor = self.conn.cursor()
        
        if action_type:
            cursor.execute("""
                SELECT * FROM activity_log
                WHERE action_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (action_type, limit))
        else:
            cursor.execute("""
                SELECT * FROM activity_log
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # Utility Methods
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute custom SQL query"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()


if __name__ == "__main__":
    # Test database
    print("Testing ThreadsGPT Database...")
    
    try:
        db = Database()
        print("✓ Database initialized")
        
        # Test saving account stats
        db.save_account_stats("test_user", {
            'followers': 100,
            'following': 50,
            'posts': 10,
            'engagement_rate': 5.5
        })
        print("✓ Account stats saved")
        
        # Test retrieving history
        history = db.get_account_history("test_user", days=7)
        print(f"✓ Retrieved {len(history)} history records")
        
        # Test activity log
        db.log_activity("test", "Database test successful", "success")
        print("✓ Activity logged")
        
        db.close()
        print("✓ Database closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
