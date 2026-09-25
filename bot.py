import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
# ============================================================
# SUPABASE
# ============================================================
SUPABASE_URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
# Publishable / Anon key
SUPABASE_ANON_KEY = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"
# Nếu bạn có Service Role / Server Key:
# KHÔNG ghi trực tiếp vào code.
# Thêm vào GitHub Secrets với tên SUPABASE_SERVICE_KEY.
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
# ============================================================
# TELEGRAM
# ============================================================
# Thêm BOT_TOKEN vào:
# GitHub -> Settings -> Secrets and variables -> Actions
BOT_TOKEN = os.getenv("BOT_TOKEN")
# ID nhóm Telegram
GROUP_CHAT_ID = "-1004446959502"
# ============================================================
# TIMEZONE
# ============================================================
TZ = ZoneInfo("Asia/Ho_Chi_Minh")
# ============================================================
# GIỜ PHÁT KEY
# ============================================================
DROP_HOURS = [7, 12, 17, 22]
# ============================================================
# LABEL KEY
# ============================================================
LABEL = "FeedBack @ShinnThieuu"
# ============================================================
# KIỂM TRA CONFIG
# ============================================================
if not BOT_TOKEN:
    raise RuntimeError(
        "Thiếu BOT_TOKEN. "
        "Hãy thêm BOT_TOKEN vào GitHub Secrets."
    )
# ============================================================
# CHỌN KEY SUPABASE
# ============================================================
# Nếu có SUPABASE_SERVICE_KEY thì ưu tiên dùng.
# Nếu chưa có thì dùng publishable/anon key.
SUPABASE_KEY = (
    SUPABASE_SERVICE_KEY
    if SUPABASE_SERVICE_KEY
    else SUPABASE_ANON_KEY
)
# ============================================================
# TẠO KEY
# ============================================================
def create_keys():
    url = (
        f"{SUPABASE_URL}"
        "/rest/v1/rpc/create_shinn_key"
    )
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "p_role": "Member",
        "p_count": 5,
        "p_hours": 1,
        "p_label": LABEL,
    }
    print("[INFO] Đang gọi Supabase...")
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )
    print(
        f"[INFO] Supabase HTTP: "
        f"{response.status_code}"
    )
    response.raise_for_status()
    data = response.json()
    print("[INFO] Supabase response:", data)
    # Trường hợp RPC trả về danh sách key
    if isinstance(data, list):
        if not data:
            raise RuntimeError(
                "Supabase trả về danh sách key rỗng."
            )
        return "\n".join(
            f"`{str(key)}`"
            for key in data
        )
    # Trường hợp RPC trả về một giá trị
    return f"`{str(data).replace(chr(34), '')}`"
# ============================================================
# GỬI TELEGRAM
# ============================================================
def send_message(message):
    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )
    payload = {
        "chat_id": GROUP_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    print("[INFO] Đang gửi Telegram...")
    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )
    print(
        f"[INFO] Telegram HTTP: "
        f"{response.status_code}"
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(
            f"Telegram API lỗi: {result}"
        )
    print("[SUCCESS] Telegram đã nhận tin nhắn.")
    return result
# ============================================================
# TẠO NỘI DUNG TIN NHẮN
# ============================================================
def build_message(keys):
    return f"""🎁 *SHINN CHEAT TEST KEYS*
{keys}
🇻🇳 *KEY TEST*
• 5 key miễn phí
• Hiệu lực: 1 giờ
• 1 thiết bị / key
• Owner: FeedBack @ShinnThieuu
🇺🇸 *TEST KEYS*
• 5 free keys
• Valid for 1 hour
• 1 device per key
• Owner: FeedBack @ShinnThieuu
"""
# ============================================================
# MAIN
# ============================================================
def main():
    now = datetime.now(TZ)
    print("=" * 50)
    print(
        "[INFO] Thời gian Việt Nam:",
        now.strftime("%Y-%m-%d %H:%M:%S"),
    )
    print(
        "[INFO] Các giờ phát key:",
        DROP_HOURS,
    )
    print("=" * 50)
    # --------------------------------------------------------
    # KIỂM TRA GIỜ
    # --------------------------------------------------------
    if now.hour not in DROP_HOURS:
        print(
            "[INFO] Chưa đến giờ phát key."
        )
        return
    # --------------------------------------------------------
    # TẠO KEY
    # --------------------------------------------------------
    print("[INFO] Bắt đầu tạo key...")
    keys = create_keys()
    print("[SUCCESS] Tạo key thành công.")
    # --------------------------------------------------------
    # TẠO MESSAGE
    # --------------------------------------------------------
    message = build_message(keys)
    # --------------------------------------------------------
    # GỬI TELEGRAM
    # --------------------------------------------------------
    send_message(message)
    print("=" * 50)
    print("[SUCCESS] HOÀN TẤT")
    print("=" * 50)
# ============================================================
# START
# ============================================================
if __name__ == "__main__":
    main()

GitHub Secrets cần tạo

Trong repo → Settings → Secrets and variables → Actions, tạo:

BOT_TOKEN

Giá trị là token bot Telegram mới của bạn.

Nếu Supabase RPC create_shinn_key yêu cầu quyền server thì thêm:

SUPABASE_SERVICE_KEY

với giá trị service-role/server key của Supabase.

Không đưa service key vào file Python hoặc commit lên GitHub.

Lưu ý thêm: code này chỉ chạy khi GitHub Actions thực sự khởi chạy vào các mốc giờ đó. Nếu workflow của bạn hiện tại đang dùng cron, mình cần sửa file .github/workflows/*.yml nữa để nó tự chạy đúng 07:00, 12:00, 17:00 và 22:00 giờ Việt Nam.