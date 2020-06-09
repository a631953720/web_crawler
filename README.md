# web_crawler

###動機
1.練習爬蟲程式
2.將爬到的資料經過整理並存成EXCEL

###功能需求
1.目標網站為氣象局網站，顯示未來一周的天氣與溫度範圍
2.爬取各地區的溫度範圍，輸出成EXCEL
3.目標網址:https://www.cwb.gov.tw/V8/C/W/week.html

###使用工具(python)
1.BeautifulSoup
2.webdriver
3.xlsxwriter

###實現過程

####情況1
起初想使用requests去爬取網頁資料，但發現氣象局會用js渲染網頁，因此會有資料無法爬取的情況。
####解決1
為了解決js渲染的部分，使用webdriver去模擬瀏覽器的操作，也能正常渲染網頁，同時可達成其他功能，例如:填寫表單、點及按鈕等一般使用者操作
