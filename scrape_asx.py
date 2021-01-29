# import urllib.request
# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import By
import yaml
import re
from typing import List
import os
from dateutil.parser import parse
import calendar
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from functools import partial
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

prefix = "https://www.asx.com.au"
suffix = "/asx/statistics/displayAnnouncement.do?display=pdf&idsId="
str_find = "idsId"

stock_codes = ["CBA"]

start_str = "asxpdf"
end_str = ".pdf"

def download_save(_id, code):
    _fp = urllib.request.urlopen('{}{}{}'.format(prefix, suffix, _id))
    mybytes = _fp.read()
    mystr = str(mybytes)
    start = mystr.find(start_str) - 1
    end = mystr.find(end_str) + len(end_str)
    pdf_suffix = mystr[start:end]
    r = requests.get("{}{}".format(prefix, pdf_suffix))
    with open("pdfs/{}/{}.pdf".format(code, calendar.timegm(parse(r.headers['Last-Modified']).timetuple())), "wb") as f:
        f.write(r.content)
    print("{}/{}".format(code, calendar.timegm(parse(r.headers['Last-Modified']).timetuple())))
    _fp.close()

def get_num_ele(_element):
    result = _element.find_elements_by_xpath("//tr")
    # print(len(result))
    return len(result) > 4 # 4 is the base number of tr elements before table is loaded

def remove_class(driver, classname):
    driver.execute_script(f"""
            var element = document.querySelector("{classname}");
            if (element)
                element.parentNode.removeChild(element);
            """) 

if __name__ == "__main__":
    if not os.path.exists("pdfs"):
        os.mkdir("pdfs")
    for code in stock_codes:
        if not os.path.exists("pdfs/{}".format(code)):
            os.mkdir("pdfs/{}".format(code))
        # fp = urllib.request.urlopen("https://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode={}&timeframe=D&period=M3".format(code))
        # fp = urllib.request.urlopen(f"https://www2.asx.com.au/markets/trade-our-cash-market/announcements.{code.lower()}")
        # mybytes = fp.read()
        url = f"https://www2.asx.com.au/markets/trade-our-cash-market/announcements.{code.lower()}"
        # fp = requests.get(url)
        
        browser.get(url)
        # browser.find_element_by_class_name("sr-only")
        element = WebDriverWait(browser, 10).until(
            get_num_ele)
        
        # Remove the dark filter that covers the table so links can be clicked
        remove_class(browser, ".onetrust-pc-dark-filter")
        remove_class(browser, ".ot-fade-in")

        scraped_data = {}
        for ele in browser.find_elements_by_xpath("//a"):
            href = ele.get_attribute('href')
            if href and href.startswith('https://cdn-api.markitdigital.com'):
                row = ele.find_element_by_xpath("./../..")
                aria = row.find_elements_by_xpath(".//a")
                print([a.text for a in aria])
                for a in aria:
                    try:
                        if a.text.startswith('and '):
                                print(a.text)
                                a.click()
                    except Exception as e:
                        print(e)
                        pass
                # print(repr(row.text))
                print(row.text)
                rd = row.text.split("\n")
                '''
                    rd information:
                        rd stands for 'row_data'
                        rd[0]: date published (can be 'Today' and 'Yesterday')
                        rd[1]: time published (shown twice, separated by a space)
                        rd[2+]: Company Codes
                        rd[company_codes+3]: Company name of company in rd[2]
                        rd[company_codes+4]: Duplicate of previous
                        yn = 2 + company_codes + 2
                        rd[yn]: Price sensitive announcement
                        rd[yn+1]: PDF title
                        rd[yn+2]:

                '''
                yn = rd.index('yes') if 'yes' in rd else rd.index('no')

                rd = [rd[0], rd[1].split(' ')[0], rd[2], rd[3], rd[4], rd[7], rd[9]]
                exit()
                # print([r.text for r in row.find_elements_by_xpath("//td")])
                # exit()
                
            # print(ele.get_attribute('href'))
        
        # print()
        # exit()
        # element = browser.find_element_by_xpath("//tbody")

        print(element.text)
        href = element.find_elements_by_xpath(xpath)
        print(href)
        # 'data-v-4784e3fa'
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        result = soup.findAll('sr-only')
        print(result)
        # print(result[0])
        # result = [r for r in result if 'href' in r and r['href'].startswith('https://')]
        # print(result)
        

        # mystr = str(mybytes)
        # id_loc: List[int] = [s.end()+1 for s in re.finditer(str_find, mystr)]
        # id_val: List[str] = [mystr[loc:loc+8] for loc in id_loc]

        # fp.close()

        # with ThreadPool(64) as p:
        #     p.map(partial(download_save, code=code), id_val)
