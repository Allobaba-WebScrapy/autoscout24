from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
import json
class AutoScout24:
    def __init__(self, url,offers = 19,startFromPage=1,waitingTime=30, businessType = "b2b"):
        self.url = url
        self.offers = offers
        self.startFromPage = startFromPage
        self.waitingTime = waitingTime
        self.errors = []
        self.num_of_pages = 0
        self.num_of_offers = 0
        self.endPage = 0
        self.businessType = businessType

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
            self.errors.append('error/pages-number/not-found')
            print(self.errors[-1])
            return 0
    

    # it's used to get number of offers found
    def getNumOffers(self):
        try:
            # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ListHeaderExperiment_title_with_sort__Gj9w7')))
            span = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/div[5]/header/div/div[1]/h1/span/span[1]")
            return int(span.text)
        except:
            self.errors.append('error/offers-number/not-found')
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
    
    # go to page given by url
    def change_page_to(self,page):
        
        try:
            print('---------------------------------------------')
            print("going to page ",page)
            self.driver.get(page)
            self.driver.implicitly_wait(self.waitingTime)
            
        except:
            self.errors.append('We got blocked in going to page {}'.format(page))
            print(self.errors[-1])
            
    
    def get_article_url(self,article):
        try:
            div = article.find_element(by=By.CLASS_NAME, value = 'ListItem_header__J6xlG')
            a = div.find_element(by=By.TAG_NAME, value='a')
            url = a.get_attribute('href')
            print(url)
            return url
        except:
            return 'error/article/url/not-found'
        
    # get business type from phone number b2b or b2c or unknown by checking the prefix
    def get_business_type(self,phone_number):

        prefixes_b2b = ['4', '5', '1', '2']
        prefixes_b2c = ['6', '9']


        if phone_number.startswith('+'):
            phone_number = phone_number[3:]


        prefix = phone_number[:1]
        if  prefix.startswith('0'):
            prefix = phone_number[1:2]
        if prefix in prefixes_b2b:
            return "b2b"
        elif prefix in prefixes_b2c:
            return "b2c"
        else:
            return "unknown"
    # get phone numbers from info card
    def get_phone_numbers(self,info_card,trys = 0):
        numbers_container = info_card.find_element(by=By.CLASS_NAME,value = "Contact_vendorCta___VygD")
        print('numbers container found')
        numbers_a = numbers_container.find_elements(by=By.TAG_NAME,value='a')
        
        # get numbers href
        numbers = []
        for a in numbers_a:
            num = a.get_attribute('href').replace("tel:", "").strip()
            if num not in numbers:
                numbers.append(num)
        if numbers.__len__() == 0 & trys < 3:
            time.sleep(3)
            return self.get_phone_numbers(info_card,trys+1)
        elif numbers.__len__() == 0:
            print('Error:request to get numbers failed')
            return 'error/product/info-card/numbers/request-failed'
        else:
            return numbers
            
    # get article data
    def get_article_data(self,url):
        try:
            try:
                self.change_page_to(url)
                # title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'StageTitle_boldClassifiedInfo__sQb0l')))
                title_div = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]")
                spans = title_div.find_elements(by=By.TAG_NAME,value='span')
                title = ''
                for span in spans:
                    title += span.text + ' '
                
                
            except Exception as e:
                print('Error:title not found \n',e)
                title = 'error/product/title/not-found'
            print('-- titile : ',title)

            try:
                # title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'StageTitle_boldClassifiedInfo__sQb0l')))
                div = self.driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[2]")
                model = div.text
                
            except Exception as e:
                print('Error:title not found \n',e)
                model = 'error/product/model/not-found'
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
                # click on call button for get numbers
                try:    
                    info_card.find_element(by=By.XPATH,value = '//*[@id="vendor-section-call-button"]').send_keys(Keys.ENTER)
                except:
                    print('Error:Click on btn error \n')
                    vendor_info['numbers'] = 'error/product/info-card/numbers/not-found'
                # get vendor name
                try:
                    vendor_info['name'] = info_card.find_element(by=By.CLASS_NAME,value = "Contact_contactName__ZZISd").text
                    print('vendor name: ',vendor_info['name'])
                except:
                    print('Error:name not found \n')
                    vendor_info['name'] = 'error/product/info-card/name/not-found'
                
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
                    vendor_info['address'] = 'error/product/info-card/address/not-found'
                
                # get vendor company name
                try:
                    vendor_info['company'] = info_card.find_element(by=By.CLASS_NAME,value = "RatingsAndCompanyName_dealer__EaECM").find_element(by=By.TAG_NAME,value='div').text
                    print('vendor company: ',vendor_info['company'])
                except:
                    print('Error:company not found \n')
                    vendor_info['company'] = 'error/product/info-card/company-name/not-found'
                
                # get is vendor pro or not
                try:
                    
                    try:
                        vendor_info['pro'] = info_card.find_element(by=By.CLASS_NAME,value = "VendorData_title__ZcxKQ").find_element(by=By.TAG_NAME,value='span').text == 'Pro'
                    except:
                        vendor_info['pro'] = False
                    print('vendor pro: ',vendor_info['pro'])

                    
                except:
                    print('Error:pro not found \n')
                    vendor_info['pro'] = 'error/product/info-card/pro/not-found' 

                # get vendor numbers after clicking on call button
                try:    
                    print('btn clicked')
                    print('searching for numbers')
                    numbers = self.get_phone_numbers(info_card)
                    types = []
                    for number in numbers:
                        business_type = self.get_business_type(number)
                        print('number : ',number)
                        print('business type : ',business_type)
                        types.append(business_type)
                    
                    if  (self.businessType in ['b2b','b2c']) and (self.businessType not in types):
                        print('business type does not match')
                        return 'skip'
                    print("phone numbers : ",numbers)
                    vendor_info['numbers'] = numbers
                except:
                    print('Error:number not found \n')
                    if self.businessType in ['b2b','b2c']:
                        return 'skip'
                    vendor_info['numbers'] = 'error/product/info-card/numbers/not-found'
                    

            else:
                vendor_info = 'error/product/info-card/not-found'       
            self.driver.implicitly_wait(self.waitingTime)

            return {'title':title,'vendor_info':vendor_info, 'model':model}
        except Exception as e:
            print('**Error** get_article_data nothing found')
            return {"error":'error/article-data/not-found'}

    # get products data
    def format_articles_data(self):
        yield json.dumps({"type":"progress","data":{ 'message':'getting page info'}})
        self.num_of_pages = self.getPageNumber()
        self.num_of_offers = self.getNumOffers()
        print(self.num_of_pages,self.num_of_offers)

        if self.num_of_pages == 0 and self.num_of_offers == 0 :
            my_error = json.dumps({'error':'There is no producats in URL or we got blocked'})
            print('--**--Fatal Error:',my_error)
            yield my_error
            print('this error will stop request')
            return
        
        #  test if startFromPage is greater than number of pages
        if self.startFromPage > self.num_of_pages:
            self.errors.append('Page number ({}) is greater than number of pages, will start from page 1'.format(self.startFromPage))
            print(self.errors[-1])
            self.startFromPage = 1
        
        
        cars_data = []
        pages_urls = []
        self.endPage = self.startFromPage
        while self.endPage <= self.num_of_pages:
            page = self.change_page_number(self.url,self.endPage)
            print('-------------------------------------------------------')
            print(page)
            pages_urls.append(page)
            print('-------------------------------------------------------')
        
            self.change_page_to(page)
            yield json.dumps({"type":"progress","data":{ 'message':'getting products url'}})
            try:
                main = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[5]/div[3]/main")
                # main = self.driver.find_element(by=By.CLASS_NAME, value = 'ListPage_main___0g2X')
                articles = main.find_elements(by=By.TAG_NAME, value = 'article')
                if articles.__len__() == 0:
                    raise Exception('no article found')
            except Exception as e:
                print('*****Error******no article found')
                self.errors.append('No product found in {} page'.format(page))
                print(self.errors[-1])
                continue
            # set articles url table
            articles_url = []
            get_article_data_trys = 0

            # get articles urls
            for article in articles:
                articles_url.append(self.get_article_url(article))
            # print(articles_url)
            yield json.dumps({"type":"progress","data":{ 'message':'getting products info'}})
            for url in articles_url:
                # if (self.offers <= cars_data.__len__()):
                #     continue
                if url == 'error/article/url/not-found':
                    print('product url not found')
                    continue
                article_data = self.get_article_data(url)
                if article_data == 'skip':
                    print('----***----skiped')
                    continue
                try:
                    if article_data.get('error') == 'error/article-data/not-found':
                        
                        if get_article_data_trys < 3:
                            print('retry getting article data')
                            articles_url.append(url)
                        else:
                            print('skip if not get article data failed')
                        get_article_data_trys += 1
                        continue
                    elif article_data.get('error') == None:
                        if article_data.get('vendor_info') == 'error/product/info-card/not-found':
                            if get_article_data_trys < 3:
                                print('retry getting article data')
                                articles_url.append(url)
                            else:
                                print('skip because getting info card failed')
                            get_article_data_trys += 1
                            print('waiting 5 sec')
                            time.sleep(5)
                            continue
                        car = json.dumps({"url":url,"data":article_data})
                        cars_data.append(car)
                        print('-----done with getting  data for url:',url)
                        # time.sleep(2)
                        yield car
                except:
                    print('skip if not get article data failed')
                    continue
            # test if we got the offers user want
            if (self.offers <= cars_data.__len__()):
                break
            
            self.endPage+=1
                
        # -------------------------------------------------------------------
        
        if cars_data.__len__() < self.offers:
            self.errors.append('number of products requested is greater than offers found from page {} to {}'.format(self.startFromPage,self.num_of_pages))
            print(self.errors[-1])
            

        self.driver.quit()         
        returned = json.dumps(
            {
            "type":"result_info",
            "data":{
            "num_of_pages":self.num_of_pages,
            "num_of_offers":self.num_of_offers,
            "start_from_page": self.startFromPage,
            "end_in_page": self.endPage,
            "pages_url":pages_urls,
            "offers_got":cars_data.__len__(), 
            "errors_list":self.errors,
            "offers_user_want":self.offers,
            }
            })
        print('------/return------:\n',returned,'\n------/------')
        yield returned

        return