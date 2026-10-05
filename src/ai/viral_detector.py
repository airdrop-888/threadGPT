"""
ThreadsGPT Viral Content Detector
Identify trending content and patterns
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time


class ViralDetector:
    """Detect and analyze viral content on Threads"""
    
    def __init__(self, session_file: str = "threads_session.json"):
        self.session_file = session_file
        self.session_data = self._load_session()
        self.base_url = "https://www.threads.com/api/graphql"
        
        # Setup session
        self.session = requests.Session()
        self.session.headers.update(self.session_data.get('headers', {}))
    
    def _load_session(self) -> Dict:
        """Load session data"""
        session_path = Path(self.session_file)
        if not session_path.exists():
            raise FileNotFoundError(
                f"Session file not found: {self.session_file}\n"
                "Run 'python extract_cookies.py' first."
            )
        
        with open(session_path, 'r') as f:
            return json.load(f)
    
    def find_trending(self, niche: Optional[str] = None, 
                     limit: int = 10, 
                     min_engagement: int = 100) -> List[Dict]:
        """
        Find trending posts
        
        Args:
            niche: Specific niche/topic to search
            limit: Number of posts to return
            min_engagement: Minimum engagement threshold
            
        Returns:
            List of trending posts with metadata
        """
        # Placeholder implementation
        # In production, this would make actual API calls to Threads
        
        trending_posts = []
        
        # Example structure of what we would return
        example_post = {
            'id': 'post_123',
            'text': 'Example viral post content...',
            'author': 'username',
            'engagement': 250,
            'likes': 150,
            'replies': 50,
            'reposts': 50,
            'posted_at': datetime.now().isoformat(),
            'url': 'https://threads.com/@username/post/123',
            'media': [],
            'hashtags': ['#viral', '#trending'],
            'viral_score': 8.5
        }
        
        return trending_posts
    
    def analyze_viral_patterns(self, posts: List[Dict]) -> Dict:
        """
        Analyze patterns in viral posts
        
        Args:
            posts: List of posts to analyze
            
        Returns:
            Pattern analysis results
        """
        if not posts:
            return {}
        
        analysis = {
            'total_analyzed': len(posts),
            'patterns': {
                'average_length': 0,
                'common_hashtags': [],
                'common_keywords': [],
                'optimal_posting_times': [],
                'media_usage': {
                    'images': 0,
                    'videos': 0,
                    'text_only': 0
                },
                'engagement_triggers': []
            },
            'content_types': {
                'question': 0,
                'statement': 0,
                'call_to_action': 0,
                'story': 0
            },
            'recommendations': []
        }
        
        # Analyze each post
        for post in posts:
            content = post.get('text', '')
            
            # Length analysis
            analysis['patterns']['average_length'] += len(content)
            
            # Content type detection
            if '?' in content:
                analysis['content_types']['question'] += 1
            if any(cta in content.lower() for cta in ['click', 'check', 'follow', 'try']):
                analysis['content_types']['call_to_action'] += 1
        
        # Calculate averages
        if posts:
            analysis['patterns']['average_length'] //= len(posts)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate content recommendations based on analysis"""
        recommendations = []
        
        avg_length = analysis['patterns']['average_length']
        if avg_length > 0:
            recommendations.append(
                f"Optimal content length: {avg_length} characters"
            )
        
        # Content type recommendations
        content_types = analysis['content_types']
        if content_types['question'] > len(analysis) / 2:
            recommendations.append("Questions generate high engagement - ask your audience!")
        
        return recommendations
    
    def calculate_viral_score(self, post: Dict) -> float:
        """
        Calculate viral potential score (0-10)
        
        Args:
            post: Post data
            
        Returns:
            Viral score
        """
        score = 0.0
        
        # Engagement metrics
        engagement = post.get('engagement', 0)
        if engagement > 1000:
            score += 3.0
        elif engagement > 500:
            score += 2.0
        elif engagement > 100:
            score += 1.0
        
        # Timing (recent posts score higher)
        posted_at = post.get('posted_at')
        if posted_at:
            post_time = datetime.fromisoformat(posted_at.replace('Z', '+00:00'))
            hours_ago = (datetime.now() - post_time).total_seconds() / 3600
            
            if hours_ago < 6:
                score += 3.0
            elif hours_ago < 24:
                score += 2.0
            elif hours_ago < 48:
                score += 1.0
        
        # Media presence
        if post.get('media'):
            score += 2.0
        
        # Hashtags
        hashtags = post.get('hashtags', [])
        if 1 <= len(hashtags) <= 3:
            score += 1.0
        
        # Content length (optimal range)
        content = post.get('text', '')
        if 100 <= len(content) <= 280:
            score += 1.0
        
        return min(score, 10.0)
    
    def track_competitor(self, username: str, days: int = 7) -> Dict:
        """
        Track competitor's content performance
        
        Args:
            username: Competitor username
            days: Number of days to analyze
            
        Returns:
            Competitor analysis
        """
        analysis = {
            'username': username,
            'period_days': days,
            'total_posts': 0,
            'average_engagement': 0,
            'posting_frequency': 0,
            'top_posts': [],
            'content_themes': [],
            'hashtag_usage': []
        }
        
        return analysis
    
    def find_trending_hashtags(self, limit: int = 20) -> List[Dict]:
        """
        Find trending hashtags
        
        Args:
            limit: Number of hashtags to return
            
        Returns:
            List of trending hashtags with usage stats
        """
        # Placeholder
        return []
    
    def monitor_keywords(self, keywords: List[str], 
                        callback=None) -> List[Dict]:
        """
        Monitor specific keywords in real-time
        
        Args:
            keywords: List of keywords to monitor
            callback: Optional callback function for new matches
            
        Returns:
            List of posts matching keywords
        """
        matches = []
        
        # In production, this would continuously monitor the feed
        # For now, return empty list
        
        return matches
    
    def extract_content_dna(self, post: Dict) -> Dict:
        """
        Extract the 'DNA' of a successful post
        
        Args:
            post: Viral post to analyze
            
        Returns:
            Content DNA breakdown
        """
        content = post.get('text', '')
        
        dna = {
            'structure': {
                'hook': content[:50] if content else '',  # First 50 chars
                'body': content[50:-50] if len(content) > 100 else '',
                'cta': content[-50:] if len(content) > 50 else '',
            },
            'elements': {
                'has_question': '?' in content,
                'has_numbers': any(char.isdigit() for char in content),
                'has_emoji': any(ord(char) > 127 for char in content),
                'has_hashtags': len(post.get('hashtags', [])) > 0,
                'has_media': len(post.get('media', [])) > 0,
            },
            'emotional_tone': self._detect_tone(content),
            'length': len(content),
            'sentence_count': content.count('.') + content.count('!') + content.count('?'),
        }
        
        return dna
    
    def _detect_tone(self, content: str) -> str:
        """Detect emotional tone of content"""
        content_lower = content.lower()
        
        # Simple keyword-based tone detection
        if any(word in content_lower for word in ['love', 'amazing', 'great', 'awesome', '!']):
            return 'positive'
        elif any(word in content_lower for word in ['sad', 'bad', 'hate', 'worst']):
            return 'negative'
        elif '?' in content:
            return 'curious'
        else:
            return 'neutral'
    
    def suggest_content_improvements(self, content: str) -> List[str]:
        """
        Suggest improvements for content
        
        Args:
            content: Draft content
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Length check
        if len(content) < 50:
            suggestions.append("Content is too short. Aim for 100-280 characters for best engagement.")
        elif len(content) > 500:
            suggestions.append("Content is too long. Consider breaking it into a thread.")
        
        # Hook check
        if not content[0].isupper():
            suggestions.append("Start with a capital letter for better readability.")
        
        # Question check
        if '?' not in content:
            suggestions.append("Consider adding a question to encourage replies.")
        
        # Emoji check
        has_emoji = any(ord(char) > 127 for char in content)
        if not has_emoji:
            suggestions.append("Add 1-2 relevant emojis to make content more engaging.")
        
        # Hashtag check
        hashtag_count = content.count('#')
        if hashtag_count == 0:
            suggestions.append("Add 1-2 relevant hashtags for better discoverability.")
        elif hashtag_count > 5:
            suggestions.append("Too many hashtags. Stick to 1-3 most relevant ones.")
        
        return suggestions


if __name__ == "__main__":
    # Test viral detector
    print("Testing ThreadsGPT Viral Detector...")
    
    try:
        detector = ViralDetector()
        print("✓ Viral Detector initialized")
        
        # Test viral score calculation
        test_post = {
            'text': 'This is a test post with great content! 🔥 #viral',
            'engagement': 150,
            'posted_at': datetime.now().isoformat(),
            'media': ['image.jpg'],
            'hashtags': ['#viral']
        }
        
        score = detector.calculate_viral_score(test_post)
        print(f"✓ Viral score: {score}/10")
        
        # Test content suggestions
        suggestions = detector.suggest_content_improvements("short post")
        print(f"✓ Suggestions: {len(suggestions)} recommendations")
        
    except Exception as e:
        print(f"✗ Error: {e}")
