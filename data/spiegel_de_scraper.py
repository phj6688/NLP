from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from itertools import zip_longest, chain
from time import sleep
import snoop

# url grabber
@snoop
def url_topic_grabber(url,start,end):
    urls = []
    for i in range(start,end):
        url_ = f'{url}p{i}'
        request = requests.get(url_).text
        soup = bs(request,'lxml')
        href = soup.find_all('a',class_ = 'text-black block')
        for i in href:
            urls.append(i.get_attribute_list('href'))
    urls = set(list(chain.from_iterable(urls)))
    print('urls list done!')
    return list(urls)



@snoop
def grab_details(urls, topic):
    day = []
    month = []
    year = []
    category = []
    article_ = []
    kurz_text = []
    haupt_text = []
    
    count = 0
    for url in urls:
        try:
            request = requests.get(url).text
            soup = bs(request, 'lxml')
            article_.append(soup.find('span',class_='align-middle').text)
            kurz_text.append(soup.find('div',class_="RichText RichText--sans leading-loose lg:text-xl md:text-xl sm:text-l lg:mb-             32 md:mb-32 sm:mb-24").text)
            haupt_text.append(soup.find('div',class_="RichText RichText--iconLinks lg:w-8/12 md:w-10/12 lg:mx-auto md:mx-auto                 lg:px-24 md:px-24 sm:px-16 break-words word-wrap").text)
            day.append(int(soup.find('time', class_='timeformat').text.split(',')[0].split('.')[0]))
            month.append(int(soup.find('time', class_='timeformat').text.split(',')[0].split('.')[1]))
            year.append(int(soup.find('time', class_='timeformat').text.split(',')[0].split('.')[2]))
            count +=1
            if count % 100 == 0:
                print(f'{count} pages done!')
            elif count % 500 == 0:
                sleep(1200)
            category.append(topic)
        except:
            pass
    print(f'last page done! {count}')
    
    list_of_results = [day, month, year, category, article_, kurz_text, haupt_text]
    export_data = zip_longest(*list_of_results, fillvalue = '')
    df = pd.DataFrame(export_data,columns=['day', 'month', 'year', 'category', 'article', 'kurz_text', 'haupt_text'])
    df.to_csv(f'{topic}.csv', index = True, index_label='Line_ID', header = True )
    
    
    return df



# get the urls
politik_urls = url_topic_grabber('https://www.spiegel.de/politik/',1,200)
sport_urls = url_topic_grabber('https://www.spiegel.de/sport/',1,200)
kultur_urls = url_topic_grabber('https://www.spiegel.de/kultur/',1,200)
# save to csv
df_politik_urls = pd.DataFrame(politik_urls)
df_politik_urls.to_csv('politik_urls.csv')

df_sport_urls = pd.DataFrame(sport_urls)
df_sport_urls.to_csv('sport_urls.csv')

df_kultur_urls = pd.DataFrame(kultur_urls)
df_kultur_urls.to_csv('kultur_urls.csv')
''''
# run the function through all three url list

politik = grab_details(politik_urls,'Politik')
sport = grab_details(sport_urls,'Sport')
kultur = grab_details(kultur_urls,'Kultur')

''''




#list_of_results = [day, month, year, category, article_, kurz_text, haupt_text]
#export_data = zip_longest(*list_of_results, fillvalue = '')

#df = pd.DataFrame(export_data,columns=['day', 'month', 'year', 'category', 'article', 'kurz_text', 'haupt_text'])
#df.to_csv(f'{}.csv', index = True, index_label='Line_ID', header = True )

