import requests
from bs4 import BeautifulSoup
from selenium import webdriver
URL = 'https://music.bugs.co.kr/genre/chart/kpop/jazz/total/day' #URL 변수에는 대상이 되는 사이트의 주소를 넣어줬습니다.

request = requests.get(URL) #request라는 변수를 만들어 requests의 get() 함수를 이용하여 주소를

#넘겨주었습니다 request는 부탁하다 라는 뜻이 있습니다 

html = request.text

soup = BeautifulSoup(html,'html.parser') #soup이라는 변수에는 BeautifulSoup() 함수를 이용해 html 즉 request의 text를. parser 분석하라는 뜻입니다.

# print(URL) #https://music.bugs.co.kr/chart
# print(request) #<Response [200]>

titles = soup.select('p.title')
artists = soup.select('p.artist')
numbers = soup.select('tbody')
driver = webdriver.Chrome('C:\chromedriver.exe') 
print(titles[1].text)
print(artists[1].text)
print(numbers[0])
'''
f = open('BugsTOP100.txt','w',-1,'UTF-8')
for i in range(len(titles)):
    title = titles[i].text.strip().split('\n')[0]
    artist =artists[i].text.strip().split('\n')[0]
    number =numbers[i].get
    data = '{:3}위 {} - {} - {}'.format(i+1, title, artist,number)
    f.write(data + '\n')
f.close()
'''