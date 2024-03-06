from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)


def getpageNumber(driver):
    try:
        list_pages_links = driver.find_elements(by=By.CLASS_NAME,value='pagination-item')
        return  int(list_pages_links[-1].find_element(by=By.TAG_NAME,value='button').text)
    except:
        return 0

def getNumOffers(driver):
    try:
        results = driver.find_element(by=By.CLASS_NAME,value='ListHeaderExperiment_title_with_sort__Gj9w7')
        results = results.find_element(by=By.TAG_NAME,value='span')
        results = results.find_elements(by=By.TAG_NAME,value='span')
        return int(results[0].text)
    except:
        return 0

def getArticlesUrls(driver):
    text_box = driver.find_element(by=By.CLASS_NAME, value="ListPage_main___0g2X")
    articles = text_box.find_elements(by=By.TAG_NAME,value = 'article')
    
    cars_url = []
    cars_titles = []

    for article in articles:
        try:
            div = article.find_element(by=By.CLASS_NAME,value='ListItem_header__J6xlG')
            a = div.find_element(by=By.TAG_NAME, value='a')
            url = a.get_attribute('href')
            print(url)
            cars_url.append(url)
        except:
            cars_url.append('url not found')
            print('url not found')
        
    for url in cars_url:
        try:
            driver.get(url)
            print('wait 10 seconds')
            driver.implicitly_wait(10)
            print('wait 10 seconds done')
            
            title = driver.find_element(by=By.CLASS_NAME,value='StageTitle_boldClassifiedInfo__sQb0l')
            title = title.text
            print(title)
            cars_titles.append(title)
        except:
            cars_titles.append('title not found')
            print('title not found')
            
    return cars_url,cars_titles


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/scrape')
def scrape():
    url = 'https://www.autoscout24.fr/lst/bmw/i3?atype=C&cy=F&damaged_listing=exclude&desc=0&fregfrom=2022&fregto=2024&powerfrom=130&powertype=kw&pricefrom=2500&search_id=1qv0q5u1xd1&sort=standard&source=homepage_search-mask&ustate=N%2CU'

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode

    # Create a Chrome WebDriver with opion we just set in Option object
    driver = webdriver.Chrome(options=chrome_options)

    # navigate to url
    driver.get(url)
    driver.implicitly_wait(5)

    
    num_of_pages = getpageNumber(driver)
    num_of_offers = getNumOffers(driver)
    print(num_of_offers)
    print(num_of_pages)
    if num_of_pages == 0 | num_of_offers == 0 :
        return 'no result'
    # Extract the title using Selenium
    title = driver.title
    
    text_box = driver.find_element(by=By.CLASS_NAME, value="ListPage_main___0g2X")
    articles = text_box.find_elements(by=By.TAG_NAME,value = 'article')
    
    cars_url = []
    cars_titles = []

    cars_url,cars_titles = getArticlesUrls(driver)

    # Close the browser window
    driver.quit()

    return jsonify({'title': title,'pages number':num_of_pages,'offers number':num_of_offers,'cars':cars_url,'titiles':cars_titles,'author':'ilorez not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
