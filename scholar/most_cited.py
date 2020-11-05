import requests as req
from bs4 import BeautifulSoup as soup

keyword = "psychology"
since = 2010 # start year
pages = 15 # pages searching through
top_x = 5 # top __ pages you wish to see

pages_f = [n*10 for n in range(pages)] # formatting articles by every 10
articles = [] 
count = 0 # counting first 10 sufficient articles

for page in pages_f:
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
	url = "https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,33&as_ylo={}&as_yhi=2020".format(str(page), keyword, str(since))

	response = req.get(url, headers=headers)
	resp_parsed = soup(response.content,'lxml')

	if "Our systems have detected unusual traffic from your computer network." in resp_parsed.text: # checking for IP block
		print('! IP Blocked !')
	else:
		pass

	for article in resp_parsed.select('[data-rp]'): # initializing socket connection
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
				
				if count <= top_x: # after we have our top 10, the point of reference will be the lowest # of citations in the list
					articles.append([title, cites, link])
					articles.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
				else:
					if cites > articles[-1][1]:
						articles[-1][1] = cites
						articles.sort(key=lambda e: e[1], reverse=True) # sorting by # of citations
						print('\n--- constructing top {} most cited articles\n'.format(str(top_x)))
						continue
					else:
						continue		

		except Exception as e: 
			pass

if __name__ == "__main__":
	print("\n\n Keyword: {}\t\tSince: {}\t\tArticles Analyzed: {}\n\n".format(keyword, str(since), str(pages)))
	for a in articles:
		print("\n TITLE: {}\n\n CITES: {}\n\n URL: {}".format(a[0], a[1], a[2]), end='\n-----------------------------------------\n')

		
