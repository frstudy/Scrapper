from bs4 import BeautifulSoup as bs
import urllib
import urllib.request
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json
import re

column=['id','name','rating','address','phone','link','category','city']

def soup_maker(url, type='html.parser'):
	'''
	Make a soup from the URL

	Arguemnt:
	url: the page url for which we have to extract the url
	'''
	header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
	req=urllib.request.Request(url, headers=header)
	page=urllib.request.urlopen(req)
	read_page=page.read()
	soup=bs(read_page, type)
	return soup, page

	
def convert_to_text(classname):
	a={
		'icon-acb':'0', #"\9d001",
		'icon-yz':'1', #"\9d002",
		'icon-wx':'2', #"\9d003",
		'icon-vu':'3', #"\9d004",
		'icon-ts':'4', #"\9d005",
		'icon-rq':'5', #"\9d006",
		'icon-po':'6', #"\9d007",
		'icon-nm':'7', #"\9d008",
		'icon-lk':'8', #"\9d009",
		'icon-ji':'9', #"\9d010",
		'icon-dc':'+', #"\9d011",
		'icon-ba':' ', #"\9d012",
		'icon-hg':')', #"\9d013",
		'icon-fe':'(' #"\9d014"
	}
	return a[classname]

def extracting_info_from_soup(soup, category='', city=''):
	df=pd.DataFrame(columns=column)
	rest_name=[] 
	rest_rating=[] 
	rest_add=[] 
	rest_number=[] 
	rest_link =[]
	hashes=[]
	# phone_number=[]
	for i in soup.findAll('li',{'class':'cntanr'}):
		try:
			hashes.append(int(hash(i['data-href']+category)))
			rest_name.append(i.find('span',{'class':'lng_cont_name'}).text) # Restau name
			rest_rating.append(i.find('span',{'class':'exrt_count'}).text) # Rating
			rest_add.append(i.find('span',{'class':'cont_fl_addr'}).text) # Restaurant Address
			rest_link.append(i['data-href'])
			print(i['data-href'])
			rest_number.append(extracting_numbers_from_soup(i['data-href']))
		except Exception as e:
			print('\033[0;31mElement Exception',e,'\033[0;37m')
	df[column[0]]=hashes
	df[column[1]]=rest_name
	df[column[2]]=rest_rating
	df[column[3]]=rest_add
	df[column[4]]=rest_number
	df[column[5]]=rest_link
	df[column[6]]=category
	df[column[7]]=city
	return df


def extracting_numbers_from_soup(link):
	sp, pg=soup_maker(link)
	cipherKey = str(sp.select('style[type="text/css"]')[1])
	keys = re.findall('-(\w+):before', cipherKey, flags=0)
	values = [int(item)-1 for item in re.findall('9d0(\d+)', cipherKey, flags=0)]
	cipherDict = dict(zip(keys,values))
	cipherDict[list(cipherDict.keys())[list(cipherDict.values()).index(10)]] = '+'
	k=sp.find('ul',{'class':'comp-contact'})
	telephoneNumber=''
	for tel in k.findAll('a',{'class':'tel'}):
		ddE = [item['class'][1].replace('icon-','') for item in tel.select('span[class*="icon"]')]
		telephoneNumber+=''.join([str(cipherDict.get(i)) for i in ddE])
		telephoneNumber+=' '
	return telephoneNumber


categories=[
	'Doctors',
	'Chemists',	
	'Grocery',
	'Books ',
	'Repairs',
	'Anything On Hire',
	'Automobile',
	'Real Estate',
	'Order Flowers',
	'Acting Academies',
	'Aerobic Classes',
	'Apparels',
	'Astrology',
	'ATMs',
	'Auditoriums',
	'Banquets',
	'Beauty & Spa',
	'Car Rentals',
	'Cleaning Services',
	'Clubs ',
	'Computers',
	'Consultants',
	'Dance & Music',
	'Dieticians',
	'DTH Services',
	'Education',
	'Electronics',
	'Emergency',
	'Entertainment',
	'Essentials',
	'Exhibition',
	'Fitness',
	'Foreign Exchange',
	'Furniture',
	'Gems & Jewellery',
	'Gifts',
	'Government',
	'Handyman',
	'Hobby Classes',
	'Home',
	'Hospitals',
	'Insurance',
	'Internet & Services',
	'Jobs',
	'Language Classes',
	'Libraries',
	'Loans & Cards',
	'Lodging Services',
	'Mobile Phones',
	'Money Transfer',
	'Motor Training',
	'Nightlife',
	'Optics',
	'Packers & Movers',
	'Party',
	'Passport & Visa Serv',
	'Personal Finance',
	'Pest Control',
	'Petrol Pumps',
	'Photo Studios',
	'Pizza',
	'Resorts',
	'Security',
	'Shopping',
	'Sports Shops', 
	'Sweets Shops', 
	'Tattoo Artists', 
	'Tiffin Services', 
	'Towing', 
	'Travel', 
	'Wedding ', 
	'Yoga Classes'
	]


if __name__ == '__main__':
	# print(
	# extracting_info_from_soup(soup_maker('https://www.justdial.com/Mumbai/Hospital')[0],
	# 	'hopital', 'Mumbai')
	# )

	print(
		extracting_numbers_from_soup('\
		https://www.justdial.com/Mumbai/Gagal-Home-Apartment-Hotel-Near-Brijwasi-Sweet-Kandivali-East/022PXX22-XX22-120120145920-P5T7_BZDET?xid=TXVtYmFpIEhvdGVscw==\
		'))