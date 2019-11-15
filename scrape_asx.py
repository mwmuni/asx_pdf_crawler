import urllib.request
import requests
import re
from typing import List
import os
from dateutil.parser import parse
import calendar
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from functools import partial

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
    # print(pdf_suffix)
    r = requests.get("{}{}".format(prefix, pdf_suffix))
    with open("pdfs/{}/{}.pdf".format(code, calendar.timegm(parse(r.headers['Last-Modified']).timetuple())), "wb") as f:
        f.write(r.content)
    print("{}/{}".format(code, calendar.timegm(parse(r.headers['Last-Modified']).timetuple())))
    _fp.close()

if __name__ == "__main__":
    for code in stock_codes:
        if not os.path.exists("pdfs/{}".format(code)):
            os.mkdir("pdfs/{}".format(code))
        fp = urllib.request.urlopen("https://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode={}&timeframe=D&period=M3".format(code))
        mybytes = fp.read()

        mystr = str(mybytes)#mybytes.decode("latin")
        id_loc: List[int] = [s.end()+1 for s in re.finditer(str_find, mystr)]
        id_val: List[str] = [mystr[loc:loc+8] for loc in id_loc]

        fp.close()

        with Pool(64) as p:
            p.map(partial(download_save, code=code), id_val)

    # print(mystr)
    # print(id_loc)
    # print(id_val)