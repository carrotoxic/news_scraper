import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {'User-Agent': ua}

target_url = 'https://a16z.com/news-content/'
response = requests.get(target_url,headers=headers)


title_list = []
url_list = []
content_list = []

if response.status_code == 200:

    soup = BeautifulSoup(response.text,"html.parser")
    for articles in soup.find_all('ul', class_='recent-announcements-list'):
        article = articles.find_all('a')

        for elem in article:
            title = elem.text.strip()
            url =  elem.get('href')
            if url != None:
                title_list.append(title)
                url_list.append(url)
                all_text = ''

                target_url_content = url
                response_url = requests.get(target_url_content, headers=headers)

                if response_url.status_code == 200:

                    soup2 = BeautifulSoup(response_url.text, "html.parser")
                    for lines in soup2.find_all('div', attrs={ 'class': ['tombstone-enable', 'post-block'] }):
                        all_text  +=  lines.text
                    content_list.append(all_text)

    zipped = zip(title_list, url_list, content_list)
    whole_list = list(zipped)              
    df = pd.DataFrame(whole_list, columns = ['Title', 'URL', 'Content'])
    print(df)
    df.to_excel('a16z_announcement.xlsx', index=False)
