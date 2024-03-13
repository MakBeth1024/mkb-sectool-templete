import requests
import os

def check_cdn(target_url):
    command = 'nslookup ' + target_url
    print(command)
    cdn_data = os.popen(command)
    # print(cdn_data)
    points = cdn_data.read().count('.')
    if points > 10:
        return True
    else:
        return False

if __name__ == '__main__':
    # target_url = sys.argv[1]
    target_url = 'www.baidu.com'
    if(check_cdn(target_url)):
        print('There is CDN')
    else:
        print('No CDN')