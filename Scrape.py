from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


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

    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    def change_page_number(url, new_page_number):
        """
        Change the page number in the given URL.

        Args:
            url (str): The original URL.
            new_page_number (int): The new page number to be set.

        Returns:
            str: The updated URL with the new page number.

        Example:
            >>> original_url = "https://www.autoscout24.fr/lst/volkswagen/amarok?atype=C&cy=F&desc=0&powertype=kw&search_id=2fe1dqq1j4q&sort=standard&source=listpage_pagination&ustate=N%2CU"
            >>> new_page_number = 3
            >>> updated_url = change_page_number(original_url, new_page_number)
            >>> print("Original URL:", original_url)
            >>> print("Updated URL:", updated_url)
        """
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



    def format_articles_data(self):
        num_of_pages = self.getPageNumber()
        num_of_offers = self.getNumOffers()

        if num_of_pages == 0 | num_of_offers == 0 :
            return 'no result'
        
        pages_urls = []
        for i in range(2,num_of_pages+1):
            pages_urls.append(self.change_page_number(self.url,i))
        isFirstTime = True
        
        cars_data = []
        for page in pages_urls:
            if not isFirstTime:
                self.driver.get(page)
                self.driver.implicitly_wait(10)
            isFirstTime = False
            text_box = self.driver.find_element(by=By.CLASS_NAME, value="ListPage_main___0g2X")
            articles = text_box.find_elements(by=By.TAG_NAME, value = 'article')
            # set articles url table
            articles_url = []
            # get articles urls
            for article in articles:
                articles_url.append(self.get_article_url(article))
            
            for url in articles_url:
                if url == 'url not found':
                    continue
                cars_data.append({"url":url,"data":self.get_article_data(url)})
            

            
        return {'num_of_pages':num_of_pages,'num_of_offers':num_of_offers,'cars':cars_data}
    

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
            return {'other data willbe here:':'okay','title':title}
        except:
            return {"error":'data not found'}
        

    def exit(self):
        self.driver.quit()
                