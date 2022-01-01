"""
chromedriver mac无法移动到/usr/bin目录的情况下
https://www.selenium.dev/documentation/getting_started/
便捷选项是移动到当前虚拟环境的bin目录，比如pyenv，移动到~/.pyenv/version/you-path/bin目录
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

s1 = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
# This example requires Selenium WebDriver 3.13 or newer
with webdriver.Chrome(chrome_options=chrome_options) as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://google.com/ncr")
    driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
    first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3")))
    print(first_result.get_attribute("textContent"))
print(time.time() - s1)
