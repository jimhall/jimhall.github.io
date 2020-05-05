from urllib.request import urlopen
from html.parser import HTMLParser
from datetime import datetime
import os
import glob
import sys

# Source: https://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def missing_dirs(typedir):
    geturl = baseurl + typedir + '/' + typedir + 'cloud.html'
    html = urlopen(geturl)
    rawcats = html.read().decode(encoding)
    plaintext = strip_tags(rawcats)

    #https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
    # Or Learning Python ch03 p66
    catset = set(plaintext.split())
    dir_contents = set(os.listdir(typedir))
    os.chdir(typedir)
    md_files = set(glob.glob('*.md'))
    os.chdir('..')
    existing_dirs = dir_contents.difference(md_files)
    create_dirs = catset.difference(existing_dirs)
    return create_dirs

#https://realpython.com/python-command-line-arguments/
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
baseurl = 'https://jimhall.github.io/TestBlog4/'
encoding = 'utf-8'
catindexmd = '''---
layout: categories
'''

tagindexmd = '''---
layout: tags
'''
tmpfile='/tmp/newcatortag.txt'

if __name__ == "__main__":
    with open(tmpfile, 'wt') as sout:
        sout.write('0\n')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if "-c" in opts: # categories print("Adding new categories directories if necessary")
        typedir = 'categories'
        print("Adding new categories directories if necessary")
        print('RUN = ' + dt_string + ' ' + typedir + '\n')
    elif "-t" in opts: # tags
        typedir = 'tags'
        print("Adding new tags directories if necessary")
        print('RUN = ' + dt_string + ' ' +  typedir + '\n')
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} (-c | -t ) <arguments>...")

# Simple logic if there are no new dirs to create
# https://stackoverflow.com/questions/29064227/how-can-i-test-to-see-if-a-defaultdictset-is-empty-in-python
    create_dirs = missing_dirs(typedir)
    if not create_dirs:
        # Preferred way to exit:
        # https://stackoverflow.com/questions/73663/how-to-terminate-a-python-script
        print('No new ' + typedir + ' directories to create')
        sys.exit()
    else:
        print('TYPEDIR\tNAME')
        with open(tmpfile, 'wt') as sout:
            sout.write('1\n')

    for dir in create_dirs:
        basedir = typedir + '/' + dir
        indexmd = basedir + '/index.md'
        print(typedir + '\t' + dir)
        os.mkdir(basedir)
        with open(indexmd, 'wt') as fout:
            if typedir == 'categories':
                fout.write(catindexmd)
            if typedir == 'tags':
                fout.write(tagindexmd)
            fout.write('title: ' + dir + '\n')
            fout.write('---\n')
