import sys
import os
import re
from bs4 import BeautifulSoup


def initParser():
# -m month
# -d directory (if you want to scrap few months)
# -fl path to friend list file 
	pass


def getFiles(directory):
	for file in os.listdir("/mydir"):
	if file.endswith(".txt"):
		print(os.path.join("/mydir", file))

def getFriendlist(file):
	soup = BeautifulSoup(file,"html.parser")
	friends = soup.findAll("div", {"class": "friends_user_row clear_fix"})
	for fr in friends:
		name = None
		id_ = None
		href = None
		# check_param
	pass

def saveResult(result):
	pass


def main(args):
	workDir = args[1]
	files = getFiles(workDir)
	friendList = getFriendList(workDir)
	result = scrapBirthDays(files, friendList)
	saveResult(result)

if __name__ == "__main__":
	main(sys.argv)