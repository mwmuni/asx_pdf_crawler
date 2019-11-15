from os import mkdir, listdir
from os.path import exists
from fitz import open as fitz_open
from typing import List
from multiprocessing import Pool



in_folder = 'pdfs/'
out_folder = 'out/'

if not exists(in_folder):
    print("Input folder does not exist!")
    exit(1)
stocks = listdir(in_folder)

if not exists(out_folder):
    mkdir(out_folder)

for s in stocks:
    if not exists('{}{}/'.format(out_folder, s)):
        mkdir('{}{}/'.format(out_folder, s))

def process(s):
    files = listdir('{}{}/'.format(in_folder, s))
    for f in files:
        _f = f.split('.')[0]
        doc = fitz_open('{}{}/{}.pdf'.format(in_folder, s, _f))
        page_text: str = ''
        for p in range(doc.pageCount):
            page = doc.loadPage(p)
            page_text += page.getText().encode('ascii', 'ignore').decode('utf-8')
        with open('{}{}/{}.txt'.format(out_folder, s, _f), 'w') as o:
            o.write(page_text)

if __name__ == '__main__':
    with Pool() as p:
        p.map(process, stocks)

