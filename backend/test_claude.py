"""Test script to verify Claude API connectivity"""
import sys
import os
import warnings

# Suppress SSL warnings for testing
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from anthropic import Anthropic
import httpx

def test_claude_api():
    """Test if Claude API is working"""
    try:
        print("=== Testing Claude API ===")
        print(f"API Key present: {bool(Config.ANTHROPIC_API_KEY)}")
        print(f"API Key (first 15 chars): {Config.ANTHROPIC_API_KEY[:15] if Config.ANTHROPIC_API_KEY else 'None'}...")

        # Create Anthropic client with SSL verification disabled (for testing only)
        print("\n[NOTE] Disabling SSL verification for testing (corporate environment workaround)")
        http_client = httpx.Client(verify=False)
        client = Anthropic(api_key=Config.ANTHROPIC_API_KEY, http_client=http_client)
        print("[OK] Claude client initialized")

        # Try a simple generation (using Claude Haiku 4.5)
        print("\n=== Testing message generation ===")
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'Hello! Claude API test successful!' and nothing else."}
            ]
        )

        result = response.content[0].text
        print(f"[OK] Response: {result}")

        print("\n[SUCCESS] All tests passed! Claude API is working correctly.")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error: {type(e).__name__}")
        print(f"Details: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_claude_api()
    sys.exit(0 if success else 1)
