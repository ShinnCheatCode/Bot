import os
import requests
from datetime import datetime, timezone

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not URL or not KEY:
    raise Exception("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

now = datetime.now(timezone.utc).isoformat()

api = f"{URL}/rest/v1/keys?type=eq.test&expires_at=lt.{now}"

r = requests.delete(api, headers=headers)

print(r.status_code)
print(r.text)