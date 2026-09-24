import requests

URL = "https://efhqbzdnrtifqjqlqseb.supabase.co"
ANON = "sb_publishable_jnycTCgXRMrluvwJORd_4g_B7ojwi9R"

r = requests.post(
    f"{URL}/rest/v1/rpc/delete_shinn_test_keys",
    headers={
        "apikey": ANON,
        "Authorization": f"Bearer {ANON}",
        "Content-Type": "application/json",
    },
    json={},
    timeout=20,
)
print(r.status_code, r.text)
r.raise_for_status()