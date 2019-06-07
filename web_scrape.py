# Scraping from CoreyMS
from bs4 import BeautifulSoup
import requests
import csv 


source = requests.get('http://coreyms.com').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('cms_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'video_link'])


# could use a context manager here 
for article in soup.find_all('article'):

    # Grab the headline 
    headline = article.header.h2.a.text 
    print(headline)
    # Grab the summary

    summary = article.find('div', class_='entry-content').p.text
    print(summary)

    # Get the link of the embedded video 
    vid_src = article.find('iframe', class_='youtube-player')['src']
    vid_id = vid_src.split('/')[4]
    vid_id = vid_id.split('?')[0]

    # Create a new youtube link with the parsed information
    yt_link = f'https://youtube.com/watch?v={vid_id}'
    print(yt_link)

    print()

    csv_writer.writerow([headline, summary, yt_link])
csv_file.close()
# soup.prettify() - formats document 
'''
This will get the first tag on the page: 
Access tag like an attribute 
match = soup.title.text
print(match)

-----------------------------------------
Find a specific class with a certain attribute:
match = soup.find('div', class_='footer')
print(match)

-----------------------------------------
Find all of the article headlines in the page 
article = soup.find('div', class_='article')
print(article)

-----------------------------------------
find list of tags that has all the tags
for article in soup.find_all('div', class_='article'):
    headline = article.h2.a.text
    print(headline)
    summary = article.p.text
    print(summary)

'''
