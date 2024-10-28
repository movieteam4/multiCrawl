# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:34:05 2024

@author: ASUS
"""
from bs4 import BeautifulSoup as bs
import requests
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
import re
import traceback
mira_error='美麗華程式完美跑完'
mira_data=''
try:
    type_and_time={}
    che=[]
    che2=[]
    chinese_name=[]
    eng_name=[]
    versions=[]
    dates_data_list=[]
    time_data_list=[]
    release_dates=[]
    genre=[]
    director=[]
    actor=[]
    description=[]
    data_cinema=[]
    l_move_img = []
    youtube=[]
    time_links=[]
    cinema_group=[]
    sess=requests.Session()
    r=sess.post('https://www.miramarcinemas.tw/timetable',headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    r=r.text
    soups=bs(r,'html.parser').find_all(class_='timetable_list row')
    for soup in soups:
        titles=soup.find_all(class_='title')
        titles_en=soup.find_all(class_='title_en')
        length=soup.find_all(class_='time')
        level=soup.find_all(class_='badge_movie_level')
        movie_date=soup.find_all(class_='booking_date_area')
        movie_time_r=r.split('block booking_date_area')[1:]
        movie_descriptions=soup.find_all(class_='description hide-on-small-only')
        genre_links=soup.select('div.col.m4.s5>a')
        imgs=soup.select('div.col.m4.s5>img')
        for t,te,l,le,md,mt,des,link,img in zip(titles,titles_en,length,level,movie_date,movie_time_r,movie_descriptions,genre_links,imgs):
            # print(t.text)
            # print(te.text)
            # print(l.text)
            # print(le.text)
            # print(des.text.replace(' ',''))
            date_list=md.text.strip('\n').split('\n')
            soup_time=bs(mt,'html.parser')
            movie_times=soup_time.find_all(class_='time_area')
            cinema_type=soup_time.find_all(class_='room')
            response=sess.post('https://www.miramarcinemas.tw/'+link.get('href'))
            time_link='https://www.miramarcinemas.tw/'+link.get('href')
            soup2=bs(response.text,'html.parser')
            try:
                youtube_link=soup2.find('iframe').get('src')
            except AttributeError:
                youtube_link=''
            detail=soup2.find(class_='movie_info_item')
            img_r=sess.get(img.get('src'),headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
            if img_r.status_code == 200:
                filename = secure_filename(f'{te.text}.jpg')
                with open(filename,'wb') as file:
                    file.write(img_r.content)
            # print(detail.text.replace(' ','').replace('\n\n',''))
            detail_list=detail.text.replace(' ','').replace('\n\n','').split('\n')
            new_detail=soup.select('div.col.m6.s12.time_list_right')
            last_type=[]
            change_date=0
            for d in new_detail:
                che.append(d.text)
                d=d.text.split('\n\n\n')
                d[0]=d[0].replace('event_note請選擇日期及廳別場次:','').strip('\n')
                che2.append(d)
                pattern=re.compile(r'\d{2}:\d{2}')
                for dd in d[1:-1]:
                    dd=dd.strip('\n').split('\n')
                    if dd[0] in last_type:
                        last_type=[]
                        change_date+=1
                    for tt in dd:
                        if pattern.match(tt):
                            if '演員CAST' not in detail_list[5]:
                                director.append(detail_list[5])
                            else:
                                director.append(None)
                            try:
                                actor.append(detail_list[7])
                            except IndexError:
                                actor.append(None)
                            time_data_list.append(tt)
                            chinese_name.append(t.text)
                            eng_name.append(te.text)
                            description.append(des.text.replace(' ',''))
                            versions.append(last_type[-1])
                            dates_data_list.append(d[0].split('\n')[change_date])
                            chee=d[0].split('\n')
                            release_dates.append(detail_list[1])
                            genre.append(detail_list[3])
                            data_cinema.append('美麗華影城  Da-Zhi Cinema')
                            l_move_img.append(img.get('src'))
                            youtube.append(youtube_link)
                            time_links.append(time_link)
                            cinema_group.append('美麗華影城')
                        elif tt!='':
                            last_type.append(tt)
                        
                            
                    
                    
        #     for i,i2,i3 in zip(date_list,movie_times,cinema_type):
        #         # if '演員CAST' not in detail_list[5]:
        #         #     director.append(detail_list[5])
        #         # else:
        #         #     director.append(None)
        #         # try:
        #         #     actor.append(detail_list[7])
        #         # except IndexError:
        #         #     actor.append(None)
        #         # data_cinema.append('美麗華影城  Da-Zhi Cinema')
        #         print(i.strip('\n'))
        #         print(i3.text)
        #         print(i2.text.strip('\n'))
        #         timess=i2.text.split('\n')
        #         for tt in timess[1:-1]:
        #             if '演員CAST' not in detail_list[5]:
        #                 director.append(detail_list[5])
        #             else:
        #                 director.append(None)
        #             try:
        #                 actor.append(detail_list[7])
        #             except IndexError:
        #                 actor.append(None)
        #             time_data_list.append(tt)
        #             chinese_name.append(t.text)
        #             eng_name.append(te.text)
        #             description.append(des.text.replace(' ',''))
        #             versions.append(i3.text)
        #             dates_data_list.append(i.strip('\n'))
        #             release_dates.append(detail_list[1])
        #             genre.append(detail_list[3])
        #             data_cinema.append('美麗華影城  Da-Zhi Cinema')
        #         print('-------------------')
        #     print()
    mira_data=pd.DataFrame({'中文片名':chinese_name,'英文片名':eng_name,'廳位':versions,
                                '日期':dates_data_list,'時刻表':time_data_list,'電影院名稱': data_cinema,'上映日':release_dates,'類型':genre,
                                '導演':director,'演員':actor,'簡介':description,'宣傳照':l_move_img,'youtube': youtube,
                                'time_link':time_links,'影城':cinema_group})
    
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    mira_error='美麗華錯誤報告\n'
    for frame in tb:
        mira_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"