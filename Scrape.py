from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Url:
    def __init__(self, url):
        self.url = url
         # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode
        # Create a Chrome WebDriver with opion we just set in Option object
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        
    def getPageNumber(self):
        try:
            list_pages_links = self.driver.find_elements(by=By.CLASS_NAME,value='pagination-item')
            return  int(list_pages_links[-1].find_element(by=By.TAG_NAME,value='button').text)
        except:
            return 0
        
    def getNumOffers(self):
        try:
            results = self.driver.find_element(by=By.CLASS_NAME,value='ListHeaderExperiment_title_with_sort__Gj9w7')
            results = results.find_element(by=By.TAG_NAME,value='span')
            results = results.find_elements(by=By.TAG_NAME,value='span')
            return int(results[0].text)
        except:
            return 0
        
    def format_articles_data(self):
        num_of_pages = self.getPageNumber()
        num_of_offers = self.getNumOffers()

        if num_of_pages == 0 | num_of_offers == 0 :
            return 'no result'
        
        text_box = self.driver.find_element(by=By.CLASS_NAME, value="ListPage_main___0g2X")
        articles = text_box.find_elements(by=By.TAG_NAME, value = 'article')
        
        articles_url = []
        cars_titles = []

        for article in articles:
            articles_url.append(self.get_article_url(article))
            
        for url in articles_url:
            if url == 'url not found':
                continue
            cars_titles.append(self.get_article_data(url))
        return {'num_of_pages':num_of_pages,'num_of_offers':num_of_offers,'cars_url':articles_url,'cars_title:':cars_titles}
    

    def get_article_url(self,article):
        try:
            div = article.find_element(by=By.CLASS_NAME,value='ListItem_header__J6xlG')
            a = div.find_element(by=By.TAG_NAME, value='a')
            url = a.get_attribute('href')
            print(url)
            return url
        except:
            return 'url not found'

    def get_article_data(self,url):
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            title = self.driver.find_element(by=By.CLASS_NAME,value='StageTitle_boldClassifiedInfo__sQb0l')
            title = title.text
            return {'url':url,'title':title}
        except:
            return {"error":'data not found'}
        

    def exit(self):
        self.driver.quit()
                