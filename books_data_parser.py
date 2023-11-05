import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException

driver = webdriver.Chrome()
url = "https://prometheus-platform.github.io/Example_of_course_project_2/#/signin"
driver.get(url)
username_input = driver.find_element(By.NAME, "username")
username_input.clear()
username_input.send_keys("user")
sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign-In']")
sign_in_button.click()

results = []
for id in range(1, 22):
    url = f"https://prometheus-platform.github.io/Example_of_course_project_2/#/specific-book/{id}"
    try:
        driver.get(url)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        book_data = {}
        book_data['title'] = soup.find('h1', class_='fs-2 mb-3').text.strip()
        book_data['image_src'] = soup.find(
            'img', class_='img-fluid rounded')['src']
        book_data['descr'] = soup.find('div', class_='co-12 mb-3').text.strip()
        ul_element = soup.find('ul', class_='list-unstyled')
        if ul_element:
            list_items = ul_element.find_all('li')

            for item in list_items:
                text = item.text
                key, value = text.split(': ', 1)
                value = value.strip()
                if key == 'Author(s)':
                    book_data['author'] = value
                elif key == 'Book level':
                    book_data['level'] = value
                elif key == 'Book tags':
                    book_data['tags'] = value
        li_element = soup.find(
            'li', class_='list-group-item d-flex justify-content-between align-items-center border-0')

        if li_element:
            book_data['price'] = li_element.find('span').text

        results.append(book_data)
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Error on page {id}: {e}")
driver.quit()

with open('books_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)
