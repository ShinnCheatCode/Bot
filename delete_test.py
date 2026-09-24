import os
import requests

SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
ANON = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"
BOT = os.environ["TELEGRAM_BOT_TOKEN"]
GROUP = os.environ.get("GROUP_CHAT_ID", "-1004446959502")

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
            "p_label": "group-free",
        },
        timeout=20,
    )
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
    r.raise_for_status()

keys = create_test_keys(5)
send(
    "SHINN CHEAT — Free test keys\n\n"
    + keys
    + "\n\n"
    "VI\n"
    "• 5 key / lần • hạn 1 giờ • 1 thiết bị\n"
    "• Cập nhật mỗi 5 giờ\n"
    "• Thêm thành viên để nhận key free\n"
    "• Key dài hạn / tạo key: @ShinnThieuu\n\n"
    "EN\n"
    "• 5 keys per drop • 1 hour • 1 device\n"
    "• Posted every 5 hours\n"
    "• Add members to get free keys\n"
    "• Long-term / create keys: @ShinnThieuu"
)
print("sent")