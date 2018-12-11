from selenium import webdriver
from bs4 import BeautifulSoup as soup
import time
import os
import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument("--window-size=900,900")
options.add_argument("headless")
options.add_argument("nogpu")

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
driver.get('https://order.chipotle.com/Meal/Index/1928?showloc=1')
#Calhoun Chipotle - https://order.chipotle.com/Meal/Index/1928?showloc=1
#13th street - https://order.chipotle.com/Meal/Index/2168?showloc=1%27

os.system('clear')
intro = input('Do you want to order a burrito bowl with chicken, white rice, black beans and cheese from chipotle? (yes or no): \n')
if intro[0] == 'y':
        os.system('clear')
        print("Order began...")
else:
        quit()
try:
        wait = WebDriverWait(driver, 10)
        burrito_bowl = wait.until(EC.element_to_be_clickable((By.NAME, 'BURRITO BOWL')))
        driver.find_element_by_name('BURRITO BOWL').click()
        os.system('clear')
        print("added burrito bowl")
except:
        print('internet too slow')

try:
        chicken = wait.until(EC.element_to_be_clickable((By.ID, 'chicken')))
        driver.find_element_by_id('chicken').click()
        os.system('clear')
        print('added chicken')
except:
        print('internet too slow')

        time.sleep(1.5)
        whiterice = driver.find_element_by_id('ricewhite').click()
        os.system('clear')
        print('added white rice')

        time.sleep(1)
        brownrice = driver.find_element_by_id('ricebrown').click()
        os.system('clear')
        print('added brown rice')

try:
        blackbeans = wait.until(EC.element_to_be_clickable((By.ID, 'beansblack')))
        driver.find_element_by_id('beansblack').click()
        os.system('clear')
        print("added black beans")

except:
        print('internet too slow')
try:
        cheese = wait.until(EC.element_to_be_clickable((By.ID, 'cheese')))
        driver.find_element_by_id('cheese').click()
        os.system('clear')
        print("added cheese")
except:
        print('internet too slow')
try:
        add_bag = wait.until(EC.element_to_be_clickable((By.XPATH, '//[@id="elevator"]/div[1]/cmg-arrow-button/div/button')))
        driver.find_element_by_xpath("//[@id='elevator']/div[1]/cmg-arrow-button/div/button").click()
        os.system('clear')
        print("meal added to bag")
except:
        print('internet too slow')

try:
        checkout = wait.until(EC.element_to_be_clickable((By.XPATH, '//[contains(text(), "CHECKOUT")]')))
        driver.find_element_by_xpath("//[contains(text(), 'CHECKOUT')]").click()
        os.system('clear')
        print('checking out')
except:
        print('internet too slow')

try:
        email = wait.until(EC.element_to_be_clickable((By.NAME, 'email')))
        password = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
        sign_in = wait.until(EC.element_to_be_clickable((By.ID, 'sign-in')))
        email.send_keys('johnspagnoli1@gmail.com')
        password.send_keys('Chipotle#1')
        driver.find_element_by_id('sign-in').click()
        os.system('clear')
        print('succesfully signed in')
except:
        print('internet too slow')

try:
        pickup = wait.until(EC.element_to_be_clickable((By.XPATH, '//[@id="checkout-delivery-anchor"]/div[1]/cmg-tab-bar/div/div[1]')))
        driver.find_element_by_xpath('//[@id="checkout-delivery-anchor"]/div[1]/cmg-tab-bar/div/div[1]').click()
except:
        print('internet too slow')

try:
        pickup_continue = wait.until(EC.element_to_be_clickable((By.XPATH, '//[@id="checkout-delivery-anchor"]/cmg-checkout-restaurant/div[1]/div[2]/div[2]/button')))
        driver.find_element_by_xpath("//[@id='checkout-delivery-anchor']/cmg-checkout-restaurant/div[1]/div[2]/div[2]/button").click()
        os.system('clear')
        print('added pickup')
except:
        print('internet too slow')

try:
        pickup_time = wait.until(EC.element_to_be_clickable((By.XPATH, '//[@id="pickup-time-anchor"]/div[2]/button')))
        driver.find_element_by_xpath("//[@id='pickup-time-anchor']/div[2]/button").click()
        os.system('clear')
        print('pick up time confirmed')
except:
        print('internet too slow')

try:
        order_summary = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/ui-view/checkout-landing/div/div[2]/card[4]/div/div/div/cmg-checkout-summary/div/div[3]/div[4]/button[2]')))
        driver.find_element_by_xpath("/html/body/div[1]/div/ui-view/checkout-landing/div/div[2]/card[4]/div/div/div/cmg-checkout-summary/div/div[3]/div[4]/button[2]").click()
        os.system('clear')
        print('confirming order')
except:
        print('internet too slow')

try:
        name_on_card = wait.until(EC.element_to_be_clickable((By.NAME, 'ccname')))
        card_number = wait.until(EC.element_to_be_clickable((By.NAME, 'ccnumber')))
        exp_month = wait.until(EC.element_to_be_clickable((By.NAME, 'expdatemonth')))
        exp_year = wait.until(EC.element_to_be_clickable((By.NAME, 'expdateyear')))
        CVV = wait.until(EC.element_to_be_clickable((By.NAME, 'cvc')))
        zipcode = wait.until(EC.element_to_be_clickable((By.NAME, 'zip')))

        name_on_card.send_keys('GC Spagnoli')
        card_number.send_keys('1111111111111111')
        exp_month.send_keys('03')
        exp_year.send_keys('20')
        CVV.send_keys('111')
        zipcode.send_keys('10011')
        os.system('clear')
        print('credit card info added')
except:
        print('internet too slow')

        time.sleep(.5)
        os.system('clear')
        print('You ordered a burrito bowl with chicken, white rice, black beans and cheese\n')

        page = soup(driver.page_source, "lxml")
        time = page.find("h3", class_="selected-time")

def password_input():

        while True:
                password = 'Chipotle#1'
                password_enter = getpass.getpass('Enter in your password: ')
                if password_enter == password:
                        break
                else:
                        os.system('clear')
                        print('INCORRECT PASSWORD')
password_input()

def confirmation():

        while True:
                confirmation = input('Type "confirm" to confirm order: ')
                if confirmation == 'confirm':
                        place_order = driver.find_element_by_id('submit-order').click()
                        os.system('clear')
                        print('Your order has been placed. Enjoy your meal!\n\nPick up your meal at '+time.text+'.\n\n')
                        break
                else:
                        os.system('clear')
                        print('INCORRECT PASSWORD')
confirmation()
