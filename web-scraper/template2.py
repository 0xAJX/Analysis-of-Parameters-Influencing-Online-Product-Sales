import requests 
import bs4
res = requests.get('https://www.amazon.in/Power-Your-Subconscious-Mind-Success/dp/8172345666/ref=sr_1_1_sspa?s=books&ie=UTF8&qid=1536939154&sr=1-1-spons&keywords=books&psc=1&smid=A05378423NJE7Q5XCN3XZ')

SOUP = bs4.BeautifulSoup(res.text, 'lxml')
rating_histo = SOUP.find_all('tr', {'class':'a-histogram-row'})
rating_5 = rating_histo[0].text.split('star')[1].replace('%', '')
rating_4 = rating_histo[1].text.split('star')[1].replace('%', '')
positive = int(rating_5) + int(rating_4)
positive = float(positive)
print(positive)