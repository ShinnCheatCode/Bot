import os
import requests
from datetime import datetime, timezone

URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]

headers = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

now = datetime.now(timezone.utc).isoformat()

api = (
    f"{URL}/rest/v1/keys"
    f"?type=eq.test&expires_at=lt.{now}"
)

r = requests.delete(api, headers=headers)

print("Status:", r.status_code)
print(r.text)