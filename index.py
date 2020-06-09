import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import xlsxwriter

driver = webdriver.Chrome()  # 如果你沒有把webdriver放在同一個資料夾中，必須指定位置給他
driver.get("https://www.cwb.gov.tw/V8/C/W/week.html")

# 等待javascript渲染出來
time.sleep(3)

# 取得整個天氣表格
def getTable():
    container = driver.find_element_by_id('w-1')
    table = container.find_element_by_tag_name('table')
    return table
# 取得一個城市的子表格列表
def getCityTable(table):
    return table.find_elements_by_tag_name('tbody')
# 取得城市名稱
def getCityName(table):
    tmp = []
    for i in range(len(table)):
        print(i)
        item = table[i].find_element_by_tag_name('th')
        name = item.find_element_by_css_selector('span.heading_3')
        tmp.append(name.get_attribute('innerText'))
        print(tmp[i])
    return tmp
# 取得溫度，並拆分最高溫與最低溫，白天、晚上的溫度列表會分開
def getTemp(table, name):
    tempList = []
    cityAndTemp = []
    for i in range(len(table)):
        print(i)
        items = table[i].find_elements_by_tag_name('td')
        print(name[i])
        cityAndTemp.append(name[i]+'白天')
        for j in range(len(items)):
            tempRange = items[j].find_element_by_class_name(
                'tem-C').get_attribute('innerText').replace('\u2002', '')
            temps = tempRange.split('-')
            # tempList.append(temps[0])
            # tempList.append(temps[1])
            cityAndTemp.append(int(temps[0]))
            cityAndTemp.append(int(temps[1]))
            if j == 6:
                print('晚間溫度')
                tempList.append(cityAndTemp)
                cityAndTemp = []
                cityAndTemp.append(name[i]+'晚上')
            # print(tempList[j])
            if j == len(items)-1:
                tempList.append(cityAndTemp)
                cityAndTemp = []
    return tempList

# 取得日期
def getDate(table):
    days = table.find_element_by_class_name('table_top')
    dayList = days.find_elements_by_tag_name('th')
    date = []
    for i in range(len(dayList)):
        if i == 0:
            date.append('')
        if i > 0:
            date.append(dayList[i].get_attribute('innerText').replace(
                '\n', '').replace('\t', '').replace(' ', '')+'最高溫')
            date.append(dayList[i].get_attribute('innerText').replace(
                '\n', '').replace('\t', '').replace(' ', '')+'最低溫')
    return date


table = getTable()
cityTable = getCityTable(table)
cityNameList = getCityName(cityTable)
cityTempList = getTemp(cityTable, cityNameList)
dateList = getDate(table)

# 插入日期到第一列
cityTempList.insert(0, dateList)

print(cityNameList)
print(cityTempList)
print(dateList)

# html = driver.page_source # 取得html文字
# elem = driver.find_element_by_css_selector('span.tem-C')
# print(elem.get_attribute('innerHTML'))
driver.close()  # 關掉Driver打開的瀏覽器

with xlsxwriter.Workbook('天氣資料.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(cityTempList):
        worksheet.write_row(row_num, 0, data)
