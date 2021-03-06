# !/usr/bin/python
# -*- coding:utf-8 -*-
# author: Pan3a
# time: 2021/8/15
from prettytable import PrettyTable
from time import strftime,localtime,sleep
from base64 import b64encode
from requests import get
import xlwt
import os

class Fofa:
    def __init__(self):
        self.Headers = {
            'Authorization':'eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZ',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        }
        self.URL = 'https://api.fofa.so/v1/search?'
        self.Color()
        self.Banner()
        self.InitVar()

    def Color(self):
        self.RED = "\033[0;31m"
        self.BLUE = "\033[94m"
        self.GREEN = "\033[32m"
        self.ORANGE = "\033[33m"

    def Banner(self):
        self.assets = ['asn_org','banner','city','country','domain','icp','ip','link','os','server','title','port',]
        self.explain = ['组织','banner','城市','国家','域名','ICP备案号','IP地址','链接','系统类型','容器类型','网站标题','端口',]
        table = PrettyTable(['编号','名称','解释'])
        for number,key in enumerate(self.assets):
            table.add_row([number+1,key,self.explain[number]])
        print(table)

    def InitVar(self):
        query = input(self.GREEN + "input query:" + self.GREEN)
        self.query = b64encode(query.encode("UTF-8")).decode('UTF-8')
        try:
            response = get(url=self.URL + "qbase64=" + self.query + "&ps=1&ps=10",timeout=5,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',}).json()
            total = response["data"]["page"]["total"]
            if total % 10 == 0:
                AllPage = total // 10
            else:
                AllPage = total // 10 + 1
            print(self.NowTime() + "total:" + str(total) + "\t" + "AllPage:" + str(AllPage))
        except Exception as e:
            exit(self.RED + str(e) + self.RED)
        self.Headers['Authorization'] = input(self.GREEN + "input auth:" + self.GREEN)
        self.start = int(input(self.GREEN + "input start:" + self.GREEN))
        self.end = int(input(self.GREEN + "input end:" + self.GREEN))
        self.number = input(self.GREEN + "input number:" + self.GREEN).split(',')
        self.tmp = []
        if self.number[-1] == "":
            self.number.pop(-1)
        for n in self.number:
            if int(n) < 1 or int(n) > 12:
                exit(self.RED + "number error" + self.RED)
            else:
                self.tmp.append(self.assets[int(n)-1])
        self.filepath = input(self.GREEN + "input filepath:" + self.GREEN)

    def Request(self):
        try:
            n = 1
            if self.filepath and self.filepath[-3:] == 'xls':
                self.WriteExcel()
            elif self.filepath and self.filepath[-3:] == 'txt':
                file = self.WriteFile()
            for page in range(self.start,self.end+1,1):
                print(self.GREEN +  self.URL + "qbase64=" + self.query + "&pn=" + str(page) + "&ps=10" + self.GREEN)
                response = get(url=self.URL + "qbase64=" + self.query + "&pn=" + str(page) + "&ps=10",headers=self.Headers)
                response.encoding = response.apparent_encoding
                jsondata = response.json()
                if jsondata["message"] != "ok":
                    exit(self.RED + "[-] " + strftime("%H:%M:%S",localtime()) + "\t" + jsondata["message"] + self.RED )
                for i in range(len(jsondata["data"]["assets"])):
                    print(self.BLUE + "-" * 70 + self.BLUE)
                    tmp = []
                    content = ''
                    for data in self.tmp:
                        if type(jsondata["data"]["assets"][i][data]) == type([]) and len(jsondata["data"]["assets"][i][data]) == 1:
                            tmp.append(jsondata["data"]["assets"][i][data][0]["name"])
                        else:
                            tmp.append(str(jsondata["data"]["assets"][i][data]))
                    m = 0
                    for key,value in zip(self.tmp,tmp):
                        print(self.BLUE + self.NowTime() + key + "\t" + value + self.BLUE)
                        content += value + "\t"
                        if self.filepath and self.filepath[-3:] == 'xls':
                            self.sheet.write(n,m,value)
                        m += 1
                    if self.filepath and self.filepath[-3:] == 'txt':
                        file.write(content + "\n")
                    n += 1
                sleep(2)
            if self.filepath and self.filepath[-3:] == 'xls':
                self.excel.save(self.filepath)
            elif self.filepath and self.filepath[-3:] == 'txt':
                file.close()
                
        except Exception as e:
            print(self.RED + str(e) + self.RED)

    def WriteFile(self):
        if os.path.exists(self.filepath):
            choose = input(self.GREEN + self.filepath + "已经存在,是否覆盖Y/N/EXIT:"+ self.GREEN)
            if choose == 'Y' or choose == 'y':
                file = open(self.filepath, 'a',errors="ignore")
                return file
            elif choose == 'N' or choose == 'n':
                self.filepath = input(self.GREEN + "input filepath:" + self.GREEN)
                file = open(self.filepath, 'a',errors="ignore")
                return file
            else:
                self.filepath = None
        else:
            file = open(self.filepath, 'a',errors="ignore")
            return file

    def WriteExcel(self):
        self.excel = xlwt.Workbook()
        self.sheet = self.excel.add_sheet('test',cell_overwrite_ok=True)
        for number,content in enumerate(self.number):
            self.sheet.write(0,number,self.explain[int(content)-1])

    def NowTime(self):
        return self.BLUE +  "[+] " + strftime("%H:%M:%S",localtime()) + "\t" + self.BLUE

if __name__ == '__main__':
    fofa = Fofa()
    fofa.Request()
