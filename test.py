from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# Specify the path to the chromedriver executable
chromedriver_path = '/usr/local/bin/chromedriver'
chrome_options.add_argument(f'--chromedriver={chromedriver_path}')
driver = webdriver.Chrome(options=chrome_options)

#driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)


driver.get('https://www.google.com')

print(driver.title)

driver.quit()