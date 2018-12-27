import time
import os
from subprocess import DEVNULL, STDOUT, check_call
try:
	import mysql.connector
	from mysql.connector import errorcode
	from sqlalchemy import create_engine
except:
	os.system('pip install -r requirements.txt')

user_name=input('Please enter your MySql username: ')
user_psd=input('Please enter your MySql password: ')

a="mysql = {'host': 'localhost:3306',"
if user_name=='':
	 a+="'user': 'root',"
else:
	a+="'user': '"+user_name+"', "
if user_psd=='':
	a+="'password': 'root',"
else:
 	a+="'password': '"+user_psd+"', "
a+=" 'db': 'justdial','table': 'JustDial'}"

b="""
cities=[
	'Mumbai', 
	]
"""

print('Writing to file...')

with open('configration.py','w') as f:
	f.write(a)
with open('configration.py','a') as f:
	f.write(b)
time.sleep(0.5)

try:
	os.system('mysql -u'+user_name+' -p'+user_psd+'< creation.sql')
	print('''
		All done! You may now use the packages.
		''')
except Exception as e:
	os.system('rm ./configration.py')
	print("Error ",e,".\nPlease run the setup again!")