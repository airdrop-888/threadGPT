"""
ThreadsGPT Threads API Client
Handle all interactions with Threads GraphQL API
"""

import requests
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import urllib.parse


class ThreadsAPI:
    """Client for interacting with Threads.net GraphQL API"""
    
    def __init__(self, session_file: str = "threads_session.json"):
        self.session_file = session_file
        self.session_data = self._load_session()
        self.base_url = "https://www.threads.com/api/graphql"
        
        # Setup requests session
        self.session = requests.Session()
        self._setup_headers()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 10  # seconds between requests
        
    def _load_session(self) -> Dict:
        """Load session data from file"""
        session_path = Path(self.session_file)
        if not session_path.exists():
            raise FileNotFoundError(
                f"Session file not found: {self.session_file}\n"
                "Run 'python extract_cookies.py' first."
            )
        
        with open(session_path, 'r') as f:
            return json.load(f)
    
    def _setup_headers(self):
        """Setup request headers from session data"""
        headers = self.session_data.get('headers', {})
        
        # Required headers for Threads API
        self.session.headers.update({
            'authority': 'www.threads.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.threads.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': headers.get('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'x-ig-app-id': headers.get('x-ig-app-id', '238260118697367'),
            'x-asbd-id': headers.get('x-asbd-id', '359341'),
        })
        
        # Add authentication headers if available
        if 'x-csrftoken' in headers:
            self.session.headers['x-csrftoken'] = headers['x-csrftoken']
        if 'x-fb-lsd' in headers:
            self.session.headers['x-fb-lsd'] = headers['x-fb-lsd']
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def _make_request(self, payload: Dict) -> Dict:
        """
        Make GraphQL request to Threads API
        
        Args:
            payload: Request payload
            
        Returns:
            Response data
        """
        self._rate_limit()
        
        try:
            response = self.session.post(
                self.base_url,
                data=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {}
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Get user profile information
        
        Args:
            username: Username to fetch (without @)
            
        Returns:
            User profile data or None
        """
        # Build GraphQL query for user profile
        # This is a placeholder - actual query structure from HAR file
        variables = {
            "username": username
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': '12345',  # Replace with actual doc_id from HAR
        }
        
        # Add session params from HAR
        headers = self.session_data.get('headers', {})
        if 'fb_dtsg' in headers:
            payload['fb_dtsg'] = headers['fb_dtsg']
        if 'lsd' in headers:
            payload['lsd'] = headers['lsd']
        
        result = self._make_request(payload)
        
        # Parse response
        # Structure depends on actual API response
        return result
    
    def get_user_threads(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get threads from a user
        
        Args:
            user_id: User ID
            limit: Number of threads to fetch
            
        Returns:
            List of threads
        """
        threads = []
        
        # Placeholder for actual implementation
        # Would use BarcelonaProfileThreadsTabQuery or similar
        
        return threads
    
    def create_thread(self, content: str, media: Optional[List[str]] = None) -> Optional[str]:
        """
        Create a new thread
        
        Args:
            content: Thread text content
            media: Optional list of media URLs/paths
            
        Returns:
            Thread ID if successful, None otherwise
        """
        # Build create thread payload
        variables = {
            "text": content,
            "publish_mode": "text_post",
        }
        
        if media:
            variables["media"] = media
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': '67890',  # Replace with actual create thread doc_id
        }
        
        # Add auth params
        headers = self.session_data.get('headers', {})
        if 'fb_dtsg' in headers:
            payload['fb_dtsg'] = headers['fb_dtsg']
        if 'lsd' in headers:
            payload['lsd'] = headers['lsd']
        
        result = self._make_request(payload)
        
        # Extract thread ID from response
        if result and 'data' in result:
            return result.get('data', {}).get('thread_id')
        
        return None
    
    def like_thread(self, thread_id: str) -> bool:
        """
        Like a thread
        
        Args:
            thread_id: Thread ID to like
            
        Returns:
            True if successful
        """
        variables = {
            "media_id": thread_id
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'like_doc_id',  # Replace with actual
        }
        
        result = self._make_request(payload)
        return bool(result)
    
    def reply_to_thread(self, thread_id: str, content: str) -> Optional[str]:
        """
        Reply to a thread
        
        Args:
            thread_id: Thread to reply to
            content: Reply content
            
        Returns:
            Reply ID if successful
        """
        variables = {
            "parent_post_id": thread_id,
            "text": content
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'reply_doc_id',  # Replace with actual
        }
        
        result = self._make_request(payload)
        
        if result and 'data' in result:
            return result.get('data', {}).get('reply_id')
        
        return None
    
    def search_threads(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for threads
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            List of matching threads
        """
        variables = {
            "query": query,
            "count": limit
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'search_doc_id',  # Replace with actual
        }
        
        result = self._make_request(payload)
        
        # Parse and return results
        return []
    
    def get_notifications(self, limit: int = 50) -> List[Dict]:
        """
        Get notifications/activity
        
        Args:
            limit: Number of notifications
            
        Returns:
            List of notifications
        """
        variables = {
            "count": limit
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'notifications_doc_id',
        }
        
        result = self._make_request(payload)
        return []
    
    def follow_user(self, user_id: str) -> bool:
        """
        Follow a user
        
        Args:
            user_id: User ID to follow
            
        Returns:
            True if successful
        """
        variables = {
            "user_id": user_id
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'follow_doc_id',
        }
        
        result = self._make_request(payload)
        return bool(result)
    
    def unfollow_user(self, user_id: str) -> bool:
        """
        Unfollow a user
        
        Args:
            user_id: User ID to unfollow
            
        Returns:
            True if successful
        """
        variables = {
            "user_id": user_id
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'unfollow_doc_id',
        }
        
        result = self._make_request(payload)
        return bool(result)
    
    def get_feed(self, feed_type: str = "for_you", limit: int = 20) -> List[Dict]:
        """
        Get feed posts
        
        Args:
            feed_type: 'for_you', 'following', or 'trending'
            limit: Number of posts
            
        Returns:
            List of feed posts
        """
        variables = {
            "feed_type": feed_type,
            "count": limit
        }
        
        payload = {
            'variables': json.dumps(variables),
            'doc_id': 'feed_doc_id',
        }
        
        result = self._make_request(payload)
        return []


if __name__ == "__main__":
    # Test API client
    print("Testing ThreadsGPT API Client...")
    
    try:
        api = ThreadsAPI()
        print("✓ API Client initialized")
        print(f"✓ Session loaded with {len(api.session.headers)} headers")
        
        # Test profile fetch (will need real implementation)
        print("\n[INFO] API client ready for testing with real endpoints")
        print("[INFO] Replace doc_id placeholders with actual values from HAR file")
        
    except Exception as e:
        print(f"✗ Error: {e}")
