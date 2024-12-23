# 抓取秀泰電影名稱
# 圖片、上映時間、演員、導演、劇情、類型
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import traceback
import os
import time
show_time_error='秀泰 程式完美'
show_time_data =''
try:
    # 秀泰網站
    url = "https://www.showtimes.com.tw/programs"

    # 搜尋特定字串
    wait_str_01 = "客服信箱"

    # 依順序儲存資料的list
    l_move_title = ["英文片名", "中文片名", "上映日", "演員", "導演", "簡介", "類型", "電影院名稱", "日期", "廳位", "時刻表"]
    l_move_Engname = []
    l_move_Chrname = []
    l_move_release_date = []
    l_move_actor = []
    l_move_director = []
    l_move_introduction = []
    l_move_genre = []
    l_move_cinema_name = []
    l_move_date = []
    l_move_hall = []
    l_move_timetable = []
    time_links=[]
    def set_text():
        # 讀取出內容資訊
        move_soup1 = driver.page_source
        soup1 = BeautifulSoup(move_soup1,"html.parser")
        # 找中英文名以及各式資訊
        move_Chr_name = soup1.select("div.sc-jnOGJG.mQyVn") #找中文名
        move_Eng_name = soup1.select("div.sc-dZoequ.gdfOVW") #找英文名
        # 0級別,1片長,2上映日,3上映影城,4類型,5演員,6導演,7簡介
        find_rule = soup1.select("div.sc-cmaqmh.bIIkFl") #其他電影資訊
        find_date = soup1.select("div.sc-iMTnTL.hlfQuj") #找日期
        find_hall = soup1.select("div.sc-gFVvzn.eECWsO") #廳位
        find_timetable = soup1.select("button.sc-iGgWBj.ffxCYX.btn.sc-bBeLUv.enqmAq.mr-2.mb-2.py-2.btn-outline-primary") #找時刻表
        # 依電影廳數*時刻表數量儲存資訊
        for hall_num in range(len(find_hall)):
            for tle_num in range(len(find_timetable)):
                l_move_Engname.append(move_Eng_name[0].text)
                l_move_Chrname.append(move_Chr_name[0].text)
                l_move_release_date.append(find_rule[2].text)
                l_move_actor.append(find_rule[5].text)
                l_move_director.append(find_rule[6].text)
                l_move_introduction.append(find_rule[7].text)
                l_move_genre.append(find_rule[4].text)
                l_move_cinema_name.append(find_hall[hall_num].text.split("秀泰")[0] + "秀泰")
                l_move_date.append(find_date[0].text)
                l_move_hall.append(find_hall[hall_num].text.split("廳")[0] + "廳")
                l_move_timetable.append(re.findall("\\d{2}:\\d{2}",find_timetable[tle_num].text)[0])
                time_links.append(time_link)
    
    # 使用動態抓取,並用隱性等待駛往詹資訊完整抓取資料
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    # driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)

    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)
    # 顯性等待最多10秒，每0.5秒尋找一次，等待頁面出現"即將上映"。
    WebDriverWait(driver, 40, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME,"sc-bbSZdi.dLAzVo")))
    # 讀取出內容資訊，並記錄即將上映前的數量依數量抓取電影數
    ontime_move_html = driver.page_source.split("即將上映")[0]
    ontime_move_soup = BeautifulSoup(ontime_move_html,"html.parser")
    moves_cut = ontime_move_soup.select("div.sc-uVWWZ.jGcugE")
    # 尋找CLASS點擊進入電影名稱內網站
    move_names = driver.find_elements(By.CLASS_NAME,'sc-uVWWZ.jGcugE')
    
    # 依序進入內容選取資訊
    for move_num in range(len(moves_cut)):
        move_names[move_num].click() #點擊電影照
        time.sleep(3)
        # 顯性等待最多10秒，每0.5秒尋找一次，等待頁面出現"即將上映"。
        # WebDriverWait(driver, 40, 0.8).until(EC.presence_of_element_located((By.CLASS_NAME,"sc-krNlru.kYzChH")))
        # 讀取出內容資訊，並記錄即將上映前的數量依數量抓取電影數
        Cinema_html = driver.page_source
        Cinema_soup = BeautifulSoup(Cinema_html,"html.parser")
        time_link=driver.current_url
        Cinema_num = Cinema_soup.select("button.sc-iGgWBj.ffxCYX.btn.sc-jMakVo.jDptCM.mr-2.mb-2.py-2.px-4.btn-outline-primary")
        if len(Cinema_num) > 0: 
            # 搜尋各個電影院並點擊
            Cinema_names = driver.find_elements(By.CLASS_NAME, "sc-iGgWBj.ffxCYX.btn.sc-jMakVo.jDptCM.mr-2.mb-2.py-2.px-4.btn-outline-primary")
            for num_c in range(len(Cinema_names)):
                Cinema_names[num_c].click()
                set_text()
                # 確認日期數量大於1，再搜尋日期的按妞
                dateTime_soup = driver.page_source
                soup2 = BeautifulSoup(dateTime_soup,"html.parser")
                dateTime = soup2.select("div.sc-iMTnTL.kZfgzt")
                if len(dateTime) > 0:
                    # 搜尋各電影院的日期時刻表資訊
                    date_time = driver.find_elements(By.CLASS_NAME, "sc-iMTnTL.kZfgzt")
                    for num_t in range(len(date_time)):
                        date_time[num_t].click()
                        set_text()
        else:
            set_text()
            # 確認日期數量大於1，再搜尋日期的按妞
            dateTime = Cinema_soup.select("div.sc-iMTnTL.kZfgzt")
            if len(dateTime) > 0:
                # 搜尋各電影院的日期時刻表資訊
                date_time = driver.find_elements(By.CLASS_NAME, "sc-iMTnTL.kZfgzt")
                for num_t in range(len(date_time)):
                    date_time[num_t].click()
                    set_text()
        driver.back()
        move_names = driver.find_elements(By.CLASS_NAME,'sc-uVWWZ.jGcugE')
            
    
    driver.quit()
    
    show_time_data = pd.DataFrame({l_move_title[0] : l_move_Engname,
                        l_move_title[1] : l_move_Chrname,
                        l_move_title[2] : l_move_release_date,
                        l_move_title[3] : l_move_actor,
                        l_move_title[4] : l_move_director,
                        l_move_title[5] : l_move_introduction,
                        l_move_title[6] : l_move_genre,
                        l_move_title[7] : l_move_cinema_name,
                        l_move_title[8] : l_move_date,
                        l_move_title[9] : l_move_hall,
                        l_move_title[10] : l_move_timetable,
                        'time_link':time_links
                        }) 
    # data.to_csv("電影清單.csv",encoding="big5",index=False,errors="replace")
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    show_time_error='秀泰錯誤報告\n'
    for frame in tb:
        show_time_error+=f"文件：{frame.filename}, 行號：{frame.lineno}, 錯誤類型：{e.__class__.__name__}, 錯誤信息：{e}\n"     
    print(show_time_error)