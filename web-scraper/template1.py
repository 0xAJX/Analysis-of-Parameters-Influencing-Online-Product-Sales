#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:40:49 2018

@author: deepanshu
"""

import requests 
import bs4
res = requests.get('https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=books')
soup = bs4.BeautifulSoup(res.text, 'lxml')

#for link in soup.select('.a-text-normal'):
#next_page = soup.find('span',{'class':'pagnRA'})
#print(next_page.a['href'])
#    print(link.text)

# containers = list of books 
containers = soup.find_all('li', 's-result-item')

# container = each book from the list 
for container in containers:
    try:
        print(container.a['href'])
    except:
        pass
#print(containers.find('li',{'li':'result_1'}))
