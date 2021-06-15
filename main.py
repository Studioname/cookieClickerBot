from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import selenium
from selenium.webdriver.common.action_chains import ActionChains

driver_path = r"C:\Users\Conan\Development\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(driver_path)
cookie_clicker_endpoint = "https://orteil.dashnet.org/cookieclicker/"

driver.get(cookie_clicker_endpoint)
items = driver.find_elements_by_css_selector("#store div")


def get_total_cookies():
    cookies = driver.find_element_by_id("cookies").text.split()[0].replace(",", "")
    return int(cookies)


def get_cookies_per_minute():
    cookies = driver.find_element_by_id("cookies").text.split()[5]
    return cookies


def get_unformatted_price_list():
    return [x
                .text.replace(",","") for x in driver.find_elements_by_css_selector("#store .price") if x]


def get_formatted_price_list(unformatted_price_list):
    price_list = []
    for item in unformatted_price_list:
        if item != "":
            if "million" in item:
                item = float(item.split()[0]) * 1000000
                item = int(item)
            if get_total_cookies() >= int(item):
                price_list.append(int(item))
    return price_list


def get_list_of_buttons():
    button_list = [driver.find_element_by_id(f"product{i}") for i in range(0, len(get_formatted_price_list(get_unformatted_price_list())))]
    return button_list


def get_click_count():
    click_count = get_total_cookies()//max(get_formatted_price_list(get_unformatted_price_list()))
    return click_count


big_cookie = driver.find_element_by_id("bigCookie")


start = time.time()
purchase_timer = 5
purchase_timer_increment = 0
runtime_duration_in_seconds = 300

while time.time() - start <= runtime_duration_in_seconds:
    big_cookie.click()
    if time.time() - purchase_timer >= 5:
        price_list = get_formatted_price_list(get_unformatted_price_list())
        button_list = get_list_of_buttons()
        highest_cost_item = max(price_list, default=-10)
        if highest_cost_item != -10:
            highest_cost_item_index = price_list.index(highest_cost_item)
            button_list[highest_cost_item_index].click()

        purchase_timer_increment += 1
        purchase_timer = time.time() + purchase_timer_increment
