from concurrent.futures import ThreadPoolExecutor
from scraper_api import ScraperAPIClient
import requests as req
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Analyze Google Scholar by Keyword')
parser.add_argument(
    '--keyword',
    type=str,
    help='keyword to search against'
    )
parser.add_argument(
    '--start',
    type=str,
    default="2010",
    help='start year in format "YYYY", default "2010"'
    )
parser.add_argument(
    '--pages',
    type=int,
    default=200,
    help='number of pages to search, default "200'
    )
parser.add_argument(
    '--top',
    type=int,
    default=10,
    help='number of results to return, default "10"'
    )
parser.add_argument(
    '--threads',
    type=int,
    default=5,
    help='number of threads to run, default "5"'
    )
args = parser.parse_args()
keyword = args.keyword
since = args.start
pages = args.pages
top_x = args.top
threads = args.threads

class GoogleScholarBot:

    def __init__(self, url_list, threads, top_x):

        self.urls = url_list
        self.results = []
        self.threads = threads
        self.top_x = top_x
        # making counting variables self-variables, so they can be accessed from multiple threads
        self.count_v_a = [] 
        self.a_count = [] 
        self.p_count = []
       
    def make_request(self, url):
        try:
            client = ScraperAPIClient('bb129ca384c265942abc9af857eb1471') # making request throuhg Scraper API
            r = client.get(url=url, timeout=60) 
        except Exception as e:
            print(e)
        return r.content

    def parse_results(self, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            for article in soup.select('[data-rp]'): # initializing socket connection
                try:
                    title = article.select('h3')[0].text
                    if 'BOOK' in title.split()[0] or 'CITATION' in title.split()[0]: # making sure article is valid
                        continue
                    else:
                        self.count_v_a += 1 # everytime a sufficient article is found

                        print('\n--- retrieving article data ---\n')

                        cites_sloppy = [a.contents for a in article.select('a') if 'cites' in a.get('href')]
                        cites = int(cites_sloppy[0][0].split()[-1]) # only grabbing the # of cites
                        link = article.select('a')[0].get('href')

                        if self.count_v_a <= self.top_x: # after we have our top 10, the point of reference will be the lowest # of citations in the list
                            self.results.append([title, cites, link])
                            self.results.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
                        else:
                            if cites > self.results[-1][1]:
                                self.results[-1][1] = cites
                                self.results.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
                                print('\n--- constructing top {} most cited articles\n'.format(str(self.top_x)))
                                continue
                            else:
                                continue        
            
                except Exception as e: 
                    pass
        except Exception as e:
            print(e)

    def wrapper(self, url):
        html = self.make_request(url)
        self.parse_results(html)
 
    def run_script(self):
        self.count_v_a = 0 # counting valid article
        with ThreadPoolExecutor(max_workers=self.threads) as Executor:
            execute = [Executor.submit(self.wrapper, u) for u in self.urls]


if __name__ == '__main__':

    # keyword = "psychology"
    # since = 2010 # start year
    # pages = 200 # pages searching through
    # threads = 5 # max for free trial
    # top_x = 10 # top __ results you wish to return

    pages_f = [n*10 for n in range(pages)] # formatting articles by every 10
    urls  = ["https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,33&as_ylo={}&as_yhi=2020".format(str(page), keyword, str(since)) for page in pages_f]
    gs_bot = GoogleScholarBot(urls, threads, top_x)
    gs_bot.run_script()
    print("\n\n Keyword: {}\t\tSince: {}\t\tArticles Analyzed: {}\n\n".format(keyword, str(since), str(pages*10)))
    for a in gs_bot.results:
        print("\n TITLE: {}\n\n CITES: {}\n\n URL: {}".format(a[0], a[1], a[2]), end='\n\n-----------------------------------------\n')
