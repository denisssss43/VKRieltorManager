"""Либа для поиска и парса поста"""

import requests
from bs4 import BeautifulSoup
import re 
import uuid
from datetime import datetime, timedelta
import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import ast 
import copy 





if __name__ == "__main__":
	while(True):
		try:
			print (datetime.datetime.now(), 'Connect')
			db.Connect()

			for i in range(3):
				db.SearchFromGroupWithoutAddress(g_id='123114913', g_title='', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='105543780', g_title='', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='', g_title='arendav24', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='', g_title='arenda.v.krasnoyarske', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='76867861', g_title='', offset=i*10, country='Россия', city='Красноярск') 
				db.SearchFromGroupWithoutAddress(g_id='80318218', g_title='', offset=i*10, country='Россия', city='Красноярск')

			db.CloseConnect()
			print ('	CloseConnect')
		except: pass
    
    pass