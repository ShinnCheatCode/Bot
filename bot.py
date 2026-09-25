import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
ANON = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"
BOT = os.environ["8841904683:AAFDQmAuhcoWv26p_5TC_tQV9zhdaXbNoCk"]
GROUP = os.environ.get("GROUP_CHAT_ID", "-1004446959502")
TZ = ZoneInfo("Asia/Ho_Chi_Minh")


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
        timeout=30,
    )
    print("create", r.status_code, r.text[:300])
    r.raise_for_status()
    raw = r.json()
    if isinstance(raw, list):
        return "\n".join(str(x) for x in raw)
    return str(raw).replace("\\n", "\n").strip().strip('"')


def send(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        json={"chat_id": GROUP, "text": text, "disable_web_page_preview": True},
        timeout=30,
    )
    print("telegram", r.status_code, r.text[:300])
    r.raise_for_status()


hour = datetime.now(TZ).hour
if hour < 7:
    print("outside window", hour)
    raise SystemExit(0)

footer = ""
if hour == 22:
    footer = "\n\nĐây là key cuối cùng của ngày, nhớ ủng hộ Admin nhé @ShinnThieuu"

keys = create_test_keys(5)
send(
    "SHINN CHEAT — Free test keys\n\n"
    + keys
    + "\n\n"
    "VI\n"
    "• 5 key / lần • hạn 1 giờ • 1 thiết bị\n"
    "• 7h sáng – 12h đêm, mỗi 5 giờ\n"
    "• Thêm thành viên để nhận key free\n"
    "• Key dài hạn / tạo key: @ShinnThieuu\n\n"
    "EN\n"
    "• 5 keys per drop • 1 hour • 1 device\n"
    "• 7:00–24:00, every 5 hours\n"
    "• Add members to get free keys\n"
    "• Long-term / create keys: @ShinnThieuu"
    + footer
)
print("sent", hour)