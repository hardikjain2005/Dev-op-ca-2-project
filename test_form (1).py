from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os

driver = webdriver.Chrome()

file_path = "file:///" + os.getcwd() + "/form.html"
driver.get(file_path)

driver.maximize_window()
time.sleep(2)

# Fill form
driver.find_element(By.ID,"name").send_keys("Rahul")
driver.find_element(By.ID,"email").send_keys("rahul@gmail.com")
driver.find_element(By.ID,"password").send_keys("123456")
driver.find_element(By.ID,"confirm").send_keys("123456")

# ✅ FIX: Select gender using NAME instead of ID
gender = driver.find_elements(By.NAME, "gender")
gender[0].click()   # Select Male

# Select course
course = Select(driver.find_element(By.ID,"course"))
course.select_by_visible_text("BCA")

# Submit
driver.find_element(By.XPATH,"//input[@type='submit']").click()

time.sleep(5)
driver.quit()