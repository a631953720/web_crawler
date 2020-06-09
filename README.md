# web_crawler

### 動機
1.練習爬蟲程式<br>
2.將爬到的資料經過整理並存成EXCEL<br>

### 功能需求
1.目標網站為氣象局網站，顯示未來一周的天氣與溫度範圍<br>
2.爬取各地區的溫度範圍，輸出成EXCEL<br>
3.目標網址:https://www.cwb.gov.tw/V8/C/W/week.html <br>

### 使用工具(python)
1.BeautifulSoup<br>
2.selenium(webdriver)<br>
3.xlsxwriter<br>

### 實現過程

#### 情況1
起初想使用requests去爬取網頁資料，但發現氣象局會用js渲染網頁，因此會有資料無法爬取的情況。
#### 方法1
為了解決js渲染的部分，使用webdriver去模擬瀏覽器的操作，也能正常渲染網頁，同時可達成其他功能，例如:填寫表單、點擊按鈕等一般使用者操作。<br>
使用前除了引入library，還需要下載相對應的webdriver用以啟用瀏覽器(並非一般使用的瀏覽器，而是測試用)。<br>

#### 情況2
觀察氣象局網頁，一個大表格就可包含全縣市的溫度資料，每個縣市獨立一個tbody，內含兩個tr分別是早晚的天氣狀況，每一個th裡面放的是縣市名稱，td放的是溫度區間、天氣狀況。

#### 方法2
首先是取得單一一個城市的表格，只需要針對tbody的tag名稱產生陣列(列表)即可。<br>
取得城市名稱，再成功取得單一一個tbody就代表成功取得一個縣市一周的所有天氣資料，最後只需要取得唯一的一個th就可以撈到縣市名稱。<br>
取得溫度的部分，透過前面的tbody陣列，一一撈取溫度資料，若不設條件，一共會撈到7天14筆的溫度區間，由於資料個數固定，因此加入簡易判斷，當撈到第7個資料時會重置暫存陣列，並重新生成新的陣列，同時會在此加入地區名稱來作判別(如下範例，是個二維陣列)。<br>
取得日期則是透過thead內的tr標籤取得。

```
期望溫度資料陣列:[['地區','26-34','25-35']['地區','26-34','25-35']]
```
#### 情況3
希望不要是溫度區間，而是分開成為最高、最低溫度數值，網站內的字串為'26 - 34'。

#### 方法3
透過python的字串處理，去除特殊字元，再透過'-'字元座分割，即可獨立出兩個數字，並轉成整數型態，並依序放入，除了陣列中的第一個元素為地區，後面接為成雙的資料(地區、低溫、高溫、低溫、高溫...)。

```
期望溫度數據: ['地區',26,34,27,34]
```

#### 情況4
將資料寫入EXCEL檔案

#### 方法4
透過前面的方式，建立出二維陣列，再用下列的範例程式碼即可生成EXCEL，生成的方式是把二維陣列中的每個元素依序放入EXCEL的每一列當中。
```
生成的二維陣列如下:
[['', '06/10星期三最低溫', '06/10星期三最高溫', '06/11星期四最低溫', '06/11星期四最高溫', '06/12星期五最低溫', '06/12星期五最高溫', '06/13星期六最低溫', '06/13星期六最高溫', '06/14星期日最低溫', '06/14星期日最高溫', '06/15星期一最低溫', '06/15星期一最高溫', '06/16星期二最低溫', '06/16星期二最高溫'], ['基隆市白天', 26, 34, 27, 34, 27, 33, 27, 34, 27, 33, 27, 32, 27, 32], ['基隆市晚上', 26, 31, 27, 31, 27, 31, 27, 31, 26, 31, 26, 30, 26, 30], ....]
```
```
with xlsxwriter.Workbook('天氣資料.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(cityTempList): # cityTempList是一個二維陣列
        worksheet.write_row(row_num, 0, data)
```

### Reference
selenium的基本使用:<br>
https://freelancerlife.info/zh/blog/python%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2%E6%95%99%E5%AD%B8-selenium%E5%9F%BA%E6%9C%AC%E6%93%8D%E4%BD%9C/ <br>
selenium的指令範例:<br>
https://selenium-python.readthedocs.io/locating-elements.html
