# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 15:34:03 2024

@author: ASUS
"""
import datetime
from datetime import datetime
import pandas as pd
import re
def unify_date(date):
    pattern= re.compile('\d{4}/\d{1,2}/\d{1,2}')
    pattern2= re.compile('\d{1,2}/\d{1,2}')
    pattern3= re.compile(r'\d{1,2}[\u4e00-\u9fff]\d{1,2}[\u4e00-\u9fff]')
    pattern4= re.compile('\d{1,2}-\d{1,2}')
    if pattern.search(date):
        date=pattern.search(date).group()
        today = pd.to_datetime('today')
        current_year = today.year
        
        # 解析日期並組合成完整的日期（默認設置為今年）
        # full_date_str = f"{current_year}/{date}"
        
        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)
        
        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
        
        # date=date.strftime('%Y-%m-%d')
        # date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    elif pattern2.search(date):
        date=pattern2.search(date).group()
        today = pd.to_datetime('today')
        current_year = today.year
        
        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"
        
        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)
        
        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
        
        # date=date.strftime('%Y-%m-%d')
        # date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    elif pattern4.search(date):
        date=pattern4.search(date).group()
        date = date.replace('-','/')
        today = pd.to_datetime('today')
        current_year = today.year
         
        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"
         
         # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)
         
        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
    elif pattern3.search(date):
        date=pattern3.search(date).group()
        date = re.sub(r'[\u4e00-\u9fff]', '/', date)[:-1]
        today = pd.to_datetime('today')
        current_year = today.year
        
        # 解析日期並組合成完整的日期（默認設置為今年）
        date = f"{current_year}/{date}"
        
        # 轉換為 datetime 格式
        date = pd.to_datetime(date, format='%Y/%m/%d').replace(hour=23, minute=59, second=59)
        
        # 如果該日期在今天之前，則設定為明年
        if date < today:
            date = date.replace(year=current_year + 1)
        year = pd.to_datetime('today').year
        date=pd.to_datetime(date)
    return date
        # date=date.strftime('%Y-%m-%d')
        # date=datetime.strptime(date,'%Y-%m-%d %H:%M:%S')

    