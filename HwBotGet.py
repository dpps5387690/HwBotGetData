from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

WebDriverPath = Service('./chromedriver.exe')
WINDOW_SIZE = "1920,1080"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


def getAllData(url):
    # url = "https://hwbot.org/submission/5028103_d3lta_king_3dmark_cpu_profile_max_core_i9_12900k_15901_marks"
    driver = webdriver.Chrome(service=WebDriverPath, options=chrome_options)
    driver.get(url)

    datas = driver.find_elements("xpath",
                                 '//*[@itemprop="author"]/a')

    Name = datas[0].text
    BenchMark = datas[1].text

    datas = driver.find_elements("xpath",
                                 '//*[@class="result float-left"]/p/span')

    Source = datas[0].text

    datas = driver.find_elements("xpath",
                                 '//*[@id="media"]/dl')

    ModelName = "null"
    if len(datas) > 1:
        Model = datas[1].text
        if "BIOS/UEFI" in Model:
            Model = datas[2].text
        if "CHECKSUM" not in Model:
            ModelName = Model
    strline = "%60s %25s %25s %30s" % (BenchMark, Source, Name, ModelName)
    print(strline)
    driver.quit()


def getallBenchMark(CPUStr):
    url = "https://hwbot.org/hardware/processor/%s/" % (CPUStr)
    driver = webdriver.Chrome(service=WebDriverPath, options=chrome_options)
    driver.get(url)

    datas = driver.find_elements("xpath",
                                 '//*[@id="hardwarerecordssummary"]/*[@class="listview small responsive"]/tbody/tr')
    BenchMarkList = []
    for data in datas:  # get first 3 row
        BenchMarkName = data.find_element("xpath", './td[1]').text.lower().replace(" ", "_")
        BenchMarkValue = data.find_element("xpath", './td[2]').text.lower().replace(" ", "_")

        BenchMarkUrl = ""
        if BenchMarkValue != "n/a":
            BenchMarkUrl = data.find_element("xpath", './td[2]/a').get_attribute("href")

        print(BenchMarkName, BenchMarkValue, BenchMarkUrl)
        BenchMarkList.append(
            dict(BenchMarkName=BenchMarkName, BenchMarkValue=BenchMarkValue, BenchMarkUrl=BenchMarkUrl))
    driver.quit()
    return BenchMarkList


# url = "https://hwbot.org/submission/4847355_splave_cinebench___2003_core_i9_12900k_12770_cb"
# getAllData(url)
start = time.time()

BenchMarkList = getallBenchMark("core_i9_12900k")
print(Fore.CYAN)
for BenchMark in BenchMarkList:
    BenchMarkName = BenchMark["BenchMarkName"]
    BenchMarkValue = BenchMark["BenchMarkValue"]
    BenchMarkUrl = BenchMark["BenchMarkUrl"]
    if BenchMarkValue == "n/a":
        strline = "%s BenchMark No Rank Data\n" % (BenchMarkName)
        print(Fore.GREEN + strline + Fore.CYAN)
        continue
    getAllData(BenchMarkUrl)

# 結束測量
end = time.time()

# 輸出結果
TotalTIme = "Total Time: %s\n" % (timedelta(seconds=(end - start)))
# TotalTIme = "Total Time: %s\n" % (datetime.utcfromtimestamp(end - start).strftime("%H:%M:%S.%f"))
print(TotalTIme)
