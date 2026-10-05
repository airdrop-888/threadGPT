"""
Simple Cookie Loader - No HAR file needed!
Just paste cookies from browser DevTools
"""

import yaml
from pathlib import Path


def load_cookies_from_config():
    """Load cookies from config.yaml"""
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("[ERROR] config.yaml not found!")
        print("\nSteps:")
        print("1. Copy config.example.yaml to config.yaml")
        print("2. Edit config.yaml and paste your cookies")
        print("\nHow to get cookies:")
        print("1. Open threads.com in browser")
        print("2. Press F12")
        print("3. Go to Application tab > Cookies > threads.com")
        print("4. Copy: sessionid, csrftoken, ds_user_id")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        cookies = config.get('cookies', {})
        
        # Validate cookies
        required = ['sessionid', 'csrftoken', 'ds_user_id']
        missing = [c for c in required if not cookies.get(c)]
        
        if missing:
            print(f"[ERROR] Missing cookies: {', '.join(missing)}")
            print("\nEdit config.yaml and add these cookies!")
            return None
        
        # Build session data
        session_data = {
            'cookies': cookies,
            'headers': {
                'x-csrftoken': cookies['csrftoken'],
                'x-ig-app-id': '238260118697367',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        print("[OK] Cookies loaded successfully!")
        print(f"[OK] User: {config.get('account', {}).get('username', 'unknown')}")
        
        return session_data
        
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return None


def main():
    """Test cookie loader"""
    print("="*60)
    print("ThreadsGPT - Simple Cookie Loader")
    print("="*60)
    
    session = load_cookies_from_config()
    
    if session:
        print("\n[SUCCESS] Ready to use ThreadsGPT!")
        print("\nNext steps:")
        print("  python main.py analytics")
        print("  python main.py post \"Your content\" --time 19:00")
    else:
        print("\n[FAILED] Please setup config.yaml first")
        print("\nQuick setup:")
        print("1. Copy config.example.yaml to config.yaml")
        print("2. Open threads.com and press F12")
        print("3. Application tab > Cookies > Copy sessionid, csrftoken")
        print("4. Paste into config.yaml")


if __name__ == "__main__":
    main()
