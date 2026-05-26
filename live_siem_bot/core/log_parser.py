import win32evtlog
import xml.etree.ElementTree as ET
import time

class LogParser:
    def __init__(self):
        self.session = None 
        self.channel = "Security"
        # CANLI SÜZGƏC: Bütün hədəf ID-ləri bura rəsmən əlavə etdik!
        self.query = "*[System[(EventID=4625 or EventID=4648 or EventID=4720 or EventID=4726 or EventID=1102)]]" 
        
    def monitor_logs(self, callback_function):
        print("🛡️ [SIEM LOG PARSER] Geniş spektrli pusku başladı: [4625, 4648, 4720, 4726, 1102] izlənilir...")
        query_flags = 513 
        
        handle = win32evtlog.EvtQuery(Session=self.session, Path=self.channel, Query=self.query, Flags=query_flags)
        events = win32evtlog.EvtNext(handle, 1)
        
        last_processed_record_id = 0
        if events:
            xml_data = win32evtlog.EvtRender(events[0], win32evtlog.EvtRenderEventXml)
            root = ET.fromstring(xml_data)
            ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
            record_id_node = root.find(".//ns:EventRecordID", ns)
            if record_id_node is not None:
                last_processed_record_id = int(record_id_node.text)

        print(f"🚀 [SIEM ACTIVE] Pusqu aktivdir! Son Sistem Record ID: {last_processed_record_id}")

        while True:
            live_handle = win32evtlog.EvtQuery(Session=self.session, Path=self.channel, Query=self.query, Flags=query_flags)
            live_events = win32evtlog.EvtNext(live_handle, 10)
            
            if live_events:
                for event in live_events:
                    try:
                        xml_data = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
                        root = ET.fromstring(xml_data)
                        ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
                        
                        current_record_id = int(root.find(".//ns:EventRecordID", ns).text)
                        
                        if current_record_id > last_processed_record_id:
                            last_processed_record_id = current_record_id 
                            event_id = int(root.find(".//ns:EventID", ns).text)
                            
                            data_nodes = root.findall(".//ns:Data", ns)
                            log_data = {node.get('Name'): node.text for node in data_nodes if node.get('Name') is not None}
                            
                            # İstifadəçi adını loqun növünə görə ağıllı şəkildə tapırıq
                            if event_id in [4720, 4726]:
                                username = log_data.get('TargetUserName', 'Sistem_User')
                                ip_address = "Lokal Sistem"
                            elif event_id == 1102:
                                username = log_data.get('SubjectUserName', 'Admin')
                                ip_address = "Lokal Sistem"
                            else:
                                username = log_data.get('TargetUserName', 'HackerUser')
                                ip_address = log_data.get('IpAddress', '127.0.0.1')

                            if ip_address == "-" or not ip_address:
                                ip_address = "127.0.0.1"

                            # Mərkəzə ötür
                            callback_function(event_id, username, ip_address)
                            
                    except Exception:
                        pass
            
            time.sleep(1)