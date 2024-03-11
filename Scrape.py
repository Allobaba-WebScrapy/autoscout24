from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import math



class Url:
    def __init__(self, url,offers = 19,startFromPage=1,waitingTime=10):
        self.url = url
        self.offers = offers
        self.startFromPage = startFromPage
        self.waitingTime = waitingTime
         # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode
        # Create a Chrome WebDriver with opion we just set in Option object
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.implicitly_wait(self.waitingTime)
        
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

    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    def change_page_number(self,url, new_page_number):
        
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        query_parameters['page'] = [str(new_page_number)]
        updated_query_string = urlencode(query_parameters, doseq=True)
        updated_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            updated_query_string,
            parsed_url.fragment
        ))
        return updated_url 


    def get_page_number_from_url(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)

        # Extract the 'page' parameter if present, or default to 1
        page_number = int(query_parameters.get('page', ['1'])[0])

        return page_number

    def format_articles_data(self):
        num_of_pages = self.getPageNumber()
        num_of_offers = self.getNumOffers()
        errors = []
        if num_of_pages == 0 | num_of_offers == 0 :
            return {'error':'no result found'}
        
        #  test if startFromPage is greater than number of pages
        if self.startFromPage > num_of_pages:
            errors.append('startFromPage is greater than number of pages')
            print(errors)
            self.startFromPage = 1
        
        # set end page
        endPage = math.ceil(self.offers // 19)
        if endPage > num_of_pages:
            errors.append('number of offers is greater than offers found from page ${self.startFromPage} to ${num_of_pages}')
            print(errors[-1])
            endPage = num_of_pages

        
        print(num_of_pages)
        pages_urls = []
        for i in range(self.startFromPage,endPage+1):
            page = self.change_page_number(self.url,i)
            print('-------------------------------------------------------')
            print(page)
            print('-------------------------------------------------------')
            pages_urls.append(page)
        

        
        cars_data = []
        for page in pages_urls:
            if  page != self.driver.current_url:
                print('---------------------------------------------')
                print("going tot page ",page)
                self.driver.get(page)
                self.driver.implicitly_wait(self.waitingTime)
            text_box = self.driver.find_element(by=By.CLASS_NAME, value="ListPage_main___0g2X")
            articles = text_box.find_elements(by=By.TAG_NAME, value = 'article')
            # set articles url table
            articles_url = []
            # get articles urls
            for article in articles:
                articles_url.append(self.get_article_url(article))
            
            for url in articles_url:
                if (self.offers <= cars_data.__len__()):
                    continue
                if url == 'url not found':
                    print('product not found')
                    continue
                cars_data.append({"url":url,"data":self.get_article_data(url)})
                print('done with getting  data for url:',url)
            

            
        return {
            'num_of_pages':num_of_pages,
            'num_of_offers':num_of_offers,
            'start from page': self.startFromPage,
            'end in page': endPage,
            'pages urls':pages_urls,
            'offers got':cars_data.__len__(), 
            'cars':cars_data,
            'errors list':errors,
            'offers user want':self.offers,
            }
    

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
            self.driver.implicitly_wait(self.waitingTime)
            title = self.driver.find_element(by=By.CLASS_NAME,value='StageTitle_boldClassifiedInfo__sQb0l')
            title = title.text
            return {'other data willbe here:':'okay','title':title}
        except:
            return {"error":'data not found'}
        

    def exit(self):
        self.driver.quit()
                