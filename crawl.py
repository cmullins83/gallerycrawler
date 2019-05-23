from lxml import html
import requests
import urllib.request
import os

baseurl = "https://rule34.paheal.net"
#TODO: We need to find a way to navigate to the next page
search = input("Search for:")
directory = './' + search + '/'
try:
	os.mkdir(directory)
except:
	print(directory, " already exists...continuing...")
url = 'https://rule34.paheal.net/post/list/'+search+'/1'
page = requests.get(url)
tree = html.fromstring(page.content)
title = tree.xpath('/html/head/title/text()')

print('Page title: ',title[0])

image = tree.xpath("//a[contains(@class, 'shm-thumb-link')]/@href")
for link in image:
	try:
		imagepage = requests.get(baseurl+link)
	except:
		print("Failure in imagepage. Contents: ", imagepage)
	try:
		imagetree = html.fromstring(imagepage.content)
	except:
		print("Failure in imagetree. Contents: ", imagetree)
	try:
		name = imagetree.xpath('/html/head/title')
	except:
		print("Failure in name. Contents: ", name)
	#Hmmm...seems we have a duplicate...might need to play with this and see which is working
	try:
		name = imagetree.findtext('.//title')
	except:
		print("Failure in name. Contents: ", name)
	try:
		imageurl = imagetree.xpath('//*[@id="main_image"]/@src')
	except:
		print("Failure in imageurl. Contents: ", imageurl)
	try:
		extension = imageurl[0][-4:]
	except:
		print("Failure in extension. Contents: ", extension)
	try:
		download = imageurl[0]
	except:
		print("Failure in download. Contents: ", download)
	try:
		urllib.request.urlretrieve(download, directory + name + extension)
		print("Downloading: ",name)
	except:
		print("Couldn't download " + name + ". Skipping...")
