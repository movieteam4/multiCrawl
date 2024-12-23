# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 02:03:16 2024

@author: ASUS
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
# from datetime import datetime
import traceback
anbassedor_error='國賓程式完美'
try:
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}
    url = "https://www.ambassador.com.tw/"

    # 依順序儲存資料的list
    l_move_title = ["英文片名", "中文片名", "上映日", "演員", "簡介", "類型", "電影院名稱", "日期", "廳位", "時刻表", "宣傳照"]
    l_move_Eng = []
    l_move_Chr = []
    l_move_release_date = []
    l_move_actor = []
    l_move_introduction = []
    l_move_genre = []
    l_move_cinema_name = []
    l_move_date = []
    l_move_version = []
    l_move_timetable = []
    l_move_img = []
    youtube=[]
    time_links=[]
    cinema_group=[]
    # s_t = datetime.now()
    # 使用 session 來保持連接
    with requests.Session() as sess:
        # 抓取所有現正熱映
        move_list = 'home/MovieList'
        r1_html = sess.get(url+move_list,headers = headers)
        r1_soup = BeautifulSoup(r1_html.text.split("即將上映")[0],"html.parser") #取得即將上映前的電影資訊
        f_move_names = r1_soup.select("div.poster-info > div.title > h6 > a") #搜尋電影名稱欄位(附連結網址)
        for m_soup in f_move_names:
            m_href = url + m_soup.get("href") #取得當前網站網址
            move_Chr = m_soup.text #取得電影名稱
            # 顯示電影名稱
            # print("中文片名：", move_Chr)
            r2_html = sess.get(m_href, headers = headers) #進入個別電影網址頁面
            r2_soup = BeautifulSoup(r2_html.text,"html.parser") #取得即將上映前的電影資訊
            youtube_link=r2_soup.find('iframe').get('src')
            print('我抓到youtube了')
            dates_html = r2_soup.select("li.has-submenu > ul.menu.scrollbar > li > a") #取得可購票日期
            move_img = r2_soup.select("div.cell.small-3.medium-2.large-2.movie-pic-box > img") #取得電影宣傳照
            move_Eng = r2_soup.select("div.cell.small-12.medium-12.large-12.movie-info-box > h6") #取得英文名稱
            move_rule = r2_soup.select("div.cell.small-12.medium-12.large-12.movie-info-box > p") #取得其他內容
            
            # print("英文片名：", move_Eng[0].text)
            # print("簡介：", move_rule[0].text)
            # print("演員：", move_rule[1].text.split("：")[1])
            # print("類型：", move_rule[2].text.split("：")[1])
            # print("上映日：", move_rule[3].text.split("：")[1])
            # print("宣傳照：", move_img[0].get("src"))
            
            for date_t in dates_html:
                # print(date_t.text)
                r3_html = sess.get(url + date_t.get("href"), headers = headers) #依日期尋找電影資訊
                time_link=url + date_t.get("href")
                r3_soup = BeautifulSoup(r3_html.text,"html.parser") #取得電影時刻表
                cinema_row = r3_soup.select("div.theater-box") # 尋電影欄
                for c_row in cinema_row:
                    cinema_names = c_row.select("h3 > a") # 尋電影院名稱
                    move_types = c_row.select("p.tag-seat") # 尋電影類型
                    move_row = c_row.select("ul.no-bullet.seat-list") # 尋電影類型欄
                    for c_name in cinema_names:
                        # 顯示電影院名稱
                        # print(c_name.text)
                        for type_num,m_row in enumerate(move_row):
                            cinema_times = m_row.select("h6") # 尋電影播放時段
                            # 顯示電影版本
                            # print(move_types[type_num].text.split(f"{move_Chr}")[0])
                            for c_time in cinema_times:
                                # 顯示電影撥放時刻
                                # print(c_time.text.strip(" "),end=" ")
                                l_move_Eng.append(move_Eng[0].text)
                                l_move_Chr.append(move_Chr)
                                l_move_release_date.append(move_rule[3].text.split("：")[1])
                                l_move_actor.append(move_rule[1].text.split("：")[1])
                                l_move_introduction.append(move_rule[0].text)
                                l_move_genre.append(move_rule[2].text.split("：")[1])
                                l_move_cinema_name.append(c_name.text)
                                l_move_date.append(date_t.text)
                                l_move_version.append(move_types[type_num].text.split(f"{move_Chr}")[0])
                                l_move_timetable.append(c_time.text.strip(" "))  
                                l_move_img.append(move_img[0].get("src"))
                                youtube.append(youtube_link)
                                time_links.append(time_link)
                                cinema_group.append('國賓影城')
            #                 print()
            #             print()
            # print("---------------------------------------------------------------------------------")
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    anbassedor_error='國賓錯誤報告\n'
    for frame in tb:
        anbassedor_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"            
finally:
    ambassedor_data = pd.DataFrame({ l_move_title[0] : l_move_Eng,
                                    l_move_title[1] : l_move_Chr,
                                    l_move_title[2] : l_move_release_date,
                                    l_move_title[3] : l_move_actor,
                                    l_move_title[4] : l_move_introduction,
                                    l_move_title[5] : l_move_genre,
                                    l_move_title[6] : l_move_cinema_name,
                                    l_move_title[7] : l_move_date,
                                    l_move_title[8] : l_move_version,
                                    l_move_title[9] : l_move_timetable,
                                    l_move_title[10] : l_move_img,
                                    'youtube': youtube,
                                    'time_link':time_links,
                                    '影城':cinema_group})
# ambassedor_data.to_csv("國賓電影清單.csv",encoding="big5",index=False,errors="replace")

# e_t = datetime.now()
# print(e_t-s_t)