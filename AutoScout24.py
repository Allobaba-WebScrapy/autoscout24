from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
import json
import os
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Debug log path: set AUTOSCOUT24_DEBUG_LOG to enable, or leave unset to disable file logging
_DEBUG_LOG = os.environ.get("AUTOSCOUT24_DEBUG_LOG", "")


def _dbg(loc, msg, data, hid, run_id="run1"):
    if not _DEBUG_LOG:
        return
    try:
        os.makedirs(os.path.dirname(_DEBUG_LOG), exist_ok=True)
        with open(_DEBUG_LOG, "a") as f:
            f.write(
                json.dumps(
                    {
                        "location": loc,
                        "message": msg,
                        "data": data,
                        "timestamp": int(time.time() * 1000),
                        "hypothesisId": hid,
                        "runId": run_id,
                    }
                )
                + "\n"
            )
    except Exception:
        pass

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
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # When running in Docker, use Chromium binary and driver from env
        chrome_bin = os.environ.get("CHROME_BIN")
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if chrome_bin:
            chrome_options.binary_location = chrome_bin
        _dbg("AutoScout24.py:__init__", "before Chrome()", {"url": url}, "B")
        try:
            if chromedriver_path:
                service = Service(executable_path=chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Auto-download ChromeDriver if missing (requires Chrome/Chromium installed)
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                except Exception:
                    # Fallback: let Selenium use its built-in manager (Selenium 4.6+)
                    self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            _dbg("AutoScout24.py:__init__", "Chrome() failed", {"error": str(type(e).__name__), "message": str(e)}, "D")
            msg = str(e).strip()
            raise RuntimeError(
                "Chrome or Chromium is required but not available.\n"
                "  • Install Chrome (https://www.google.com/chrome/) or Chromium, then run again.\n"
                "  • Or run with Docker (no local Chrome needed):\n"
                "    docker build -t autoscout24 . && docker run -p 3000:3000 autoscout24\n"
                "Original error: " + (msg if len(msg) < 200 else msg[:200] + "...")
            ) from e
        _dbg("AutoScout24.py:__init__", "before driver.get", {"url": self.url}, "B")
        self.driver.implicitly_wait(self.waitingTime)
        self.wait = WebDriverWait(self.driver, self.waitingTime)
        parsed = urlparse(self.url)
        self._base_url = f"{parsed.scheme or 'https'}://{parsed.netloc or 'www.autoscout24.fr'}"
        self.driver.get(self.url)

    def _soup(self):
        """Parse current page with BeautifulSoup (resilient to HTML changes)."""
        if not BeautifulSoup:
            return None
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def _parse_listing_page(self):
        """Use BeautifulSoup to get pagination, offer count, and article URLs from current listing page."""
        soup = self._soup()
        if not soup:
            return 0, 0, []
        num_pages = 0
        num_offers = 0
        urls = []

        # Pagination: find buttons/links with page numbers
        for el in soup.select("[class*='pagination'] button, [class*='pagination'] a, nav button, nav a"):
            t = (el.get_text() or "").strip()
            if t.isdigit():
                num_pages = max(num_pages, int(t))
            href = el.get("href") or ""
            m = re.search(r"page=(\d+)", href)
            if m:
                num_pages = max(num_pages, int(m.group(1)))
        if num_pages == 0:
            for el in soup.find_all(class_=re.compile(r"page|pagination", re.I)):
                for b in el.find_all(["button", "a"]):
                    t = (b.get_text() or "").strip()
                    if t.isdigit():
                        num_pages = max(num_pages, int(t))

        # Offer count: header h1 or span with digits
        for el in soup.select("header h1, header h1 span, h1, [class*='ListHeader'] h1, [class*='header'] h1"):
            t = (el.get_text() or "").replace(",", "").replace(".", "")
            m = re.search(r"(\d+)\s*(?:results|offers|angebote|vehicles|résultats|annonces|véhicules)?", t, re.I)
            if m:
                num_offers = int(m.group(1))
                break
        if num_offers == 0:
            for el in soup.find_all(["h1", "span"]):
                t = (el.get_text() or "").strip()
                if re.match(r"^\d[\d,.\s]*$", t) and len(t) < 15:
                    try:
                        num_offers = int(re.sub(r"[\s,.]", "", t))
                        if num_offers > 0 and num_offers < 100000:
                            break
                    except ValueError:
                        pass

        # Article links: main article a[href*='/offers/'] (works for .fr, .de, .com, etc.)
        main = soup.find("main")
        container = main if main else soup
        base = self._base_url
        for a in container.select('a[href*="/offers/"]'):
            href = (a.get("href") or "").strip()
            if not href:
                continue
            if href.startswith("/"):
                href = base.rstrip("/") + href
            if ("autoscout24" in href or "autoscout24" in base) and href not in urls:
                urls.append(href)
        if not urls:
            for art in container.find_all("article"):
                a = art.find("a", href=re.compile(r"/offers/"))
                if a:
                    href = (a.get("href") or "").strip()
                    if "/offers/" not in href:
                        continue
                    if href.startswith("/"):
                        href = base.rstrip("/") + href
                    if href and href not in urls:
                        urls.append(href)

        return num_pages, num_offers, urls

    # get number of pages (uses BS when available, else Selenium fallback)
    def getPageNumber(self):
        if BeautifulSoup:
            num_pages, _, _ = self._parse_listing_page()
            if num_pages > 0:
                return num_pages
        for selector in [
            (By.CSS_SELECTOR, "[class*='pagination'] button"),
            (By.CSS_SELECTOR, "nav [class*='pagination'] a"),
            (By.CLASS_NAME, "pagination-item"),
        ]:
            try:
                self.wait.until(EC.presence_of_element_located(selector))
                els = self.driver.find_elements(by=selector[0], value=selector[1])
                if not els:
                    continue
                nums = []
                for el in els:
                    t = (el.text or el.get_attribute("href") or "").strip()
                    if t.isdigit():
                        nums.append(int(t))
                    if not t and selector[0] == By.CSS_SELECTOR and "a" in selector[1]:
                        m = re.search(r"page=(\d+)", el.get_attribute("href") or "")
                        if m:
                            nums.append(int(m.group(1)))
                if nums:
                    return max(nums)
            except Exception:
                continue
        self.errors.append("error/pages-number/not-found")
        print(self.errors[-1])
        return 0

    # number of offers found (uses BS when available)
    def getNumOffers(self):
        if BeautifulSoup:
            _, num_offers, _ = self._parse_listing_page()
            if num_offers > 0:
                return num_offers
        for selector in [
            (By.CSS_SELECTOR, "header h1"),
            (By.CSS_SELECTOR, "[class*='ListHeader'] h1"),
            (By.CSS_SELECTOR, "h1 span"),
            (By.XPATH, "//header//h1//span[contains(., '')]"),
        ]:
            try:
                els = self.driver.find_elements(by=selector[0], value=selector[1])
                for el in els:
                    t = (el.text or "").replace(",", "").replace(".", "").strip()
                    m = re.search(r"(\d+)\s*(?:results|offers|angebote|vehicles|résultats|annonces|véhicules)?", t, re.I)
                    if m:
                        n = int(m.group(1))
                        if 0 < n < 100000:
                            return n
            except Exception:
                continue
        self.errors.append("error/offers-number/not-found")
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
            
    
    def get_article_url(self, article):
        """Get listing URL from a Selenium WebElement (article)."""
        try:
            a = article.find_element(by=By.CSS_SELECTOR, value='a[href*="/offers/"]')
            url = a.get_attribute("href")
            if url:
                print(url)
                return url
        except Exception:
            pass
        try:
            a = article.find_element(by=By.TAG_NAME, value="a")
            url = a.get_attribute("href")
            if url and "/offers/" in (url or ""):
                return url
        except Exception:
            pass
        return "error/article/url/not-found"
        
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
    # get phone numbers from info card (Selenium WebElement; resilient selectors)
    def get_phone_numbers(self, info_card, trys=0):
        numbers = []
        try:
            numbers_a = info_card.find_elements(by=By.CSS_SELECTOR, value='a[href^="tel:"]')
            for a in numbers_a:
                href = a.get_attribute("href") or ""
                num = href.replace("tel:", "").strip()
                if num and num not in numbers:
                    numbers.append(num)
        except Exception:
            pass
        if not numbers:
            try:
                for container_sel in ["[class*='Contact']", "[class*='vendorCta']", "[class*='Cta']"]:
                    containers = info_card.find_elements(by=By.CSS_SELECTOR, value=container_sel)
                    for c in containers:
                        for a in c.find_elements(by=By.TAG_NAME, value="a"):
                            href = a.get_attribute("href") or ""
                            if href.startswith("tel:"):
                                num = href.replace("tel:", "").strip()
                                if num and num not in numbers:
                                    numbers.append(num)
                    if numbers:
                        break
            except Exception:
                pass
        if numbers:
            print("numbers container found")
        _dbg("AutoScout24.py:get_phone_numbers", "retry check", {"numbers_len": len(numbers), "trys": trys}, "C")
        if len(numbers) == 0 and trys < 3:
            time.sleep(3)
            return self.get_phone_numbers(info_card, trys + 1)
        if len(numbers) == 0:
            print("Error: request to get numbers failed")
            return "error/product/info-card/numbers/request-failed"
        return numbers

    def _parse_detail_bs(self, soup):
        """Parse detail page with BeautifulSoup: title, model, vendor (name, address, company, pro)."""
        title = 'error/product/title/not-found'
        model = 'error/product/model/not-found'
        vendor_info = 'error/product/info-card/not-found'
        main = soup.find("main")
        root = main if main else soup
        for h1 in root.select("h1"):
            t = (h1.get_text() or "").strip()
            if t and len(t) > 3:
                parts = t.split(maxsplit=2)
                if len(parts) >= 2:
                    title = " ".join(parts[:2]) if len(parts) == 2 else t
                    model = parts[-1] if len(parts) > 2 else ""
                else:
                    title = t
                break
        for el in root.select("[class*='Title'] [class*='bold'], [class*='StageTitle']"):
            t = (el.get_text() or "").strip()
            if t and len(t) > 2:
                title = t
                break
        for div in root.select("h1 div, [class*='Title'] div"):
            t = (div.get_text() or "").strip()
            if t and t != title and len(t) < 100:
                model = t
                break
        vendor_block = (
            root.select_one("[class*='VendorData'], [class*='Vendor_main'], [id*='vendor-section']")
            or root.select_one("[class*='Contact_contact'], [class*='Dealer']")
        )
        if vendor_block:
            vendor_info = {}
            name_el = vendor_block.select_one("[class*='contactName'], [class*='Contact_name']")
            vendor_info['name'] = (name_el.get_text() or "").strip() if name_el else 'error/product/info-card/name/not-found'
            addr_el = vendor_block.select_one("a[href*='maps'], a[href*='google'], [class*='Address'], [class*='Department_link']")
            if addr_el:
                vendor_info['address'] = {'url': addr_el.get('href', ''), 'text': (addr_el.get_text() or "").strip()}
            else:
                vendor_info['address'] = 'error/product/info-card/address/not-found'
            company_el = vendor_block.select_one("[class*='dealer__'], [class*='CompanyName'], [class*='RatingsAndCompany'] div")
            vendor_info['company'] = (company_el.get_text() or "").strip() if company_el else 'error/product/info-card/company-name/not-found'
            pro_el = vendor_block.select_one("[class*='VendorData_title'], [class*='Pro']")
            vendor_info['pro'] = (pro_el and (pro_el.get_text() or "").strip() == 'Pro') if pro_el else False
            vendor_info['numbers'] = []
        return title, model, vendor_info

    # get article data (BeautifulSoup for parsing + Selenium for click-to-reveal numbers)
    def get_article_data(self, url):
        try:
            self.change_page_to(url)
            title = 'error/product/title/not-found'
            model = 'error/product/model/not-found'
            vendor_info = 'error/product/info-card/not-found'

            if BeautifulSoup:
                soup = self._soup()
                if soup:
                    title, model, vendor_info = self._parse_detail_bs(soup)
            if title == 'error/product/title/not-found' or (not BeautifulSoup):
                try:
                    title_div = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]")
                    title = " ".join(s.text for s in title_div.find_elements(by=By.TAG_NAME, value='span'))
                except Exception:
                    pass
            if model == 'error/product/model/not-found' or (not BeautifulSoup):
                try:
                    div = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[2]")
                    model = div.text
                except Exception:
                    pass

            print('-- title:', title, '-- model:', model)

            info_card = None
            for sel in [
                (By.CSS_SELECTOR, "[class*='VendorData_main'], [class*='Vendor_mainContainer']"),
                (By.CSS_SELECTOR, "[id*='vendor-section']"),
                (By.CSS_SELECTOR, "[class*='Vendor_main'], [class*='VendorData']"),
                (By.CSS_SELECTOR, "[class*='Contact_contact'], [class*='Dealer']"),
                (By.XPATH, "//*[contains(@class,'Vendor') or contains(@class,'Contact')]"),
            ]:
                try:
                    info_card = self.driver.find_element(by=sel[0], value=sel[1])
                    break
                except Exception:
                    continue
            if info_card and isinstance(vendor_info, dict):
                self.driver.implicitly_wait(0)
                try:
                    call_btn = info_card.find_element(by=By.XPATH, value='.//*[@id="vendor-section-call-button"]')
                    call_btn.send_keys(Keys.ENTER)
                except Exception:
                    try:
                        call_btn = info_card.find_element(by=By.LINK_TEXT, value="Call")
                        call_btn.click()
                    except Exception:
                        try:
                            self.driver.find_element(by=By.CSS_SELECTOR, value='a[href^="tel:"]').click()
                        except Exception:
                            pass
                time.sleep(1)
                try:
                    numbers = self.get_phone_numbers(info_card)
                    if isinstance(numbers, list):
                        types = [self.get_business_type(n) for n in numbers]
                        if (self.businessType in ['b2b', 'b2c']) and (self.businessType not in types):
                            return 'skip'
                        vendor_info['numbers'] = numbers
                    else:
                        vendor_info['numbers'] = numbers
                except Exception:
                    vendor_info['numbers'] = 'error/product/info-card/numbers/not-found'
                self.driver.implicitly_wait(self.waitingTime)
            elif not isinstance(vendor_info, dict):
                vendor_info = 'error/product/info-card/not-found'

            return {'title': title, 'vendor_info': vendor_info, 'model': model}
        except Exception as e:
            print('**Error** get_article_data', e)
            return {"error": 'error/article-data/not-found'}

    # get products data
    def format_articles_data(self):
        yield json.dumps({"type":"progress","data":{ 'message':'getting page info'}})
        self.num_of_pages = self.getPageNumber()
        self.num_of_offers = self.getNumOffers()
        # #region agent log
        _dbg('AutoScout24.py:format_articles_data', 'after getPageNumber getNumOffers', {'num_of_pages': self.num_of_pages, 'num_of_offers': self.num_of_offers}, 'E')
        # #endregion
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
        consecutive_no_articles = 0
        max_consecutive_failures = 3  # stop after 3 pages with no articles to avoid 200-page loop
        while self.endPage <= self.num_of_pages:
            page = self.change_page_number(self.url, self.endPage)
            print('-------------------------------------------------------')
            print(page)
            pages_urls.append(page)
            print('-------------------------------------------------------')

            self.change_page_to(page)
            yield json.dumps({"type": "progress", "data": {"message": "getting products url", "page": self.endPage, "total_pages": self.num_of_pages}})
            articles_url = []
            if BeautifulSoup:
                _, _, articles_url = self._parse_listing_page()
            if not articles_url:
                try:
                    try:
                        main = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[5]/div[3]/main")
                    except Exception:
                        main = self.driver.find_element(By.TAG_NAME, "main")
                    articles = main.find_elements(by=By.TAG_NAME, value='article')
                    if not articles:
                        raise Exception('no article found')
                    consecutive_no_articles = 0
                    for article in articles:
                        articles_url.append(self.get_article_url(article))
                except Exception as e:
                    print('*****Error******no article found', e)
                    self.errors.append('No product found in {} page'.format(page))
                    consecutive_no_articles += 1
                    if consecutive_no_articles >= max_consecutive_failures:
                        self.errors.append('Stopped after {} pages with no articles (site structure may have changed)'.format(max_consecutive_failures))
                        break
                    continue
            else:
                consecutive_no_articles = 0
            get_article_data_trys = 0
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