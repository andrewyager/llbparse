import csv
import requests
import sys
import os

images = {}
categorylist = []

with open('output/scrape.csv', "r") as csvfile:
	csvread = csv.reader(csvfile, delimiter=',')
	for row in csvread:
		images[row[0]]=row[1]

try:
	os.mkdir('output/images')
except FileExistsError:
	pass

for barcode in images:
	try:
		os.mkdir('output/images/{}'.format(barcode[0:5]))
	except FileExistsError:
		pass
	try:
		filename = 'output/images/{}/{}.jpg'.format(barcode[0:5], barcode)
		if not os.path.exists(filename):
			r = requests.get(images[barcode])
			print("Writing {}".format(filename))
			with open(filename, "wb") as file:
				file.write(r.content)
	except requests.exceptions.MissingSchema:
		pass