from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from itertools import zip_longest, chain
from time import sleep
import snoop


@snoop
def grab_details(file, topic):
    day = []
    month = []
    year = []
    category = []
    article_ = []
    kurz_text = []
    haupt_text = []
    

    urls = pd.read_csv(f'{topic}_urls.csv')


    count = 0
    for url in urls['0']:
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
            if count % 500 == 0:
                sleep(1800)
            category.append(topic)
        except:
            pass
    print(f'last page done! {count}')
    

    list_of_results = [day, month, year, category, article_, kurz_text, haupt_text]
    export_data = zip_longest(*list_of_results, fillvalue = '')
    df = pd.DataFrame(export_data,columns=['day', 'month', 'year', 'category', 'article', 'kurz_text', 'haupt_text'])
    df.to_csv(f'{topic}_normal.csv', index = True, index_label='Line_ID', header = True )



# run the function through all three url list

politik = grab_details(politik_urls,'Politik')
sport = grab_details(sport_urls,'Sport')
kultur = grab_details(kultur_urls,'Kultur')






#list_of_results = [day, month, year, category, article_, kurz_text, haupt_text]
#export_data = zip_longest(*list_of_results, fillvalue = '')

#df = pd.DataFrame(export_data,columns=['day', 'month', 'year', 'category', 'article', 'kurz_text', 'haupt_text'])
#df.to_csv(f'{}.csv', index = True, index_label='Line_ID', header = True )

