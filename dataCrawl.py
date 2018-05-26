#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv
import sys,requests,io


'''
    @author：星星
    @content:
    1.爬取某租房网站的租房信息，同时需要获取位置信息，以便接入高德地图API显示位置
    2.爬取细则，遍历爬取每一页网页信息
    3.找到对应租房信息标签
    4.将具体信息获取并保存
    5.先实现单进程，后期完善成多进程，加快爬取速度
'''
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
csv_file = open("data.csv","w",encoding='utf-8')


csv_writer = csv.writer(csv_file, delimiter = ',')
url = "http://wh.58.com/pinpaigongyu/pn/{page}/?minprice={minpri}_{maxpri}" # 爬取的网址
page = 0 # 页码
minpri = 2000 # 最低价格
maxpri = 3000 # 最高价格

# 开始爬取
while True:
    page += 1
    t_url = url.format(page=page,minpri=minpri,maxpri=maxpri)
    print("获取网址：", t_url)
    response = requests.get(t_url) # 解析爬取的网址信息

    html = BeautifulSoup(response.text)
    #print(html)
    house_list = html.select(".list > li")
    # 读取页面数据为空时结束循环
    if not house_list:
        break

    
    for house in house_list:
        house_title = house.select("h2")[0].string#提取出标签下的字符串内容
        house_url = urljoin(url, house.select("a")[0]["href"]) #获取完成的url
        house_info_list = house_title.split() #将房屋地址信息解析
        
        #如果第二列是公寓民则取第一列作为地址, 否则一般都取第二列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]
        
        house_money = house.select(".money")[0].select("b")[0].string #select返回的都是list类型

        #将数据存入csv文件中去
        csv_writer.writerow([house_title,house_location,house_money,house_url])
csv_file.close()
       
