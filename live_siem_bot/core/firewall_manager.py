import subprocess 
import os

class FirewallManager:
    def __init__(self):
        # Sinif daxili prefiks təyin edirik
        self.rule_prefix = "SIEM_SOAR_BLOCK_"

    def block_ip(self, ip_address):
        # Localhost və daxili IP-ləri təhlükəsizlik üçün keçirik
        if ip_address in ["127.0.0.1", "Lokal Sistem", "Lokal"]:
            print(f"ℹ️ [FIREWALL] {ip_address} daxili İP olduğu üçün bloklanma bypass edildi.")
            return False

        # self.rule_prefix istifadə edərək qayda adını qururuq
        rule_name = f"{self.rule_prefix}{ip_address}"
        print(f"🧱 [FIREWALL] {ip_address} üçün bloklama qaydası hazırlanır...")

        # Windows Firewall üçün rəsmi PowerShell əmri
        cmd = f'New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -Action Block -RemoteAddress "{ip_address}"'

        try:
            # Əmri sistemdə icra edirik
            subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
            print(f"🛡️ [FIREWALL SUCCESS] {ip_address} rəsmi olaraq Windows Firewall-da bloklandı!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ [FIREWALL ERROR] Qayda icra edilə bilmədi: {e.stderr}")
            return False

    def unblock_ip(self, ip_address):
        """İstənilən vaxt bloklanmış İP-ni açmaq üçün funksiya"""
        rule_name = f"{self.rule_prefix}{ip_address}"
        cmd = f'Remove-NetFirewallRule -DisplayName "{rule_name}"'
        try:
            subprocess.run(["powershell", "-Command", cmd], check=True)
            print(f"🔓 [FIREWALL] {ip_address} bloku uğurla açıldı.")
            return True
        except Exception:
            return False