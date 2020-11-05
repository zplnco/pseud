import requests as req
from bs4 import BeautifulSoup as soup
from scraper_api import ScraperAPIClient
from concurrent.futures import ThreadPoolExecutor

keyword = "psychology"
since = 2010 # start year
pages = 2 # pages searching through
top_x = 3 # top __ pages you wish to see

class Google_Scholar_Bot:

	def __init__(self, keyword, start_year, total_pages, top_x):
		self.keyword = keyword
		self.since = start_year
		self.pages = total_pages
		self.top_x = top_x

	def Get_Article_Data(self, page, keyword, since):
		
		url = "https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,33&as_ylo={}&as_yhi=2020".format(str(page), self.keyword, str(self.since))

		client = ScraperAPIClient('bb129ca384c265942abc9af857eb1471')
		response = client.get(url, timeout=60) 
		resp_parsed = soup(response.content,'lxml')

		if "Our systems have detected unusual traffic from your computer network." in resp_parsed.text: # checking for IP block
			return '! IP Blocked !'
		elif resp_parsed.status_code == 403:
			return'! exceeded avaliable API calls !'
		elif resp_parsed.status_code == 429:
			return '! exceeded concurrent-connections limit !' # slow down request rate
		elif resp_parsed.status_code == 500:
			return '! request failed !'
		else:
			pass

		return resp_parsed


	def Analyze_Data(self, keyword, since, top_x):

		pages_f = [n*10 for n in range(pages)] # formatting articles by every 10
		articles = [] 
		count = 0 # counting first 10 sufficient articles

		for page in pages_f:
			for article in self.Get_Article_Data(page, self.keyword, self.since).select('[data-rp]'): # initializing socket connection
				try:
					title = article.select('h3')[0].text
					if 'BOOK' in title.split()[0] or 'CITATION' in title.split()[0]:
						continue
					else:
						count += 1
						print('\n--- retrieving article data ---\n')

						cites_sloppy = [a.contents for a in article.select('a') if 'cites' in a.get('href')]
						cites = int(cites_sloppy[0][0].split()[-1]) # only grabbing the # of cites
						link = article.select('a')[0].get('href')
						
						if count <= self.top_x: # after we have our top 10, the point of reference will be the lowest # of citations in the list
							articles.append([title, cites, link, int(page/10)+1])
							articles.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
						else:
							if cites > articles[-1][1]:
								articles[-1][1] = cites
								articles.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
								print('\n--- constructing top {} most cited articles\n'.format(str(self.top_x)))
								continue
							else:
								continue		

				except Exception as e: 
					pass

		return articles

	def Output(self, keyword, since, pages):
		
		articles = self.Analyze_Data(self.keyword, self.since, self.top_x)
		print("\n\n Keyword: {}\t\tSince: {}\t\tArticles Analyzed: {}\n\n".format(self.keyword, str(self.since), str(self.pages*10)))
		for a in articles:
			print("\n TITLE: {}\n\n CITES: {}\n\n URL: {}\n\n PAGE: {}".format(a[0], a[1], a[2], a[3]), end='\n-----------------------------------------\n')

	# def run_script(self):
 #        with ThreadPoolExecutor(max_workers=min(len(self.urls),self.max_threads)) as Executor:
 #            jobs = [Executor.submit(self.wrapper, u) for u in self.urls]


if __name__ == "__main__":
	gs_bot = Google_Scholar_Bot(keyword, since, pages, top_x)
	run = gs_bot.Output(keyword, since, pages)
	
