import os
import requests
from datetime import datetime, timezone

SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SERVICE_ROLE_KEY:
    raise Exception("Missing SUPABASE_SERVICE_KEY")

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Thời gian hiện tại UTC
now = datetime.now(timezone.utc).isoformat()

# Chỉ xoá key test đã hết hạn
api = (
    f"{SUPABASE_URL}/rest/v1/keys"
    f"?type=eq.test&expires_at=lt.{now}"
)

r = requests.delete(api, headers=headers)

print("Status:", r.status_code)
print("Response:", r.text)