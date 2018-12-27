import os
import time

try:
	import configration as cfg 
except:
	print('Please run the setup.py before moving on.')
	exit()

try:	
	import libraries, urllib
	import pandas as pd
	from libraries import soup_maker, convert_to_text, extracting_info_from_soup
	from sqlalchemy import create_engine
except:
	os.system('pip install -r requirements.txt')
# Configrations for the script
cities=cfg.cities
engine = create_engine('mysql+pymysql://'+cfg.mysql['user']+':'+cfg.mysql['password']+'@'+cfg.mysql['host']+'/'+cfg.mysql['db'],
					 echo=False
					 )

categories=libraries.categories
category_links=[]

column=['id','name','rating','address','phone','link','category','city']


def justdial():
	if not os.path.exists('logs'):
		os.system('mkdir logs')
	if not os.path.exists('data'):
		os.system('mkdir data')
	for city in cities:
		df=pd.DataFrame(columns=column)
		file_name=city+'.csv'
		log_file=city+str(time.time())+'.txt'
		if os.path.exists('./data/'+file_name):
			os.system('mv ./data/'+file_name+' ./data/'+file_name.split('.')[0]+'_'+str(int(time.time()))+'_old.csv')
		df.to_csv('./data/'+file_name,index=None)
		parent_link='https://www.justdial.com/'+city
		for category in categories:
			link=str(parent_link+'/'+category).replace(' ','%20')
			for page in range(1,100): # Change the range for overall site
				t_link=link+'/page-'+str(page)
				soup, page = soup_maker(t_link)
				if (urllib.parse.urlparse(page.geturl()).query)=='':
					try:
						df=extracting_info_from_soup(soup, category, city)
						df.to_csv('./data/'+file_name, mode='a', index=None, header=None)
						df.to_sql(name='JustDial',
							con=engine,
							# schema='mysql',
							if_exists='append',
							index=False)
						print('\033[0;32m',t_link,' Done!\033[0;37m')
					except Exception as e:
						with open(log_file, 'a') as log:
							log.append(str(time.time)+" Error occurred in {}".format(t_link))
						print('\033[0;37mError in link: \033[1;30;41m',t_link,'\033[0;37m', e)
				else:
					print('Breaks here')
					break


if __name__ == '__main__':
	justdial()