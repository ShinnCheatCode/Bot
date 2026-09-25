import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
ANON_KEY = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"

BOT_TOKEN = os.environ["8841904683:AAFDQmAuhcoWv26p_5TC_tQV9zhdaXbNoCk"]
GROUP_CHAT_ID = "-1004446959502"

TZ = ZoneInfo("Asia/Ho_Chi_Minh")
DROP_HOURS = [7, 12, 17, 22]

LABEL = "FeedBack @ShinnThieuu"


def create_keys():
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/create_shinn_key",
        headers={
            "apikey": ANON_KEY,
            "Authorization": f"Bearer {ANON_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "p_role": "Member",
            "p_count": 5,
            "p_hours": 1,
            "p_label": LABEL
        },
        timeout=30,
    )

    r.raise_for_status()
    data = r.json()

    if isinstance(data, list):
        return "\n".join(f"`{k}`" for k in data)

    return f"`{str(data).replace(chr(34), '')}`"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": GROUP_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        },
        timeout=30,
    ).raise_for_status()


def main():
    now = datetime.now(TZ)

    if now.hour not in DROP_HOURS or now.minute != 0:
        return

    keys = create_keys()

    text = f"""🎁 *SHINN CHEAT TEST KEYS*

{keys}

🇻🇳 **KEY TEST**
• 5 key miễn phí
• Hiệu lực: 1 giờ
• 1 thiết bị / key
• Owner: FeedBack @ShinnThieuu

🇺🇸 **TEST KEYS**
• 5 free keys
• Valid for 1 hour
• 1 device per key
• Owner: FeedBack @ShinnThieuu
"""

    send(text)


if __name__ == "__main__":
    main()