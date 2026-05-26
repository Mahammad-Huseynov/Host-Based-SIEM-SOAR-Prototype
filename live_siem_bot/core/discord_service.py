import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class DiscordService:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_alert(self, event_id, username, ip_address, severity, threat_description, action, firewall_status):
        if not self.webhook_url:
            print("⚠️ [DISCORD DEBUG] .env faylında DISCORD_WEBHOOK_URL tapılmadı!")
            return

        message_text = (
            f"🛡️ **[SIEM/SOAR ALERT]**\n"
            f"📌 **Hadisə:** {threat_description}\n"
            f"🆔 **Event ID:** `{event_id}`\n"
            f"🌐 **Mənbə İP:** `{ip_address}`\n"
            f"👤 **İstifadəçi:** `{username}`\n"
            f"⚙️ **SOAR Qərarı:** `{action}`\n"
            f"🧱 **Status:** {firewall_status}\n"
            f"----------------------------------------"
        )

        payload = {"content": message_text}

        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload), 
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code in [200, 204]:
                print("✅ [DISCORD SUCCESS] Bildiriş uğurla göndərildi!")
            else:
                print(f"❌ [DISCORD ERROR] Kod: {response.status_code}")
        except Exception as e:
            print(f"❌ [DISCORD CRITICAL] Şəbəkə xətası: {e}")