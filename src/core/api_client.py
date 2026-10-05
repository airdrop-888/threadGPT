"""
ThreadsGPT - Threads API Client
Real implementation using the actual Threads internal API endpoint.

Endpoint confirmed from HAR capture:
  POST https://www.threads.com/api/v1/media/configure_text_only_post/
"""

import requests
import json
import time
import yaml
import uuid
import re
from typing import Dict, List, Optional
from pathlib import Path
from urllib.parse import quote


class ThreadsAPI:
    """Post to Threads using the internal configure_text_only_post endpoint."""

    POST_URL  = "https://www.threads.com/api/v1/media/configure_text_only_post/"
    APP_ID    = "238260118697367"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )

    def __init__(self, config_file: str = "config.yaml"):
        self.config = self._load_config(config_file)
        self.cookies_cfg = self.config.get('cookies', {})
        self._validate_cookies()
        self.session = requests.Session()
        self._setup_session()

    # ------------------------------------------------------------------
    # Init helpers
    # ------------------------------------------------------------------

    def _load_config(self, path: str) -> Dict:
        cfg = Path(path)
        if not cfg.exists():
            raise FileNotFoundError(
                f"Config not found: {path}\n"
                "Copy config.example.yaml -> config.yaml and fill in your cookies."
            )
        with open(cfg, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def _validate_cookies(self):
        required = ['sessionid', 'csrftoken', 'ds_user_id']
        missing  = [k for k in required if not self.cookies_cfg.get(k)]
        if missing:
            raise ValueError(
                f"Missing cookies in config.yaml: {', '.join(missing)}\n"
                "Open threads.com -> F12 -> Application -> Cookies -> copy the values."
            )

    def _setup_session(self):
        c = self.cookies_cfg

        # Set all cookies
        cookie_map = {
            'sessionid':  (c['sessionid'],  '.threads.com'),
            'csrftoken':  (c['csrftoken'],   '.threads.com'),
            'ds_user_id': (c['ds_user_id'],  '.threads.com'),
        }
        for k, (v, domain) in cookie_map.items():
            self.session.cookies.set(k, v, domain=domain)

        # Optional cookies from config
        for opt in ['ig_did', 'mid', 'rur']:
            if c.get(opt):
                self.session.cookies.set(opt, c[opt], domain='.threads.com')

        # Get web_session_id (x-web-session-id) — fetch from home page
        self.web_session_id = self._fetch_web_session_id()

        # Headers (matches exactly what browser sends)
        self.session.headers.update({
            'authority':            'www.threads.com',
            'accept':               '*/*',
            'accept-language':      'en-US,en;q=0.9',
            'content-type':         'application/x-www-form-urlencoded;charset=UTF-8',
            'origin':               'https://www.threads.com',
            'referer':              'https://www.threads.com/',
            'sec-fetch-dest':       'empty',
            'sec-fetch-mode':       'cors',
            'sec-fetch-site':       'same-origin',
            'user-agent':           self.USER_AGENT,
            'x-asbd-id':            '359341',
            'x-bloks-version-id':   'eb91d73a91a524be8e4f4d5e3793a8eada30ccc66f6990edc31e5ddf8c1c3a2c',
            'x-csrftoken':          c['csrftoken'],
            'x-ig-app-id':          self.APP_ID,
            'x-instagram-ajax':     '0',
            'x-web-session-id':     self.web_session_id,
        })

    def _fetch_web_session_id(self) -> str:
        """Fetch web_session_id from the Threads home page."""
        try:
            resp = requests.get(
                'https://www.threads.com/',
                headers={'user-agent': self.USER_AGENT},
                cookies={
                    'sessionid': self.cookies_cfg['sessionid'],
                    'csrftoken': self.cookies_cfg['csrftoken'],
                },
                timeout=10
            )
            # Pattern: "sessionID":"dopyld:8xuxlv:el86v9"
            m = re.search(r'"sessionID"\s*:\s*"([^"]+)"', resp.text)
            if m:
                sid = m.group(1)
                print(f"[OK] web_session_id: {sid}")
                return sid
        except Exception as e:
            print(f"[WARN] Could not fetch web_session_id: {e}")
        return ""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_post(self, text: str,
                    media_paths: Optional[List[str]] = None) -> Dict:
        """
        Create a text-only Threads post.

        Args:
            text:        Post content (plain text)
            media_paths: Not used for text-only posts (future feature)

        Returns:
            {'success': bool, 'post_id': str, 'error': str}
        """
        upload_id        = str(int(time.time() * 1000))
        composer_id      = str(uuid.uuid4())
        self_thread_id   = str(uuid.uuid4())

        text_post_app_info = {
            "community_flair_id":          None,
            "composer_session_id":         composer_id,
            "entry_point":                 "profile_completion_milestone",
            "excluded_inline_media_ids":   "[]",
            "fediverse_composer_enabled":  True,
            "is_genai_invocation_post":    False,
            "is_reply_approval_enabled":   False,
            "is_spoiler_media":            False,
            "link_attachment_url":         None,
            "link_preview_default_render_style": None,
            "quoted_post_id":              None,
            "ranking_info_token":          None,
            "reply_control":               0,
            "self_thread_context_id":      self_thread_id,
            "snippet_attachment":          None,
            "special_effects_enabled_str": None,
            "tag_header":                  None,
            "text_with_entities": {
                "entities": [],
                "text":     text
            }
        }

        # Build form data (URL-encoded, same as browser)
        data = {
            'async_publish':                '',
            'audience':                     'default',
            'barcelona_source_reply_id':    '',
            'caption':                      text,
            'chain_id':                     '',
            'chain_index':                  '',
            'chain_length':                 '',
            'creator_geo_gating_info':      '{"whitelist_country_codes":[]}',
            'cross_share_info':             '',
            'custom_accessibility_caption': '',
            'gen_ai_detection_method':      '',
            'internal_features':            '',
            'is_meta_only_post':            '',
            'is_paid_partnership':          '',
            'is_upload_type_override_allowed': '1',
            'music_params':                 '',
            'publish_mode':                 'text_post',
            'should_include_permalink':     'true',
            'text_post_app_info':           json.dumps(text_post_app_info),
            'upload_id':                    upload_id,
            'web_session_id':               self.web_session_id,
        }

        # jazoest = sum of ASCII codes of web_session_id + "2" prefix
        jazoest = "2" + str(sum(ord(c) for c in self.web_session_id))
        data['jazoest'] = jazoest

        try:
            print(f"[INFO] Posting to Threads...")
            resp = self.session.post(
                self.POST_URL,
                data=data,
                timeout=30
            )

            print(f"[DEBUG] HTTP {resp.status_code}")

            if resp.status_code == 200:
                try:
                    result = resp.json()
                    status = result.get('status', '')
                    if status == 'ok':
                        media = result.get('media', {})
                        post_pk = media.get('pk', 'unknown')
                        print(f"[SUCCESS] Posted! pk={post_pk}")
                        return {'success': True, 'post_id': str(post_pk)}
                    else:
                        msg = result.get('message', str(result)[:200])
                        print(f"[FAILED] API returned: {msg}")
                        return {'success': False, 'error': msg}
                except ValueError:
                    # Sometimes response is not JSON
                    print(f"[FAILED] Non-JSON response: {resp.text[:200]}")
                    return {'success': False, 'error': f"Non-JSON: {resp.text[:200]}"}

            elif resp.status_code == 403:
                return {'success': False, 'error': 'Forbidden (403) - cookies may be expired. Get fresh cookies.'}
            elif resp.status_code == 401:
                return {'success': False, 'error': 'Unauthorized (401) - sessionid invalid.'}
            else:
                return {'success': False, 'error': f"HTTP {resp.status_code}: {resp.text[:200]}"}

        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'No internet connection.'}
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Request timed out (30s).'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def verify_session(self) -> bool:
        """Quick check if session is still valid."""
        try:
            resp = self.session.get(
                'https://www.threads.com/api/v1/users/whoami/',
                timeout=10
            )
            return resp.status_code == 200
        except Exception:
            return False
