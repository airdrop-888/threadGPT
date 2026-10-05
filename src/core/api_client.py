"""
ThreadsGPT - Threads API Client
Real implementation using cookies from config.yaml
"""

import requests
import json
import time
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class ThreadsAPI:
    """Client for posting to Threads.net using browser cookies"""

    # Threads GraphQL endpoint
    BASE_URL = "https://www.threads.net/api/graphql"
    APP_ID   = "238260118697367"

    def __init__(self, config_file: str = "config.yaml"):
        self.config = self._load_config(config_file)
        self.cookies = self.config.get('cookies', {})
        self._validate_cookies()

        self.session = requests.Session()
        self._setup_session()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _load_config(self, path: str) -> Dict:
        cfg_path = Path(path)
        if not cfg_path.exists():
            raise FileNotFoundError(
                f"Config not found: {path}\n"
                "Copy config.example.yaml -> config.yaml and fill in your cookies."
            )
        with open(cfg_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def _validate_cookies(self):
        required = ['sessionid', 'csrftoken', 'ds_user_id']
        missing = [k for k in required if not self.cookies.get(k)]
        if missing:
            raise ValueError(
                f"Missing cookies in config.yaml: {', '.join(missing)}\n"
                "Open threads.com -> F12 -> Application -> Cookies and copy the values."
            )

    def _setup_session(self):
        """Build session with proper headers and cookies"""
        cookies = self.cookies

        # Set cookies on session
        self.session.cookies.set('sessionid',  cookies['sessionid'],  domain='.threads.net')
        self.session.cookies.set('csrftoken',  cookies['csrftoken'],  domain='.threads.net')
        self.session.cookies.set('ds_user_id', cookies['ds_user_id'], domain='.threads.net')
        if cookies.get('mid'):
            self.session.cookies.set('mid', cookies['mid'], domain='.threads.net')

        # Headers that Threads expects
        self.session.headers.update({
            'authority':        'www.threads.net',
            'accept':           '*/*',
            'accept-language':  'en-US,en;q=0.9',
            'content-type':     'application/x-www-form-urlencoded',
            'origin':           'https://www.threads.net',
            'referer':          'https://www.threads.net/',
            'sec-fetch-dest':   'empty',
            'sec-fetch-mode':   'cors',
            'sec-fetch-site':   'same-origin',
            'user-agent':       (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/127.0.0.0 Safari/537.36'
            ),
            'x-csrftoken':      cookies['csrftoken'],
            'x-ig-app-id':      self.APP_ID,
            'x-asbd-id':        '129477',
            'x-fb-lsd':         self._get_lsd_token(),
        })

    def _get_lsd_token(self) -> str:
        """
        Fetch the lsd token required by Threads' anti-CSRF system.
        It is embedded in the HTML of the home page.
        """
        try:
            resp = requests.get(
                'https://www.threads.net/',
                headers={'user-agent': 'Mozilla/5.0'},
                cookies={
                    'sessionid': self.cookies['sessionid'],
                    'csrftoken': self.cookies['csrftoken'],
                },
                timeout=10
            )
            # Token is in: "LSD",[],{"token":"XXXXXXXXX"}
            import re
            match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', resp.text)
            if match:
                return match.group(1)
        except Exception:
            pass
        return 'AVqbxe3J_LA'  # fallback token

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_post(self, text: str, media_paths: Optional[List[str]] = None) -> Dict:
        """
        Create a new Threads post.

        Args:
            text:        Post content
            media_paths: Optional list of local image/video paths

        Returns:
            Dict with keys: success (bool), post_id (str), error (str)
        """
        try:
            user_id = self.cookies['ds_user_id']

            # Build the payload Threads expects
            payload = {
                'variables': json.dumps({
                    'text': text,
                    'reply_control': 0,   # 0 = everyone can reply
                }),
                'doc_id': '7802822539985017',   # create_text_post mutation
                'lsd':    self.session.headers.get('x-fb-lsd', ''),
            }

            resp = self.session.post(
                self.BASE_URL,
                data=payload,
                timeout=30
            )

            print(f"[DEBUG] Status: {resp.status_code}")
            if resp.status_code != 200:
                return {
                    'success': False,
                    'error': f"HTTP {resp.status_code}: {resp.text[:200]}"
                }

            data = resp.json()
            print(f"[DEBUG] Response: {json.dumps(data, indent=2)[:300]}")

            # Check for errors inside the GraphQL response
            if 'errors' in data:
                return {
                    'success': False,
                    'error': str(data['errors'])
                }

            return {
                'success': True,
                'post_id': user_id,
                'data': data
            }

        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'No internet connection'}
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Request timed out'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def verify_session(self) -> bool:
        """Check if the current session is valid"""
        try:
            resp = self.session.get(
                'https://www.threads.net/api/v1/users/whoami/',
                timeout=10
            )
            return resp.status_code == 200
        except Exception:
            return False
