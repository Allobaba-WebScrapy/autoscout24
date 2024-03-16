from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import math

class AutoScout24:
    def __init__(self, url,offers = 19,startFromPage=1,waitingTime=30):
        self.url = url
        self.offers = offers
        self.startFromPage = startFromPage
        self.waitingTime = waitingTime
        self.errors = []
        self.num_of_pages = 0
        self.num_of_offers = 0
        self.endPage = 0

         # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode
        # Create a Chrome WebDriver with opion we just set in Option object
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(self.waitingTime)
        self.wait = WebDriverWait(self.driver, self.waitingTime)
        self.driver.get(self.url)

    
    # get number of pages
    def getPageNumber(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination-item')))
            list_pages_links = self.driver.find_elements(by=By.CLASS_NAME,value='pagination-item')
            return  int(list_pages_links[-1].find_element(by=By.TAG_NAME,value='button').text)
        except:
            self.errors.append('pages menu not found')
            print(self.errors[-1])
            return 0
    

    # it's used to get number of offers found
    def getNumOffers(self):
        try:
            # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ListHeaderExperiment_title_with_sort__Gj9w7')))
            span = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/div[5]/header/div/div[1]/h1/span/span[1]")
            return int(span.text)
        except:
            self.errors.append('offers not found')
            print(self.errors[-1])
            return 0
    
    

    # change page number in url
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
    
    # get page number from url
    def get_page_number_from_url(self,url):
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)

        # Extract the 'page' parameter if present, or default to 1
        page_number = int(query_parameters.get('page', ['1'])[0])

        return page_number
    # go to page given by url
    def change_page_to(self,page):
        # Todo: check if the page is already opened excption
        try:
            # if self.get_page_number_from_url(self.driver.current_url) != self.get_page_number_from_url(page):
            print('---------------------------------------------')
            print("going to page ",page)
            self.driver.get(page)
            self.driver.implicitly_wait(self.waitingTime)
            
        except:
            self.errors.append('error in changing page')
            print(self.errors[-1])
            
    
    def get_article_url(self,article):
        try:
            div = article.find_element(by=By.CLASS_NAME, value = 'ListItem_header__J6xlG')
            a = div.find_element(by=By.TAG_NAME, value='a')
            url = a.get_attribute('href')
            print(url)
            return url
        except:
            return 'not found'

    def get_article_data(self,url):
        try:
            try:
                self.change_page_to(url)
                # title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'StageTitle_boldClassifiedInfo__sQb0l')))
                title = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[1]")
                title = title.text
                
            except Exception as e:
                print('Error:title not found \n',e)
                title = 'not found'
            print('-- titile : ',title)

            try:
                # title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'StageTitle_boldClassifiedInfo__sQb0l')))
                div = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[2]")
                model = div.text
                
            except Exception as e:
                print('Error:title not found \n',e)
                model = 'not found'
            print('-- model : ',model)

            try:
                # self.wait.until(EC.presence_of_element_located(by=By.XPATH,value = '//*[@id="vendor-section-call-button"]'))
                info_card = self.driver.find_element(by=By.CLASS_NAME,value ="VendorData_mainContainer__qdM_f")
            except Exception as e:
                print('Error:info card not found')
                info_card = False
            if info_card:
                vendor_info = {}
                self.driver.implicitly_wait(0)
                # get vendor numbers
                try:    
                    info_card.find_element(by=By.XPATH,value = '//*[@id="vendor-section-call-button"]').send_keys(Keys.ENTER)
                    print('btn clicked')
                    print('searching for numbers')
                    # time.sleep(10)
                    numbers_container = info_card.find_element(by=By.CLASS_NAME,value = "Contact_vendorCta___VygD")
                    print('numbers container found')
                    numbers_a = numbers_container.find_elements(by=By.TAG_NAME,value='a')
                    print('numbers a found')
                    # get numbers href
                    numbers = []
                    for a in numbers_a:
                        numbers.append(a.get_attribute('href'))
                    print("phone number list : ",numbers)
                    vendor_info['numbers'] = numbers
                except:
                    print('Error:number not found \n')
                    vendor_info['numbers'] = 'not found'
                # get vendor name
                try:
                    vendor_info['name'] = info_card.find_element(by=By.CLASS_NAME,value = "Contact_contactName__ZZISd").text
                    print('vendor name: ',vendor_info['name'])
                except:
                    print('Error:name not found \n')
                    vendor_info['name'] = 'not found'
                
                # get vendor address
                try:
                    vendor_info['address'] = {}
                    a_element = info_card.find_element(by=By.CLASS_NAME,value = "Department_link__xMUEe")
                    vendor_info['address']['url'] = a_element.get_attribute('href')
                    vendor_info['address']['text'] = a_element.text.strip()
                    # vendor_info['address'] = info_card.find_element(by=By.CLASS_NAME,value = "Contact_contactAddress__3Aq9c").text
                    print('vendor address: ',vendor_info['address'])
                except:
                    print('Error:address not found \n')
                    vendor_info['address'] = 'not found'
                
                # get vendor company name
                try:
                    vendor_info['company'] = info_card.find_element(by=By.CLASS_NAME,value = "RatingsAndCompanyName_dealer__EaECM").find_element(by=By.TAG_NAME,value='div').text
                    print('vendor company: ',vendor_info['company'])
                except:
                    print('Error:company not found \n')
                    vendor_info['company'] = 'not found'
                
                # get is vendor pro or not
                try:
                    
                    try:
                        vendor_info['pro'] = info_card.find_element(by=By.CLASS_NAME,value = "VendorData_title__ZcxKQ").find_element(by=By.TAG_NAME,value='span').text == 'Pro'
                    except:
                        vendor_info['pro'] = False
                    print('vendor pro: ',vendor_info['pro'])
                except:
                    print('Error:pro not found \n')
                    vendor_info['pro'] = 'not found' 
                    

            else:
                vendor_info = 'no data found'       
            self.driver.implicitly_wait(self.waitingTime)

            return {'title':title,'vendor_info':vendor_info, 'model':model}
        except Exception as e:
            print('**Error** get_article_data nothing found')
            return {"error":'data not found'}
    def format_articles_data(self):
        self.num_of_pages = self.getPageNumber()
        self.num_of_offers = self.getNumOffers()
        print(self.num_of_pages,self.num_of_offers)

        if self.num_of_pages == 0 | self.num_of_offers == 0 :
            return {'error':'no result found'}
        
        #  test if startFromPage is greater than number of pages
        if self.startFromPage > self.num_of_pages:
            self.errors.append('startFromPage is greater than number of pages, will start from page 1')
            print(self.errors[-1])
            self.startFromPage = 1
        
        # set page we will stop in
        self.endPage = self.startFromPage + math.ceil(self.offers / 19)
        if self.endPage > self.num_of_pages:
            self.errors.append('number of offers is greater than offers found from page ${self.startFromPage} to ${num_of_pages}')
            print(self.errors[-1])
            self.endPage = self.num_of_pages + 1

        # get pages urls
        # -------------------------------------------------------------------
        
        pages_urls = []
        for i in range(self.startFromPage,self.endPage):
            page = self.change_page_number(self.url,i)
            print('-------------------------------------------------------')
            print(page)
            print('-------------------------------------------------------')
            pages_urls.append(page)
        # -------------------------------------------------------------------
        
        # get offers data (cars data - title, phone numbers, ...)
        # -------------------------------------------------------------------
        cars_data = []
        for page in pages_urls:
            self.change_page_to(page)
            
            try:
                main = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[5]/div[3]/main")
                # main = self.driver.find_element(by=By.CLASS_NAME, value = 'ListPage_main___0g2X')
                articles = main.find_elements(by=By.TAG_NAME, value = 'article')
                if articles.__len__() == 0:
                    raise Exception('no article found')
            except Exception as e:
                print('*****Error******no article found')
                self.errors.append('articles not found')
                print(self.errors[-1])
                continue
            # set articles url table
            articles_url = []
            # get articles urls
            for article in articles:
                articles_url.append(self.get_article_url(article))
            # print(articles_url)
            for url in articles_url:
                if (self.offers <= cars_data.__len__()):
                    continue
                if url == 'not found':
                    print('offer url not found')
                    continue
                cars_data.append({"url":url,"data":self.get_article_data(url)})
                print('-----done with getting  data for url:',url)
        # -------------------------------------------------------------------
        
        if cars_data.__len__() < self.offers:
            self.errors.append('number of offers found is less than offers user want')
            print(self.errors[-1])
            

        self.driver.quit()         
        return {
            'num_of_pages':self.num_of_pages,
            'num_of_offers':self.num_of_offers,
            'start from page': self.startFromPage,
            'end in page': self.endPage,
            'pages urls':pages_urls,
            'offers got':cars_data.__len__(), 
            'cars':cars_data,
            'errors list':self.errors,
            'offers user want':self.offers,
            }
    