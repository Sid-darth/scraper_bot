"""Scraper to check bestbuy.com to check stock/price of requested product from it's url"""

from flask import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from icecream import ic
from dataclasses import dataclass
from pytz import timezone
import datetime as dt

@dataclass
class CheckStock:
    url : str

    def create_driver(self) -> object:
        """create and return a headless instance of a chrome webdriver"""
        url = self.url
        
        # chrome driver options
        chrome_options = webdriver.ChromeOptions()
        # add headless state amd fake-useragent
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # chrome driver executable
        chrome_driver_path = 'C:\dev_tools\chromedriver_win32\chromedriver.exe'
        chrome_service = Service(chrome_driver_path)
        # start driver
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        # drive into url
        driver.get(url)
        # stock status
        status = self.get_stock(driver)
        
        driver.close()
        
        return status
        
    def get_stock(self,driver : object) -> dict:
        """Get current stock status"""
        # get button container
        button_container = driver.find_element(By.CSS_SELECTOR,".fulfillment-add-to-cart-button button")
        status = button_container.text
        return status

    def get_time(self) -> str:
        """Get current pst"""
        # Pacific time now
        pst = timezone('US/Pacific') # time zone
        fmt = "%Y-%m-%d %H:%M:%S %Z%z" # strformat
        pst_now_ = dt.datetime.now(pst)
        pst_now = pst_now_.strftime(fmt)

        return pst_now

    def status_object(self) -> json:
        """create returnable json object that can be exposed to endpoints"""
        # product url
        url = self.url
        # get stock
        stock_status = self.create_driver()
        # get time
        time_now = self.get_time()
        # status json
        status_object = {
            "url" : url,
            "status" : stock_status,
            "last_updated" : time_now
        }

        return status_object


if __name__ == "__main__":
    url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6462956.p?skuId=6462956'
    Stock = CheckStock(url)
    status_object = Stock.status_object()
    ic(status_object)