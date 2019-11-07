import requests
from bs4 import BeautifulSoup


def getAllLinks(html):
	soup = BeautifulSoup(html, 'lxml')
	tds = soup.find('table', id = 'currencies').find_all('td',class_='currency-name')
	links = [td.find('a').get('href') for td in tds]
	return links

def getHtml(url):
	response = requests.get(url)
	return response.text


def main():
	url = 'https://coinmarketcap.com/'
	html = getHtml(url)
	allLinks = getAllLinks(html)
	print(allLinks)
	return 0

if __name__ == "__main__":
	main()