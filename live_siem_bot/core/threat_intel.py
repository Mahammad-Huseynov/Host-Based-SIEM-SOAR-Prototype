class ThreatIntel:
    def __init__(self):
        # Bütün kritik Windows Event ID-lərinin bazası
        self.rules_database = {
            4625: ("HIGH", "🚨 BRUTE-FORCE ATTACK DETECTED! Port scanning or password cracking suspected."),
            4648: ("HIGH", "🚷 PRIVILEGE ESCALATION SUSPECT! A logon was attempted using explicit credentials."),
            4720: ("MEDIUM", "👤 Account Management: New local user account created."),
            4726: ("CRITICAL", "⚠️ SECURITY BREACH: A local user account was CRITICALLY DELETED from the system!"),
            1102: ("CRITICAL", "💀 ATTACKER DETECTED COVERING TRACKS: Security Audit logs have been cleared!")
        }

    def analyze_event(self, event_id, username, ip_address):
        # Əgər gələn Event ID bizim bazada varsa, məlumatları dinamik çıxar
        if event_id in self.rules_database:
            severity, alert_template = self.rules_database[event_id]
            
            # Mesajın içinə istifadəçi adını dinamik yerləşdiririk
            full_description = f"{alert_template} [Hədəf Profil: `{username}`]"
            return severity, full_description
        
        # Əgər siyahıda yoxdursa, sistemi yormadan sakitcə keç
        return "INFO", f"Normal system activity monitored. (Event ID: {event_id})"