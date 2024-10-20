# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 00:40:25 2024

@author: ASUS
"""
#12312354544
import threading
import pandas as pd
from flask_mail import Mail, Message
from flask import Flask
import traceback
import io
import mysql.connector
import lxml
import re
import datetime
from datetime import datetime
from werkzeug.utils import secure_filename
import time
def week_ranking(final_data):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    import os
    import traceback
    ranking_error='排行榜 程式完美'
    ranking_data =''
    #排行榜網頁
    front_page_web = "https://boxofficetw.tfai.org.tw/statistic/"
    # Week/100/0/all/False/ReleaseDate/2024-10-04 #周/顯示數量/第幾頁/all/逆排序/主要排序依據/日期
    # 日期
    date = datetime.now().date()
    # 統計方式
    # statistical_method = ["week", "month"]
    try:
            s="week"
            # 建立list
            l_name = []
            l_release_time = []
            l_little_money = []
            l_little_ticket = []
            l_all_money = []
            l_all_ticket = []
            # 寫入要搜尋的url資訊
            url = front_page_web + s + "/100/0/all/False/ReleaseDate/" + str(date)
            # 使用動態抓取,並用隱性等待駛往詹資訊完整抓取資料
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless") #無頭模式
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            from selenium.webdriver.chrome.service import Service
            service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=chrome_options)
            # driver = webdriver.Chrome()
            driver.get(url)
            driver.implicitly_wait(10)
            # 顯性等待最多40秒，每0.8秒尋找一次，於等待時間內尋找特定的字串出现。
            WebDriverWait(driver, 40, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME, "nowrap.ordered")))
            ranking_html = driver.page_source
            ranking_soup = BeautifulSoup(ranking_html,"html.parser")
            f_lists = ranking_soup.select("div.statistic-table-container tbody > tr") #找到排名表格列表位置
            for m_list in f_lists: #依排名表格儲存資料
                f_name = m_list.select("td.left.min-60")[0] # 電影名字
                f_release_time = m_list.select("td.nowrap.ordered")[0] # 上映日
                f_all_money = m_list.select("td.right")[7] # 總累積金額
                f_all_ticket = m_list.select("td.right")[8] # 總票房
                l_name.append(f_name.text)
                l_release_time.append(f_release_time.text)
                l_all_money.append(f_all_money.text)
                l_all_ticket.append(f_all_ticket.text)
                f_little_money = m_list.select("td.right")[1] # 當周金額
                f_little_ticket = m_list.select("td.right")[3] # 當周票房
                l_little_money.append(eval(f_little_money.text.replace(',','')))
                l_little_ticket.append(eval(f_little_ticket.text.replace(',','')))
                print("中文片名 :",f_name.text)
                print("上映日 :",f_release_time.text)
                print("當周金額 :"if s == "week" else "當月金額 :",f_little_money.text)
                print("當周票房數 :"if s == "week" else "當月金額票房數 :",f_little_ticket.text)
                print("總金額 :",f_all_money.text)
                print("總票房 :",f_all_ticket.text)
                print()
            if s == "week": #紀錄當周排行
                ranking_week_data = pd.DataFrame({
                                        "中文片名" : l_name,
                                        "上映日" : l_release_time,
                                        "當周金額" : l_little_money,
                                        "當周票房數" :l_little_money ,
                                        "總金額" : l_all_money,
                                        "總票房" : l_all_ticket,
                                        })
                # ranking_week_data.to_csv("當周排行.csv", encoding="big5")
            # elif s == "month":#紀錄當月排行
            #     ranking_month_data = pd.DataFrame({
            #                             "中文片名" : l_name,
            #                             "上映日" : l_release_time,
            #                             "當周金額"if s == "week" else "當月金額" : l_little_money,
            #                             "當周票房數"if s == "week" else "當月金額票房數" :l_little_money ,
            #                             "總金額" : l_all_money,
            #                             "總票房" : l_all_ticket,
            #                             })
                # ranking_month_data.to_csv("當月排行.csv",encoding="big5")

    finally:
        driver.quit()
    ranking_week_data['中文片名']= ranking_week_data['中文片名'].apply(remove_space)
    final_data = pd.merge(final_data, ranking_week_data[['中文片名', '當周票房數']], on='中文片名', how='left')
    # final_data = final_data[['中文片名',"當周金額","當周票房數","總金額","總票房"]].sort_values(by='當周票房數', ascending=False).head(10)
    return final_data
now_hour=datetime.now().hour
now_minute=datetime.now().minute
if now_minute>=50:
    now_hour+=1
if now_hour%2==0 or now_hour==0:
    app =Flask(__name__)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ian27368885@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zfpqrdqjekvgwpuh'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    db_config = {
        'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
        'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
        'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
        'database': 'xltc236odfo1enc9',
        'charset': 'utf8mb4',
        'connect_timeout':600,  # 連接超時時間
    }
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("成功連接到 MariaDB 資料庫")
    print(pd.__version__)
    print(lxml.__version__)
    cursor=connection.cursor()
    x=''
    x1=''
    y=''
    y1=''
    z=''
    z1=''
    a=''
    a1=''
    b=''
    b1=''
    c=''
    c1=''
    c2='no data'
    c3='no data'
    # 美麗新影城資料
    def miranew():
        global x,x1
        from miranew_crawl import miranew_data,miranew_error
        x= miranew_data
        x1=miranew_error
        print('美麗新城 done')
    # 秀泰資料
    def show_time():
        global y,y1
        from show_time_crawl import show_time_data,show_time_error
        y= show_time_data
        y1=show_time_error
        print('秀泰 done')
    # 大直美麗華資料
    def mira():
        global z,z1
        from mira_movie_crawl import mira_data,mira_error
        z= mira_data
        z1=mira_error
        print('美麗華 done')
    #威秀資料
    def vieshow():
        global a,a1
        from vienshow_crawl import vienson_data,vien_error
        a=vienson_data
        a1=vien_error
        print('威秀 done')
    # 國賓資料
    def amba():
        global b,b1
        from ambassedor import ambassedor_data,anbassedor_error
        b=ambassedor_data
        b1=anbassedor_error
        print('國賓 done')
    # 星光資料
    def shin():
        global c,c1,c2,c3
        from shin_kong import data , shin_error
        c=data
        c1=shin_error
        print('新光 done')
    job1=threading.Thread(target=show_time)
    job2=threading.Thread(target=miranew)
    job3=threading.Thread(target=mira)
    job4=threading.Thread(target=vieshow)
    job5=threading.Thread(target=amba)
    job6=threading.Thread(target=shin)
    if __name__ == "__main__":
        job1.start()
        # job2.start()
        job3.start()
        job4.start()
        job5.start()
        # job6.start()
        job1.join()
        job2.start()
        job2.join()
        job6.start()
        job3.join()
        job4.join()
        job5.join()
        job6.join()
        if type(x) == str:
            print('美麗新城 炸裂!')
        if type(y) == str:
            print('秀泰 炸裂!')
        if type(z) == str:
            print('美麗華 炸裂!')
        # if type(a) == str:
        #     print('威秀 炸裂!')
        if type(b) == str:
            print('國賓 炸裂!')
        if type(c) == str:
            print('新光 炸裂!')
        to_be_concat=[]
        for i in [x,y,z,b,c]:
            if type(i) == str:
                continue
            to_be_concat.append(i)
        def remove_space(x):
            full_width_punctuations = {
            '。': '.',  # 全形句號 -> 半形句號
            '，': ',',  # 全形逗號 -> 半形逗號
            '！': '!',  # 全形驚嘆號 -> 半形驚嘆號
            '？': '?',  # 全形問號 -> 半形問號
            '：': ':',  # 全形冒號 -> 半形冒號
            '；': ';',  # 全形分號 -> 半形分號
            '（': '(',  # 全形左括號 -> 半形左括號
            '）': ')',  # 全形右括號 -> 半形右括號
            '【': '[',  # 全形左中括號 -> 半形左中括號
            '】': ']',  # 全形右中括號 -> 半形右中括號
            '《': '<',  # 全形左尖括號 -> 半形左尖括號
            '》': '>',  # 全形右尖括號 -> 半形右尖括號
            '「': '"',  # 全形左引號 -> 半形引號
            '」': '"',  # 全形右引號 -> 半形引號
            '、': ',',  # 全形頓號 -> 半形逗號
            '_':'',
        }
            x=x.replace(' ','')
            translation_table = str.maketrans(full_width_punctuations)
            x=x.translate(translation_table)
            return x
        def remove_eng(x):
            if '劇場版' in x or '總集篇' in x or '電影版' in x:
                return re.sub(r'[a-zA-Z]','',x)
            return x
        final_data=pd.concat(to_be_concat)
        final_data['中文片名']=final_data['中文片名'].apply(remove_space)
        final_data['中文片名']=final_data['中文片名'].apply(remove_eng)
        if type(a) !=str:
            a['中文片名']=a['中文片名'].apply(remove_space)
            a['中文片名']=a['中文片名'].apply(remove_eng)
            final_data=pd.concat([final_data,a])
            count=len(final_data)
            cinema_to_be_fill=final_data.groupby('電影院名稱').count().index
            columns_to_be_filled=['導演','演員','類型','宣傳照','youtube','time_link']
            for cinema in cinema_to_be_fill:
                to_fill=final_data[final_data['電影院名稱']==cinema]
                ch_names=to_fill.groupby('中文片名').count().index
                for ch_name in ch_names:
                    for col in columns_to_be_filled:
                        final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))]=final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))].fillna(value=to_fill[[col,'中文片名']][to_fill['中文片名']==ch_name].iloc[0][col])
            for cinema in cinema_to_be_fill:
                to_fill=final_data[final_data['電影院名稱']==cinema]
                ch_names=to_fill.groupby('英文片名').count().index
                for ch_name in ch_names:
                    for col in columns_to_be_filled:
                        final_data[col][(final_data[col].isna()) & (final_data['英文片名'].str.contains(ch_name,case=False))]=final_data[col][(final_data[col].isna()) & (final_data['英文片名'].str.contains(ch_name,case=False))].fillna(value=to_fill[[col,'英文片名']][to_fill['英文片名']==ch_name].iloc[0][col])
            final_data=week_ranking(final_data)
            final_data1=final_data.iloc[:len(final_data)//3]
            final_data2=final_data.iloc[len(final_data)//3:(len(final_data)//3)*2]
            final_data3=final_data.iloc[(len(final_data)//3)*2:]
            final_data1=final_data1.to_html(classes='table table-striped', index=False).replace(r"'",'’')
            final_data2=final_data2.to_html(classes='table table-striped', index=False).replace(r"'",'’')
            final_data3=final_data3.to_html(classes='table table-striped', index=False).replace(r"'",'’')
            cursor.execute(f'''insert into vieshow_html (html) values ('{final_data1}') ''')
            connection.commit()
            cursor.execute(f'''insert into vieshow_html2 (html) values ('{final_data2}') ''')
            connection.commit()
            cursor.execute(f'''insert into movies_html (html) values ('{final_data3}') ''')
            connection.commit()
            print('資料輸入完成')
        else:
            print('程式有誤')
        #     a2=a.iloc[:len(a)//2]
        #     a=a.iloc[len(a)//2:]
        #     vieshow_html=a.to_html(classes='table table-striped', index=False).replace(r"'",'’')
        #     vieshow_html2=a2.to_html(classes='table table-striped', index=False).replace(r"'",'’')
        #     for i in range(3):
        #         try:
        #             cursor.execute(f'''insert into vieshow_html (html) values ('{vieshow_html}') ''')
        #             break
        #         except:
        #             time.sleep(10)
        #     connection.commit()
        #     for i in range(3):
        #         try:
        #             cursor.execute(f'''insert into vieshow_html2 (html) values ('{vieshow_html2}') ''')
        #             break
        #         except:
        #             time.sleep(10)
        #     connection.commit()
        # else:
        #     print('威秀 炸裂!')
        # final_data=pd.concat(to_be_concat)
        # count=len(final_data)+len(a)+len(a2)
        # final_data['中文片名']=final_data['中文片名'].apply(remove_space)
        # final_data['中文片名']=final_data['中文片名'].apply(remove_eng)
        # final_data_html=final_data.to_html(classes='table table-striped', index=False).replace(r"'",'’')
        # cursor.execute(f'''insert into movies_html (html) values ('{final_data_html}') ''')
        # connection.commit()
        # print('未整裡資料,輸入完成')
        # cursor.execute('SELECT * FROM movies_html ORDER BY id DESC LIMIT 1')
        # result=cursor.fetchall()
        # res=result[0][1]
        # final_data=pd.read_html(res)[0]
        # # final_data['中文片名']=final_data['中文片名'].apply(remove_space)
        # # cinema_to_be_fill=final_data.groupby('電影院名稱').count().index
        # # columns_to_be_filled=['導演','演員','類型','宣傳照']
        # # for cinema in cinema_to_be_fill:
        # #     to_fill=final_data[final_data['電影院名稱']==cinema]
        # #     ch_names=to_fill.groupby('中文片名').count().index
        # #     for ch_name in ch_names:
        # #         for col in columns_to_be_filled:
        # #             final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))]=final_data[col][(final_data[col].isna()) & (final_data['中文片名'].str.contains(ch_name,case=False))].fillna(value=to_fill[[col,'中文片名']][to_fill['中文片名']==ch_name].iloc[0][col])
        # # from unify_date import unify_date
        # # final_data['日期']=final_data['日期'].apply(unify_date)
        # final_data_html=final_data.to_html(classes='table table-striped', index=False).replace(r"'",'’')
        # cursor.execute(f'''insert into movies_html (html) values ('{final_data_html}') ''')
        # connection.commit()
    with app.app_context():
        mail = Mail(app)
        msg = Message('多工測試報告', sender = 'ian27368885@gmail.com', recipients = ['ian27368885@gmail.com','movierecommendations4@gmail.com'])
        msg.body = f'總共{count}筆資料\n{x1}\n{y1}\n{z1}\n{a1}\n{b1}\n{c1}'
        mail.send(msg)
else:
    print('休息時間')