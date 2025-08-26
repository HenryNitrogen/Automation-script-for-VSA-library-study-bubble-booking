from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
bubble_name_str = input("Enter bubble name: ")
lunch_num_str = input("Enter lunch number (1 or 2): ")
lunch_num = int(lunch_num_str)
bubble_name = int(bubble_name_str)
if(bubble_name<1 or bubble_name>5):
    print("Invalid input")
    exit()
if(bubble_name==1):
    bubble_name="i13"
if(bubble_name==2):
    bubble_name="i16"
if(bubble_name==3):
    bubble_name="i19"
if(bubble_name==4):
    bubble_name="i22"

# 获取日期范围输入
date_mode = input("Choose date mode (1: Single date, 2: Date range): ")
if date_mode == "1":
    # 单个日期模式
    date_str = input("Enter date (MM-DD-YYYY): ")
    date_list = [date_str]
elif date_mode == "2":
    # 日期范围模式
    start_date_str = input("Enter start date (MM-DD-YYYY): ")
    end_date_str = input("Enter end date (MM-DD-YYYY): ")
    
    # 解析日期
    start_date = datetime.strptime(start_date_str, "%m-%d-%Y")
    end_date = datetime.strptime(end_date_str, "%m-%d-%Y")
    
    # 生成日期列表（跳过周末）
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        # 检查是否为周末 (weekday(): 0=Monday, 6=Sunday)
        # 5=Saturday, 6=Sunday
        if current_date.weekday() < 5:  # 只包含周一到周五
            date_list.append(current_date.strftime("%m-%d-%Y"))
        current_date += timedelta(days=1)
    
    print(f"Will submit forms for dates (excluding weekends): {', '.join(date_list)}")
    print(f"Total working days: {len(date_list)}")
else:
    print("Invalid mode selection")
    exit()
mail="ps20245058@student.vsa.edu.hk"
pw="Ni926666"
service = Service(executable_path="/Users/henrynitrogen/hi/py/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfYKdUSjYDq9XNQQcoRSm6SUA9B_4t3i11vafdeNpdIypJ0rA/viewform")

email_element = driver.find_element(By.XPATH, "//input[@type='email']")
email_element.send_keys(mail)
time.sleep(1)

click_element = driver.find_element(By.ID,"identifierNext")
click_element.click()
time.sleep(3)

password_element = driver.find_element(By.XPATH, "//input[@type='password']")
password_element.send_keys(pw)

pw_click_element = driver.find_element(By.ID,"passwordNext")
pw_click_element.click()
time.sleep(15)

def submit_form(current_date, form_count):
    try:
        email_confirm_element = driver.find_element(By.ID, "i5")
        is_checked = email_confirm_element.get_attribute("aria-checked") == "true"
        if(is_checked):
            print("Already selected")
        else:
            email_confirm_element.click()
            print("Now selected")
        
        bubble_room_element = driver.find_element(By.ID, bubble_name)
        bubble_room_element.click()
        time.sleep(1)

        date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@jsname='YPqjbf']")))
        # 清空现有内容并输入新日期
        date_input.clear()
        date_input.send_keys(current_date)
        time.sleep(1)

        period = driver.find_element(By.XPATH, "//div[@aria-selected='true']")
        period.click()
        time.sleep(1)

        if(lunch_num == 1):
            lunch1_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and @data-value='Lunch 1']"))
            )
            lunch1_option.click()
        else:
            lunch2_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and @data-value='Lunch 2']"))
            )
            lunch2_option.click()

        time.sleep(1)
        year = driver.find_element(By.ID, "i47")
        year.click()
        time.sleep(1)

        next1_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span"))
        )
        next1_element.click()
        time.sleep(2)
        purpose_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/span/div/div[1]"))
        )
        purpose_element.click()

        next2_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div[2]/span"))
        )
        next2_element.click()

        rules_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='i7']/div[2]"))
        )
        if rules_element.get_attribute("aria-checked") != "true":
            rules_element.click()

        final_submit_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div[2]/span"))
        )
        final_submit_element.click()
        time.sleep(3)
        print(f"Form submitted for date {current_date} (#{form_count})")
        
        # 刷新页面准备下次提交
        driver.refresh()
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Error submitting form for date {current_date}: {str(e)}")
        return False


# 循环提交每个日期的表单
form_count = 0
successful_submissions = 0
failed_submissions = 0

print(f"Starting to submit forms for {len(date_list)} date(s)...")

for date_str in date_list:
    form_count += 1
    print(f"\nProcessing date {form_count}/{len(date_list)}: {date_str}")
    
    if submit_form(date_str, form_count):
        successful_submissions += 1
    else:
        failed_submissions += 1
    
    # 在提交之间添加延迟以避免过于频繁的请求
    if form_count < len(date_list):  # 不是最后一个
        time.sleep(2)

print(f"\n=== Submission Summary ===")
print(f"Total dates processed: {len(date_list)}")
print(f"Successful submissions: {successful_submissions}")
print(f"Failed submissions: {failed_submissions}")

time.sleep(5)
driver.quit()