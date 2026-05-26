import requests
import os
from config.settings import load_dotenv

class DiscordService:
    def __init__(self):
        # .env faylından webhook linkini mərkəzi olaraq çəkirik
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_alert(self, content: str) -> bool:
        if not self.webhook_url:
            return False
            
        # Discord API-nin qəbul etdiyi rəsmi JSON strukturu
        payload = {
            "content": content
        }
        
        try:
            # Discord uğurlu sorğu zamanı geriyə HTTP 204 status kodu qaytarır
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            return response.status_code == 204
        except requests.RequestException:
            return False