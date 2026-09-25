import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
ANON = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"
BOT = "DÁN_TOKEN_BOT"
GROUP = "-1004446959502"
TZ = ZoneInfo("Asia/Ho_Chi_Minh")

def in_window():
    return 7 <= datetime.now(TZ).hour < 24

def wait_7am():
    now = datetime.now(TZ)
    target = now.replace(hour=7, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return max(60, int((target - now).total_seconds()))

def create_test_keys(count=5):
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/create_shinn_key",
        headers={
            "apikey": ANON,
            "Authorization": f"Bearer {ANON}",
            "Content-Type": "application/json",
        },
        json={
            "p_role": "member",
            "p_days": 7,
            "p_hours": 1,
            "p_count": count,
            "p_label": "FeedBack@ShinnThieuu",
        },
        timeout=20,
    )
    print("create", r.status_code, r.text[:200])
    r.raise_for_status()
    raw = r.json()
    if isinstance(raw, list):
        return "\n".join(raw)
    return str(raw).replace("\\n", "\n").strip('"')

def send(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        json={"chat_id": GROUP, "text": text},
        timeout=20,
    )
    print("telegram", r.status_code, r.text[:200])
    r.raise_for_status()

print("key drop only")
while True:
    try:
        if not in_window():
            w = wait_7am()
            print("ngoai gio, cho", w)
            time.sleep(w)
            continue
        hour = datetime.now(TZ).hour
        footer = (
            "\n\nĐây là key cuối cùng của ngày, nhớ ủng hộ Admin nhé @ShinnThieuu"
            if hour == 22
            else ""
        )
        keys = create_test_keys(5)
        send(
            "SHINN CHEAT — Free test keys\n\n"
            + keys
            + "\n\n"
            "VI\n"
            "• 5 key / lần • hạn 1 giờ • 1 thiết bị\n"
            "• 7h–24h, mỗi 5 giờ\n"
            "• Key dài hạn: @ShinnThieuu\n\n"
            "EN\n"
            "• 5 keys • 1 hour • 1 device\n"
            "• 7:00–24:00 every 5 hours\n"
            "• Long-term: @ShinnThieuu"
            + footer
        )
        print("sent", hour)
    except Exception as e:
        print("loi:", e)
    time.sleep(5 * 60 * 60)