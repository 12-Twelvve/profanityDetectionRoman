from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
# Set up the WebDriver (make sure you have installed the appropriate WebDriver for your browser)
# driver = webdriver.Chrome('/path/to/chromedriver')
option = webdriver.ChromeOptions()
# option.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

# Open the YouTube video page
video_url = 'https://www.youtube.com/watch?v=eJQgUlL0LRo&pp=ygUYbmVwYWxpIHZ1bGdhciBpbnRlcnZpZXcg'
driver.get(video_url)
driver.maximize_window()
time.sleep(5)
# Scroll down to load more comments (modify this as needed)
scroll_pause_time = 2  # Time to pause between scrolls
scroll_limit = 5  # Number of times to scroll (increase this value if you want more comments)
prev_h = 0
while True:
    height= driver.execute_script("""
    function getActualHeight(){
        return Math.max(
            Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
            Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
            Math.max(document.body.clientHeight, document.documentElement.clientHeight),
            );
        }
    return getActualHeight()
    """)
    driver.execute_script(f"window.scrollTo({prev_h}, {prev_h +300})")
    prev_h +=900
    time.sleep(2)
    if prev_h >= height:
        break
# Parse the HTML source code with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the WebDriver
driver.quit()
title = soup.find("h1", class_="style-scope ytd-watch-metadata").text
print(title)
# Find the comment elements
comment_elements = soup.find_all('yt-formatted-string', {'id': 'content-text'})

# print(comment_elements)
# Extract the comments
comments = [comment.text for comment in comment_elements]

# Print the comments
for comment in comments:
    print(comment)

import csv
filename = 'data.csv'  # Specify the filename for the CSV file
# Open the file in write mode
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write each row of data to the CSV file
    for row in comments:
        writer.writerow(row)

# Close the WebDriver
driver.quit()