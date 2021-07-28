from selenium import webdriver
import time

chrome_driver_path = "/Applications/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Time Stamps
timeout = time.time() + 5
end = time.time() + 5*60

# The Cookie
cookie = driver.find_element_by_xpath('//*[@id="cookie"]')

# Shop Items
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

prices = driver.find_elements_by_css_selector("#store b")
item_prices = []
for price in prices:
    text = price.text
    if text != "":
        cost = int(text.split("-")[1].strip().replace(",", ""))
        item_prices.append(cost)

shop = {}
for item_id, item_price in zip(item_ids, item_prices):
    shop[item_price] = item_id


while True:
    cookie.click()

    # Every 5 Seconds
    if time.time() > timeout:

        # Current Cookie Count
        money = str(driver.find_element_by_id("money").text)
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        # Check For Most Expensive Item Available And Buy
        max_available = 0
        for price in item_prices:
            if price <= cookie_count:
                max_available = price
        driver.find_element_by_id(shop[max_available]).click()

        # Resetting The 5 Second Timer
        timeout = time.time() + 5

    # After 5 Minutes The Script Stops And Prints Out The Cookies Per Second Rating
    if time.time() > end:
        print(driver.find_element_by_id("cps").text)
        break
