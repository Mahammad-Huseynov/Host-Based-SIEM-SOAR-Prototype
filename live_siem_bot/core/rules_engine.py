class RulesEngine:
    def __init__(self):
        # Hər bir IP-nin uğursuz cəhd sayını yadda saxlamaq üçün lüğət
        self.failed_attempts = {}

    def evaluate_policy(self, severity, ip_address):
        # SAFETY FIRST: Özümüzü bloklamamaq üçün Ağ Siyahı (Whitelist) yoxlanışı
        if ip_address in ["127.0.0.1", "Lokal Sistem", "localhost"]:
            print(f"ℹ️ [RULES ENGINE] Lokal hərəkətlilik aşkarlandı ({ip_address}). Təhlükəsizlik üçün BYPASS edildi.")
            return "ALERT_ONLY", "Lokal giriş cəhdi - Təhlükəsizlik məqsədilə bypass edildi."

        # Əgər gələn loq uğursuz girişdirsə
        if severity in ["CRITICAL", "HIGH"]:
            
            # IP siyahıda yoxdursa, ilk cəhdi qeyd et
            if ip_address not in self.failed_attempts:
                self.failed_attempts[ip_address] = 1
            else:
                self.failed_attempts[ip_address] += 1
                
            current_count = self.failed_attempts[ip_address]
            print(f"⚠️ [RULES ENGINE] Uğursuz giriş cəhdi! IP: {ip_address} | Cəhd sayı: {current_count}/5")
            
            # Cəhd sayısı 5-ə çatdıqda bloklama əmrini ver
            if current_count >= 5:
                print(f"🚨 [RULES ENGINE] {ip_address} üçün 5 cəhd limiti doldu! BLOKLAMA QƏRARI VERİLDİ.")
                # Növbəti testlər üçün sayğacı sıfırlayırıq
                self.failed_attempts[ip_address] = 0 
                return "BLOCK_IP", f"Automated defense triggered: 5 failed login attempts exceeded from volatile IP: {ip_address}"
            
            # 5-ə çatmayıbsa, sadəcə xəbərdarlıq et və gözlə
            return "ALERT_ONLY", f"Failed attempt logged ({current_count}/5). Waiting for threshold."
            
        return "ALERT_ONLY", "Log analyzed. Severity does not warrant action."