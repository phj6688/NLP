from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from itertools import zip_longest, chain
from time import sleep
import snoop

# url grabber
# use Beautifulsoup to grab the a tags
@snoop
def url_topic_grabber(topic,url,start,end):
    urls = []
    for i in range(start,end):
        url_ = f'{url}p{i}'
        request = requests.get(url_).text
        soup = bs(request,'lxml')
        # find all a tags with this specific class
        href = soup.find_all('a',class_ = 'text-black block')
        # extract the href value
        for i in href:
            urls.append(i.get_attribute_list('href'))
    # remove the duplicate and pass it as a list
    urls = set(list(chain.from_iterable(urls)))
    urls = list(urls)
    # turn it into Dataframe and save it to csv format
    df = pd.DataFrame(urls)
    df.to_csv(f'{topic}_urls.csv')
    


politik_urls = url_topic_grabber('Politik','https://www.spiegel.de/politik/',1,150)
sport_urls = url_topic_grabber('Sport','https://www.spiegel.de/sport/',1,150)
kultur_urls = url_topic_grabber('Kultur','https://www.spiegel.de/kultur/',1,150)