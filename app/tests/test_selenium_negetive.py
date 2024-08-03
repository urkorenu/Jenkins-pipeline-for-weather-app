from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/")
title = driver.title
driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="location")
submit_button = driver.find_element(by=By.TAG_NAME, value="button")

text_box.send_keys("test")
submit_button.click()

if title == driver.title:
    assert False


driver.quit()
