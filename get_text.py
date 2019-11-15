import os
import fitz
from typing import List



in_folder = 'pdfs/'
out_folder = 'out/'
stocks = os.listdir(in_folder)

page_text: str = ''

for s in stocks:
    if not os.path.exists('{}{}/'.format(out_folder, s)):
        os.mkdir('{}{}/'.format(out_folder, s))

for s in stocks:
    files = os.listdir('{}{}/'.format(in_folder, s))
    for f in files:
        _f = f.split('.')[0]
        doc = fitz.open('{}{}/{}.pdf'.format(in_folder, s, _f))
        for p in range(doc.pageCount):
            page = doc.loadPage(p)
            page_text += page.getText().encode('ascii', 'ignore').decode('utf-8')
        with open('{}{}/{}.txt'.format(out_folder, s, _f), 'w') as o:
            o.write(page_text)
        # print(''.join(page_text))
