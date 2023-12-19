from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = "https://www.ycombinator.com/companies?batch=W24&batch=S23"


driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break


print(driver.current_url)
print(driver.execute_script("return document.readyState"))

web_content = driver.page_source


soup = BeautifulSoup(web_content, 'html.parser')
s = soup.find('div', class_='_section_lx3q7_146 _results_lx3q7_327')

descriptions = []

for anchor in s.find_all('a', class_='_company_lx3q7_339'):
    complete_url = urljoin("https://www.ycombinator.com", anchor.get('href'))
    driver.get(complete_url)
    time.sleep(3)

    try:
        company_description_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'prose.max-w-full'))
        )
        
        paragraphs = company_description_div.find_elements_by_tag_name('p',class_='whitespace-pre-line')
        description = "\n".join([paragraph.text.strip() for paragraph in paragraphs])
        descriptions.append(description)
    except:
        descriptions.append("Description not found.")

for name, url, description in zip(soup.find_all('span', class_='_coName_lx3q7_454'), s.find_all('a', class_='_company_lx3q7_339'), descriptions):
    complete_url = urljoin("https://www.ycombinator.com", url.get('href'))
    print(f"Company Name: {name.text.strip()}\nURL: {complete_url}\nDescription: {description}\n")





# driver.get(complete_url)
# time.sleep(3)
# company_description = soup.find('div',class_='prose max-w-full')
# des = soup.find_all('p')
# for line in des:
#     print(line.text)
    
# print(f"Description: {company_description}\n")


