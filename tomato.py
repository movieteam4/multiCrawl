# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 11:46:44 2024

@author: ASUS
"""
def get_tomatos(searchMovie,release_year):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    import os
    import requests as rq
    from bs4 import BeautifulSoup as bs
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless") #無頭模式
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--window-size=1920,1080")
    # # driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    # from selenium.webdriver.chrome.service import Service
    # service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = f'https://www.rottentomatoes.com/search?search={searchMovie}'
    sess=rq.Session()
    r=sess.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
    # driver.get(url)
    soup=bs(r.text,'html.parser')
    movie_detail=soup.select_one('search-page-media-row')
    score=movie_detail.get('tomatometerscore')
    year= movie_detail.get('releaseyear')
    if year==release_year:
        return f'{score}%'
    else:
        return ''
    # movie_card = driver.find_element(By.XPATH,'//*[@id="search-results"]/search-page-result[1]/ul/search-page-media-row[1]')
    # title = movie_card.text.split("\n")[2] #電影名稱
    # score = movie_card.text.split("\n")[1] #爛番茄指數
    # if score == "--" and  searchMovie.casefold() in title[:-7].casefold() and title[-6:].casefold() == f"({release_year})":
    #     print("此電影目前沒有爛番茄指數")
    #     return None 
    # elif searchMovie.casefold() in title[:-7].casefold() and title[-6:].casefold() == f"({release_year})":
    #     print(f"{title[:-7]}的爛番茄指數為:{score}")
    #     return score
    # else:
    #     print("搜尋不到此電影")
    #     return None
    # return None
print(get_tomatos('the wild robot','2024'))