#res = requests.get('https://www.amazon.in/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Abooks&page=1&keywords=books')

# https://www.amazon.in/s/ref=sr_pg_3?rh=n%3A976389031%2Ck%3Abooks&page=3&keywords=books&ie=UTF8&qid=1549263155
# https://www.amazon.in/s/ref=sr_pg_2?fst=as%3Aon&rh=n%3A976389031%2Ck%3Abooks&page=2&keywords=books
#"https://www.amazon.in/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Abooks&page=1&keywords=books"
# https://www.amazon.in/s/ref=sr_pg_2?rh=n%3A976389031%2Ck%3Abooks&page=2&keywords=books

import requests
import bs4
import csv

for i in range(1, 20):
 x= 'https://www.amazon.in/s/ref=sr_pg_'+ str(i) +'?rh=n%3A976389031%2Ck%3Abooks&page=' + str(i) + '&keywords=books'
 #print(x)
 res = requests.get(x)
 #filename = "data1.csv"
 #f = open(filename, "w")
 with open('data2.csv', 'w') as f:
  thewriter = csv.writer(f)
  soup = bs4.BeautifulSoup(res.text, 'lxml')
  items = soup.find_all('li', 's-result-item') 
  #headers = "sales_rank, overall_rating, positive, negative, no_of_reviews, discount_value, discount_rate\n"
  #f.write(headers)
  thewriter.writerow(['sales_rank', 'overall_rating', 'positive', 'negative', 'no_of_reviews', 'discount_value', 'discount_rate'])
  for item in items:
   try:
    print(item.a['href'])
    RES = requests.get(item.a['href'])
    SOUP = bs4.BeautifulSoup(RES.text, 'lxml')
    # sales_rank 
    container = SOUP.find_all('li',{'id':'SalesRank'})
    sales_rank = container[0].text.split('#')[1].split('(')[0]
    sales_rank = sales_rank.split(' ')[0]
    sales_rank = float(sales_rank)
    print(sales_rank)
    # rating (overall customer review ratings)
    rating = SOUP.find_all('div', {'class':'content'})
    rating = rating[1].find_all('span', {'class':'a-icon-alt'})
    rating = rating[0].text.split(' ')[0]
    rating = float(rating)
    print(rating)
    # discount_value
    container2 = SOUP.find_all('div', {'id':'buyNewInner'})
    discount_value = container2[0].find_all('span', {'class':'a-size-base'})[0].text.strip().split(' ')[3].strip()
    discount_value = float(discount_value)
    print(discount_value)
    # discount_rate
    discount_rate = container2[0].find_all('span', {'class':'a-size-base'})[0].text.strip().split(' ')[-1]
    discount_rate = discount_rate.replace('%', '')
    discount_rate = discount_rate.replace('(', '')
    discount_rate = discount_rate.replace(')', '')
    discount_rate = float(discount_rate)
    print(discount_rate)    
    # positive and negative rating
    rating_histo = SOUP.find_all('tr', {'class':'a-histogram-row'})
    rating_5 = rating_histo[0].text.split('star')[1].replace('%', '')
    rating_4 = rating_histo[1].text.split('star')[1].replace('%', '')
    positive = int(rating_5) + int(rating_4)
    positive = float(positive)
    print(positive)
    rating_2 = rating_histo[-2].text.split('star')[1].replace('%', '')
    rating_1 = rating_histo[-1].text.split('star')[1].replace('%', '')
    negative = int(rating_2) + int(rating_1)
    negative = float(negative)
    print(negative)
    # no_of_reviews
    container1 = SOUP.find_all('div', {'class':'content'})
    contain = container1[1].find_all('span', {'class':'a-size-small'})
    no_of_reviews = contain[0].text.strip()
    no_of_reviews = no_of_reviews.split(' ')[0]
    no_of_reviews = float(no_of_reviews.replace(',', ''))
    print(no_of_reviews)
    li = [sales_rank, rating, positive, negative, no_of_reviews, discount_value, discount_rate]
    #thewriter.writerow([sales_rank+","+rating+","+positive+","+negative+","+no_of_reviews+","+discount_value+","+discount_rate+"\n"])
    thewriter.writerow(li)
   except:
    pass
 
