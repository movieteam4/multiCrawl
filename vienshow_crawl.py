# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 00:49:51 2024

@author: ASUS
"""
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import traceback
import random
import time as Time
# from selenium import webdriver
# import os
import requests as rq
import mysql.connector
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless") #無頭模式
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--window-size=1920,1080")
# from selenium.webdriver.chrome.service import Service
# service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
# driver = webdriver.Chrome(service=service, options=chrome_options)
vien_error='華納威秀 程式完美\n'
vienson_data=''
try:
    title_cns=[]
    title_ens=[]
    release_dates=[]
    cinema_typess=[]
    cinemass=[]
    times=[]
    dates=[]
    genre_list=[]
    descriptions=[]
    directors=[]
    actorss=[]
    l_move_img = []
    youtube=[]
    time_links=[]
    cinema_group=[]
    cinema_list=['MUVIE CINEMAS', 'MUVIE CINEMAS台北松仁威秀(MUCROWN)', '中和環球威秀影城',
        '台中TIGER CITY威秀影城', '台中Tiger City威秀影城(GOLD CLASS)', '台中大遠百威秀影城',
        '台中大魯閣新時代威秀影城', '台北京站威秀影城', '台北信義威秀影城', '台北西門威秀影城', '台南FOCUS 威秀影城',
        '台南南紡威秀影城', '台南南紡威秀影城(GOLD CLASS)', '台南大遠百威秀影城', '新店裕隆城威秀影城',
        '新竹大遠百威秀影城', '新竹大遠百威秀影城(GOLD CLASS)', '新竹巨城威秀影城', '板橋大遠百威秀影城',
        '林口MITSUI OUTLET PARK威秀影城', '林口MITSUI OUTLET PARK威秀影城(Mappa)',
        '桃園桃知道威秀影城', '桃園統領威秀影城', '花蓮新天堂樂園威秀影城', '頭份尚順威秀影城', '高雄大遠百威秀影城',
        '高雄大遠百威秀影城(GOLD CLASS)']
    cinema_types=['4DX / 英', '4DX PRE / 韓', 'ATMOS / 英', 'GC 數位 / 英', 'IMAX / 日',
        'IMAX / 英', 'IMAX 特別場 / 英', 'LIVE / 日', 'LIVE / 韓', 'MAPPA / 英',
        'MUCROWN / 英', 'PRE / 英', 'PRE / 韓', 'PRE 應援場 / 韓', 'TITAN / 英',
        'TITAN LIVE / 韓', 'TITAN PRE / 韓', 'TITAN PRE 應援場 / 韓', '數位', '數位 / 國',
        '數位 / 日', '數位 / 泰', '數位 / 英', '數位 / 韓','4DX / 日','A+ / 日']
    dic={}
    wait_time=random.randint(5,15)
    try:
        for page in range(1,5):
            # driver.get(f'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p={page}')
            # time.sleep(wait_time)
            # r=driver.page_source
            idds=['114.33.18.16:3128','210.61.207.92:80','103.229.126.93:3128','1.160.1.221:8081','36.229.178.32:8080']*2
            sess=rq.Session()
            for idd in idds:
                proxies = {
                    'http': 'http://211.20.17.194:6000',  # HTTP代理
                    'https': f'http://{idd}',  # HTTPS代理
                }
                try:
                    r=sess.post(f'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p={page}',headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'},
                                verify=False,proxies=proxies)
                    print('page accessed')
                    break
                except:
                    continue
            Time.sleep(wait_time)
            soup=bs(r.text,'html.parser')
            # time.sleep(wait_time)
            links=soup.select('ul.movieList>li a')
            for movie_no,link in enumerate(links):
                movie_id=link.get('href')
                # driver.get(f'https://www.vscinemas.com.tw/vsweb/film/{movie_id}')
                # time.sleep(wait_time)
                # r=driver.page_source
                r=sess.post(f'https://www.vscinemas.com.tw/vsweb/film/{movie_id}',headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"},
                           verify=False,proxies=proxies)
                print(f'page {page} movie {movie_no} accessed')
                vien_error+=f'page {page} movie {movie_no} accessed'
                Time.sleep(wait_time)
                r=r.text
                soup=bs(r,'html.parser')
                try:
                    youtube_link=soup.find('iframe').get('src')
                    print('威秀抓到了youtube')
                except AttributeError:
                    youtube_link=''
                    print('威秀沒有抓到youtube')
                time_link=f'https://www.vscinemas.com.tw/vsweb/film/{movie_id}'
                pattern=re.compile(r'\d{4}\s[\u4e00-\u9fa5]\s\d{2}\s[\u4e00-\u9fa5]\s\d{2}\s[\u4e00-\u9fa5]')
                matches=re.findall(r'\d{2}:\d{2}|\d{4}\s[\u4e00-\u9fa5]\s\d{2}\s[\u4e00-\u9fa5]\s\d{2}\s[\u4e00-\u9fa5]|hidden article',r)
                body_list='\n'.join(matches).split('hidden article')[1:]
                combined_pattern = '|'.join(cinema_types)
                combined_pattern2 = '|'.join(cinema_list)
                try:
                    che=r.split('<h4><span class="icon-eyeglasses"></span>放映版本</h4>')[1].split('<p class="versionNote">*請選擇放映版本及影廳，場次將列於下方</p>')[0]
                except IndexError:
                    continue
                description=soup.find(class_='bbsArticle').text
                title_area=soup.find(class_='titleArea').text.split('\n')
                title_cn=title_area[1]
                title_en=title_area[2]
                release_date=title_area[3]
                info_area=soup.find(class_='infoArea').text.split('\n')
                img = soup.select("div.movieMain > figure > img")
                if len(info_area)<5:
                    director=''
                    actor=''
                    gere=''
                else:
                    director=info_area[5]
                    actor=info_area[9]
                    gere=info_area[13]
                soup2=bs(che,'html.parser')
                cinemas=soup2.select('a')
                # dic={}
                order=[]
                # for cinema in cinemas:
                #     print(cinema.text)
                for cinema in cinemas:
                    if "/" in cinema.text or cinema.text =='數位' :
                        order.append(cinema.text)
                        dic[cinema.text]=[]
                        last=cinema.text
                    else:
                        dic[last].append(cinema.text)
                order_index=0
                cinema_index=0
                for b in body_list:
                    if b==' ' or b=='\n':
                        continue
                    try:
                        if len(dic[order[order_index]])==cinema_index:
                            cinema_index=0
                            order_index+=1
                    except IndexError:
                        break
                    for time in b.strip('\n').split('\n'):
                        if len(time)>5:
                            date=time
                        else:
                            if order_index!= len(order) and cinema_index!=len(dic[order[order_index]]):
                                cinema_typess.append(order[order_index])
                                cinemass.append(dic[order[order_index]][cinema_index])
                                title_cns.append(title_cn)
                                title_ens.append(title_en)
                                release_dates.append(release_date)
                                times.append(time)
                                dates.append(date)
                                genre_list.append(gere)
                                descriptions.append(description)
                                directors.append(director)
                                actorss.append(actor)
                                l_move_img.append("https://www.vscinemas.com.tw/vsweb" + img[0].get("src").strip(".."))
                                youtube.append(youtube_link)
                                time_links.append(time_link)
                                cinema_group.append('華納威秀')
                                # print(title_en)
                                # print(release_date)
                                # print(order_index,order[order_index])
                                # print(cinema_index,dic[order[order_index]][cinema_index])
                                # print(time)
                            else:
                                break
                    cinema_index+=1
    except Exception as e:
        print(e)
    finally:
        vienson_data=pd.DataFrame({'中文片名':title_cns,'英文片名':title_ens,'廳位':cinema_typess,
                                '日期':dates,'時刻表':times,'電影院名稱': cinemass,'上映日':release_dates,'類型':genre_list,
                                '導演':directors,'演員':actorss,'簡介':descriptions,'宣傳照':l_move_img,'youtube': youtube,
                                'time_link':time_links,'影城':cinema_group})
        vienson_data=vienson_data.drop_duplicates()
        print(f'華納威秀總共{len(vienson_data)}筆資料')
        if len(vienson_data)==0:
            vienson_data='無'
        # db_config = {
        #     'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
        #     'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
        #     'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
        #     'database': 'xltc236odfo1enc9',  # 要使用的資料庫名稱
        # }
        # connection = mysql.connector.connect(**db_config)

        # if connection.is_connected():
        #     print("成功連接到 MariaDB 資料庫")
        # cursor=connection.cursor()
        # vieshow_html=vienson_data.to_html(classes='table table-striped', index=False).replace(r"'",'’')
        # cursor.execute(f'''insert into vieshow_html (html) values ('{vieshow_html}') ''')
        # connection.commit()
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    vien_error='華納錯誤報告\n'
    for frame in tb:
        vien_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"
    print(vien_error)

