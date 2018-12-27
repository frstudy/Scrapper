from bs4 import BeautifulSoup as bs
import urllib
import urllib.request
import pandas as pd
import pymysql
from sqlalchemy import create_engine

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
	for i in soup.findAll('li',{'class':'cntanr'}):
		try:
			hashes.append(str(hash(i['data-href']+category)))
			rest_name.append(i.find('span',{'class':'lng_cont_name'}).text) # Restau name
			rest_rating.append(i.find('span',{'class':'exrt_count'}).text) # Rating
			rest_add.append(i.find('span',{'class':'cont_fl_addr'}).text) # Restaurant Address
			number=''
			for char_k in i.find('p',{'class':'contact-info '}).findAll('span',{'class':'mobilesv'}):
				number=number+convert_to_text(char_k['class'][1])
			number=number.split(')')[-1]
			rest_number.append(number)
			rest_link.append(i['data-href'])
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
	# print(df)
	return df

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