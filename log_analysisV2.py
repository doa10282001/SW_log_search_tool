import os
import re
import pandas as pd
#使用cmd 下指令 pip install pandas
select_search = input('type in 1 to search interface information , or type in 2 to search log:\n')
#輸入1或2抓取不同的資料

log_dir = input('''
please type in the log dir full path:
ex:C:\\Users\\Ein Lin\\Desktop\\log_dir\\2021-12-23
''')
#輸入資料夾

os.chdir(log_dir)

for i in os.listdir():
#使用迴圈讀取資料夾內所有檔案
    with open(i,'r') as log_obj:
    #依序開啟檔案
        print(i)
        #列出檔名
        information_data = []
        x = []
        #建立空值以利後續延伸寫入
        if select_search == '1':
            for j in log_obj.readlines():
                j = j.strip().split('\n')
                #等於前的i為自定義變數，等於後的i為讀取資料，strip為取消多餘enter，split為把換行分割並把此資料格式轉為list
                information_data.append(j)
                #使用剛剛空字串用append做延伸寫入(不覆寫)
            interface_name = []
            unknown_protocol = []
            input_error = []
            CRC_error = []
            #建立數個後續會用到延伸寫入的空字串
            for k in range(len(information_data)):
            #使用len把資料顯示成長度
                if 'unknown protocol drops' in information_data[k][0]:
                #因上述把資料格式轉成長度，所以如果直接print(k)會變成數字，然後抓出語句有含關鍵字的字串
                    if '0' not in information_data[k][0]:
                    #分類出0以外的資料
                        x.append(k)
                        #用空字串append的資料做成index
                elif 'input errors' in information_data[k][0]:
                    if information_data[k][0].count('0') != 5:
                        #除上述unknown protocol，同時用0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
                        #字串判斷是否為5個0
                        zz = k
                        #起一個新變數zz以避免影嚮原本迴圈k變數
                        while not information_data[zz][0].endswith('output buffers swapped out'):
                        #使用while not 判斷是否為show interface 最後一段字串，如果為是(true)，即跳出迴圈
                            if 'unknown protocol drops' in information_data[zz][0]:
                            #假設unknown protocol drops 為0，但是input errors 字串中有不為0，即會進入此迴圈
                                x.append(zz)
                                break
                            zz = zz + 1
            x = set(x)
            for i in x:
            #如上所述，x為list，可以用for的方式讀取
            #此處開始讀取unknown protocol drops的index
            #開始抓取相關interface
                j = i
                #使用一個變數等於i這個index
                while not (information_data[j][0].startswith('Vlan') or information_data[j][0].startswith('GigabitEthernet') or information_data[j][0].startswith('TenGigabitEthernet') or information_data[j][0].startswith('Loopback') or information_data[j][0].startswith('Port-channel')):
                #interface 中有vlan，和giga所以使用while 用往回找的方式找到對應的interface
                #此處需將所有相關interface都加入否則有機率出錯
                    if 'input errors' in information_data[j][0]:
                    #x 的index數值會由unknown protocol drops開始，
                    #但因為我使用的變數是遞減，所以無關順序，只要match到相關關鍵字即會做出以下事項
                        input_error.append(information_data[j][0].split(' ')[0])
                        #0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored 是一字串
                        #由split(' '), 用空白做為list分開依據
                        #抓出input errors 數值，並添加至input_error 字串列表(list)
                        CRC_error.append(information_data[j][0].split(' ')[3])
                        #抓出crc 數值
                    elif 'unknown protocol' in information_data[j][0]:
                        drops_number = information_data[j][0].split(' ')[0]
                        #抓出unknown protocol drops 數值
                        unknown_protocol.append(int(drops_number))
                    j = j - 1
                interface_name.append(information_data[j][0].split(' ')[0])
                #因使用while not 比對相關interface name，當比對成功(true)時，因not，所以會終止迴圈
                #在跳出迴圈時，j變數為interface name 相關index

            data_format = {
            'interface' : interface_name,
            'input errors' : input_error,
            'CRC errors' : CRC_error,
            'unknown drops' : unknown_protocol
            }
            #做出相關dictionary，以使用pandas做成資料表
            df = pd.DataFrame(data_format)
            if df.empty == False:
                print(df.sort_values(['unknown drops'],ascending=False))
            #使用unknow drops 做排序
            print('\n')
        else:
            search_keyword = input('''
            please type in with statement keyword you want search:
            ex:type in keyword likely vlan mismatch or MACFLAP or anything you want search:
            ''')
            #輸入關鍵字，不分大小寫
            for j in log_obj.readlines():
                if bool(re.search(search_keyword,i,re.IGNORECASE)):
                #找尋logg 關鍵字，不分大小寫
                    print(j.strip())
            print('\n')

'''
以下註解範例
j = 0
for j in range(len(information_data)):
    if information_data[j][0].startswith('Vlan'):
        print(information_data[j][0])

Vlan1 is administratively down, line protocol is down
Vlan2 is up, line protocol is up
Vlan3 is up, line protocol is up
Vlan4 is up, line protocol is up
Vlan10 is up, line protocol is up
Vlan20 is up, line protocol is up
Vlan30 is up, line protocol is up
Vlan31 is up, line protocol is up
Vlan39 is up, line protocol is up
Vlan40 is up, line protocol is up
Vlan41 is up, line protocol is up
Vlan42 is up, line protocol is up
Vlan43 is up, line protocol is up
Vlan45 is up, line protocol is up
Vlan50 is up, line protocol is up
Vlan51 is up, line protocol is up
Vlan93 is up, line protocol is up
Vlan150 is up, line protocol is up
Vlan160 is up, line protocol is up
Vlan170 is up, line protocol is up
Vlan203 is up, line protocol is up
Vlan252 is up, line protocol is up
Vlan253 is up, line protocol is up
Vlan254 is up, line protocol is up
Vlan401 is up, line protocol is up
Vlan666 is up, line protocol is up
Vlan667 is up, line protocol is up
Vlan668 is up, line protocol is up
Vlan669 is up, line protocol is up
Vlan670 is up, line protocol is up
Vlan690 is up, line protocol is up
Vlan777 is up, line protocol is up
Vlan999 is up, line protocol is up
Vlan2536 is up, line protocol is up
'''
