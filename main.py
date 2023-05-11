from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import csv


def connect():
    import mysql.connector
    con = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='patrick', port=3306)
    return con


def insert_data(con, data):
    for row in data:
        print(row)
        add_data = (
            "insert into asx_table (asx_code,announcement_date,announcement_time,announcement_title,page_count,file_size,link) values (%s, %s, %s, %s, %s, %s, %s) ")
        cursor = con.cursor()
        cursor.execute(add_data, tuple(row))
        con.commit()


def get_asx_codes():
    href = "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file?access_token" \
           "=83ff96335c2d45a094df02a206a39ff4"
    filename = "asx_codes.csv"

    response = requests.get(href)
    with open(filename, "wb") as f:
        f.write(response.content)


# download asx codes csv file
get_asx_codes()

# Set up the web driver and navigate to the login page
driver = webdriver.Chrome("c:\\chromedriver.exe")

driver.get("https://www2.commsec.com.au/secure/login")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, 'username')))

# Find the username and password input fields, and enter your login details
username_field = driver.find_element_by_id("username")
password_field = driver.find_element_by_id("password")
username_field.send_keys("50739011")
password_field.send_keys("SGGU!Y78Sssd3d")

# Submit the login form
password_field.send_keys(Keys.RETURN)

element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'commsec-header')))

with open("asx_codes.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)  # skip the first row
    for row in reader:
        try:
            code = row[0]

            # Find the shadow input element
            input_element = driver.execute_script(
                "return document.querySelector('commsec-header').shadowRoot.querySelector("
                "'search-bar').shadowRoot.querySelector("
                "'input')")
            input_element.send_keys(code)
            input_element.send_keys(Keys.RETURN)

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.ID, 'overview_cost_of_sales_tab')))
            button = driver.find_element_by_id('overview_cost_of_sales_tab');
            button.click()
            element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'course-of-sales')))
            element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'tbody>cdk-virtual-scroll-viewport>div>tr')))

            table = driver.find_element_by_tag_name('course-of-sales').find_element_by_tag_name('table')
            txt = table.find_element_by_tag_name('tbody').text
            print(txt)
        except Exception as e:
            print("Exception in " + code)
# Close the browser
driver.quit()
