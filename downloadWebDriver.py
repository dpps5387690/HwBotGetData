import os
import zipfile

import requests
import wget


def downloadWebvDriver():
    # get the latest chrome driver version number
    if os.path.isfile("chromedriver.exe"):
        print("The chromedriver.exe is exist.")
        return
    else:
        print("The chromedriver.exe isn't exist.")

    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall()  # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)
