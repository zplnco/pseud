import requests as req
from bs4 import BeautifulSoup as soup

keyword = "psychology"
since = 2010
# pages = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200] # e.g. 30 = page 3
pages = [0]

articles = []

for page in pages:
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
	url = "https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,33&as_ylo={}&as_yhi=2020".format(str(page), keyword, str(since))

	response = req.get(url, headers=headers)
	resp_parsed = soup(response.content,'lxml')

	if "Our systems have detected unusual traffic from your computer network." in resp_parsed.text: # checking for IP block
		print('! IP Blocked !')

	basis = [] # setting a basis to compare other citation quantities to
	count = 0 # counting first 10 articles

	for article in resp_parsed.select('[data-rp]'): # initializing socket connection
		try:
			title = article.select('h3')[0].text
			if 'BOOK' in title.split()[0] or 'CITATION' in title.split()[0]:
				continue
			else:
				count += 1
				cites_sloppy = [a.contents for a in article.select('a') if 'cites' in a.get('href')]
				cites = cites_sloppy[0][0].split()[-1] # only grabbing the # of cites
				link = article.select('a')[0].get('href')

				basis.append([title,cites])
				basis.sort()

				if count >= 10:


				
				print("\n TITLE: {}\n\n CITES: {}\n\n URL: {}".format(title, cites, link), end='\n-----------------------------------------\n')
			
		except Exception as e: 
			print(e)
		


if __name__ == "__main__":
	for a in articles:
		print(a, end='\n\n')
