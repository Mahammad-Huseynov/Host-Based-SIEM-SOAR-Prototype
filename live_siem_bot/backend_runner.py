import os
import sys
import time
from core.log_parser import LogParser
from core.threat_intel import ThreatIntel
from core.rules_engine import RulesEngine
from core.firewall_manager import FirewallManager
from core.discord_service import DiscordService

print("============================================================")
print("🛡️   SIEM/SOAR ACTIVE DEFENSE SYSTEM (THRESHOLD v1.2)   🛡️")
print("============================================================")

parser = LogParser()
intel = ThreatIntel()
rules = RulesEngine()
firewall = FirewallManager()
discord = DiscordService()

def central_incident_handler(event_id, username, ip_address):
    print(f"\n🔔 [SIEM] Yeni loq daxil oldu --> ID: {event_id} | User: {username} | IP: {ip_address}")
    
    # 1. Təhlükə Analizi
    severity, threat_description = intel.analyze_event(event_id, username, ip_address)
    
    # 🎯 2. EVENT ID SÜZGƏCİ
    if event_id == 4625:
        # Əgər hadisə yalnız uğursuz girişdirsə, Brute-Force sayğacını və qaydalarını işə sal
        action, policy_details = rules.evaluate_policy(severity, ip_address)
    else:
        # Digər kritik loqlarda (4720, 4726, 1102) sayğacı artırmağa ehtiyac yoxdur.
        # Birbaşa bildiriş rejimini aktiv edirik, Firewall bloklaması gözlənilmir.
        action = "ALERT_ONLY"
        policy_details = f"Direct Notification for Event {event_id}"

    firewall_status = "Gözlənilir (Threshold dolmayıb)"
    
    # 3. Discord-a göndərilmə cəhdi
    try:
        print(f"📡 [DIAGNOSTIC] Discord-a sorğu paketi hazırlanır... [Action: {action}]")
        discord.send_alert(event_id, username, ip_address, severity, threat_description, action, f"Aksiya: {action}")
        print("🔹 [DIAGNOSTIC] Discord funksiyası çağrıldı və keçildi.")
    except Exception as e:
        print(f"❌ [DISCORD CRITICAL] Funksiya daxilində xəta: {e}")

    # 4. AKTİV MÜDAFİƏ
    if action == "BLOCK_IP":
        print(f"🧱 [SOAR] 5 Cəhd dolduğu üçün Firewall işə düşür...")
        firewall_triggered = firewall.block_ip(ip_address)
        if firewall_triggered:
            firewall_status = f"SUCCESS: IP {ip_address} BLOKLANDI!"
        else:
            firewall_status = "Bypassed or Failed"
            
        print(f"\n----------- [SIEM ACTIVE DEFENSE TRIGGERED] -----------")
        print(f"IP {ip_address} rəsmi olaraq divara çırpıldı.")
        print(f"Firewall Status: {firewall_status}")
        print(f"-------------------------------------------------------\n")

if __name__ == "__main__":
    try:
        parser.monitor_logs(central_incident_handler)
    except KeyboardInterrupt:
        print("\n🛑 SIEM sistemi dayandirildi.")
        sys.exit(0)