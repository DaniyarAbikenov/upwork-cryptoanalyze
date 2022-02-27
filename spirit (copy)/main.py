from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
import json


def read_json(name):
    try:
        with open(name, "r") as file:
            return json.load(file)
    except Exception as ex:
        print(ex)
        return {}  # if file not exist, create empty dict


def write_json(dict_data):
    with open("data.json", "w") as file:
        json.dump(dict_data, file, indent=4)


def check_change(driver, url="https://app.ola.finance/networks/0x892701d128d63c9856A9Eb5d967982F78FD3F2AE/markets"):
    driver.get(url)
    sleep(3)  # wait, while table is loaded
    table = driver.find_elements(By.CLASS_NAME, "jss140")[1]  # select second table on site
    data_dict = read_json("data.json")  # loaded data, if exists
    while True:  # check table all time
        cols = table.find_elements(By.CLASS_NAME, "jss142")  # parse all currencies
        for col in cols:
            now = datetime.now()
            times = now.strftime("%d-%m-%Y %H:%M")  # date is used as a key
            cells = col.find_elements(By.CLASS_NAME, "MuiGrid-root")
            for i in range(0, len(cells)):  # convert object Selenium to string
                cells[i] = cells[i].text
            title, price = cells[0], cells[3]
            if title not in data_dict.keys():
                data_dict[title] = {}
                data_dict[title]["last"] = price
                data_dict[title][times] = price
            else:
                if data_dict[title]["last"] != price:
                    data_dict[title]["last"] = price
                    print(f"{title} is changed")
                    data_dict[title][times] = price
        write_json(data_dict)


def main():
    driver = webdriver.Chrome("chrome/chromedriver")
    check_change(driver=driver)
    driver.quit()


if __name__ == '__main__':
    main()
