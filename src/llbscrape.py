import requests
import urllib.request
import time
import pprint
import re
import sys
import csv
from bs4 import BeautifulSoup

images = {}
categorylist = []

with open('output/scrape.csv', "r") as csvfile:
	csvread = csv.reader(csvfile, delimiter=',')
	for row in csvread:
		images[row[0]]=row[1]

file = open("output/scrape.csv", "a")
errorfile = open("output/errors", "a")

def parseproduct(url):
	print('parsing url {}'.format(url))
	urlre = r'barcode=(\d+|CIR\d+)'
	matches = re.search(urlre, url)
	if matches is None:
		errorfile.write(str(url) + "\n")
		errorfile.flush()
		return False
	barcode = matches[1]
	if barcode in images:
		return False
	image = None
	if url[0]=='/':
		url = base_url + url[1:]
	response = requests.get(url)
	page_soup = BeautifulSoup(response.text, "html.parser")
	link_tags = page_soup.findAll('a')
	for link_tag in link_tags:
		try:
			if link_tag['data-target'] == '#lightbox':
				image = link_tag['data-image_url']
		except KeyError:
			pass
	images[barcode] = image
	file.write("{},{}\n".format(barcode,image))
	file.flush()

def parsecategory(url):
	print('parsing category url {}'.format(url))
	if url[0]=='/':
		url = base_url + url[1:]
	if url in categorylist:
		return True
	categorylist.append(url)
	if url.find('?') != -1:
		response = requests.get(url+"&per_page_size=200")
	else:
		response = requests.get(url+"?per_page_size=200")
	page_soup = BeautifulSoup(response.text, "html.parser")
	link_tags = page_soup.findAll('a')
	for link_tag in link_tags:
		try:
			if link_tag['href'].find('/p/') != -1:
				parseproduct(link_tag['href'])
			if link_tag['href'].find('/c/') != -1:
				parsecategory(link_tag['href'])
		except KeyError:
			pass

base_url = 'https://www.littlelostbookshop.com.au/'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.findAll('a')
for link in links:
	try:
		if link['href'].find('/p/') != -1:
			parseproduct(link['href'])
		if link['href'].find('/c/') != -1:
			parsecategory(link['href'])
	except KeyError:
		pass

file.close()
errorfile.close()