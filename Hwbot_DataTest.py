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


def getDataformUrl(FileIO, BenchMark):
    stringlist = []
    url = "https://hwbot.org/benchmark/%s/rankings?hardwareTypeId=processor_6627&cores=16#start=0#interval=20" % (
        BenchMark)
    # url = "https://hwbot.org/benchmark/3dmark_cpu_profile_max/rankings?hardwareTypeId=processor_6627&cores=16#start=0#interval=20"
    try:
        driver = webdriver.Chrome(service=WebDriverPath, options=chrome_options)
        driver.get(url)
        # driver.maximize_window()
        # time.sleep(5)

        Titile = driver.find_element("xpath", '//*[@id="ranking-table-title"]').text
        print(Fore.BLUE + "Titile " + Titile + Fore.WHITE)
        stringlist.append(Titile + "\n")

        # Header = driver.find_element("xpath", '//*[@id="submissionstable"]/thead/tr')
        # SCORE = Header.find_element("xpath", './td[2]').text
        # USER = Header.find_element("xpath", './td[3]').text
        # FREQUENCY = Header.find_element("xpath", './td[4]').text
        # print(SCORE, USER, FREQUENCY)

        datas = driver.find_elements("xpath", '//*[@id="submissionstable"]/tbody/tr')

        for data in datas[:3]:  # get first 3 row
            SCORE = data.find_element("xpath", './td[2]').text
            USER = data.find_element("xpath", './td[4]').text
            FREQUENCY = data.find_element("xpath", './td[5]').text

            strline = "%25s %25s %15s" % (SCORE, USER, FREQUENCY)
            stringlist.append(strline + "\n")
            print(strline)
    except:
        strline = "Fail Read %s" % (BenchMark)
        print(Fore.RED + strline + Fore.WHITE)

    driver.quit()
    return stringlist


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
        print(BenchMarkName, BenchMarkValue)
        BenchMarkList.append(dict(BenchMarkName=BenchMarkName, BenchMarkValue=BenchMarkValue))
    driver.quit()
    return BenchMarkList


# 開始測量


NowTime = datetime.now().strftime("%Y%m%d_%H%M%S")

print(NowTime)
FileName = NowTime
FileIO = open(FileName, 'w')
# getDataformUrl(FileIO, "xtu")
start = time.time()
BenchMarkList = getallBenchMark("core_i9_12900k")

for BenchMark in BenchMarkList:
    BenchMarkName = BenchMark["BenchMarkName"]
    BenchMarkValue = BenchMark["BenchMarkValue"]
    stringlist = []
    if BenchMarkValue == "n/a":
        strline = "%s BenchMark No Rank Data\n" % (BenchMarkName)
        stringlist.append(strline)
        print(Fore.GREEN + strline + Fore.WHITE)
        continue

    retry = 5
    while True:
        stringlist = getDataformUrl(FileIO, BenchMarkName)
        if (len(stringlist) > 1) or (retry == 0):
            break
        retry -= 1
        time.sleep(5)

    if retry == 0:
        strline = "retry fail Read %s\n" % (BenchMarkName)
        stringlist.append(strline)
        print(Fore.YELLOW + strline + Fore.WHITE)

    FileIO.writelines(stringlist)
    # time.sleep(5)

# 結束測量
end = time.time()

# 輸出結果
TotalTIme = "Total Time: %s\n" % (timedelta(seconds=(end - start)))
# TotalTIme = "Total Time: %s\n" % (datetime.utcfromtimestamp(end - start).strftime("%H:%M:%S.%f"))
FileIO.writelines(TotalTIme)
print(TotalTIme)

FileIO.close()
