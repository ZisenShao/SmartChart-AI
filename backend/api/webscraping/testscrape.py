from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to ChromeDriver
service = Service(executable_path="/Users/priyarajaram/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com")
print("ChromeDriver is working!")
driver.quit()
