from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import csv
from datetime import date
import copy


def connect():
    import mysql.connector
    con = mysql.connector.connect(user='root', password='',
                                  host='localhost',
                                  database='patrick', port=3306)
    return con


def insert_data(con, data):
    for row_value in data:
        add_data = (
            "insert into commsec_course_of_sales (asx_code,date,time,price,volume,value,market,condition_value) "
            "values (%s, %s, %s, %s, %s, %s, %s, %s) ")
        cursor = con.cursor()
        cursor.execute(add_data, tuple(row_value))
        con.commit()


def get_asx_codes():
    href = "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file?access_token" \
           "=83ff96335c2d45a094df02a206a39ff4"
    filename = "asx_codes.csv"

    response = requests.get(href)
    with open(filename, "wb") as f:
        f.write(response.content)


def get_data(asx_code):
    data = []
    try:
        # Find the shadow input element
        input_element = driver.execute_script(
            "return document.querySelector('commsec-header').shadowRoot.querySelector("
            "'search-bar').shadowRoot.querySelector("
            "'input')")
        input_element.send_keys(code)
        input_element.send_keys(Keys.RETURN)

        wait.until(EC.visibility_of_element_located((By.ID, 'overview_cost_of_sales_tab')))
        button = driver.find_element_by_id('overview_cost_of_sales_tab');
        button.click()
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'course-of-sales')))
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'tbody>cdk-virtual-scroll-viewport>div>tr')))

        table = driver.find_element_by_tag_name('course-of-sales').find_element_by_tag_name('table')
        txt = table.find_element_by_tag_name('tbody').text

        if txt.lower().strip() != "no records found.":
            # Get all rows of the table
            rows = table.find_element_by_tag_name('tbody').find_elements_by_xpath('.//tr')
            # Initialize an empty list to store the data

            # Loop through each row of the table
            for tr in rows:
                # Get all cells of the row
                cells = tr.find_elements_by_xpath('.//td')

                # Initialize an empty list to store the row data
                row_data = [code, date_str]

                # Loop through each cell of the row and extract the text
                for cell in cells:
                    row_data.append(cell.text.replace(',', ''))

                # Add the row data to the table data list
                data.append(row_data)
        return data
    except Exception as e:
        print("Exception in " + code)
        exception_list.append(code)
        return data


# download asx codes csv file
# get_asx_codes()

# Get the current date
today = date.today()

# Format the date as "Day Month Year"
date_str = today.strftime("%Y-%m-%d")

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

exception_list = []
con = connect()

with open("asx_codes.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)  # skip the first row
    for row in reader:
        code = row[0]
        print("Getting " + code)
        course_of_sales = get_data(code)
        insert_data(con, course_of_sales)

# try the codes that got exception in previous step
lst = copy.deepcopy(exception_list)
exception_list = []
for code in lst:
    course_of_sales = get_data(code)
    insert_data(con, course_of_sales)

print("Unable to scrap CODES :" + ", ".join(exception_list))
# Close the browser
driver.quit()
