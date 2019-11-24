import sys 
import vk
import requests
import re
from bs4 import BeautifulSoup

def getToken():
	url = ""
	token = requests.get(url).text
	return token 


def scrap(session):
	# token = "9a33a4b06f9a6fe0d099a339a33f4b0c7f0fb272439a18c730b4568"
	session = vk.Session()
	vkAPI = vk.API(session,scope='users')
	friendIDs = vkAPI.friends.get()

def main(args):
	login = ""
	password = ""
	appID = ""
	# token = getToken()
	session = getAuthSession(login, password, appID)
	scrap(session)


if __name__ == "__main__":
	main(sys.argv)