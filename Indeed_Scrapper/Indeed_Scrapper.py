import requests as req
import bs4
from bs4 import BeautifulSoup as BS
import urllib
import pandas as pd
import numpy as np
import re
pd.set_option('max_colwidth',500)

#URL = 'https://www.indeed.com/worldwide'

USA_URL = 'https://www.indeed.com/jobs?q=Python&jt=fulltime&sort='
USA_URL_base = 'https://www.indeed.com/jobs?q='
st = '&sort='
sort_options = 'date'
start_page = '&start='
job = 'Python'
jobtype = '&jt='
jt = 'fulltime'

p = req.get(USA_URL)
soup = BS(p.text,'html.parser')
data = pd.DataFrame()

# We can only scrape 100 sites
pages = range(1,5)


for i in pages:
    i = (i-1)*10
    u = f'{USA_URL_base}{job}{jobtype}{jt}{st}{sort_options}{start_page}{i}'
    #print(u)
    p = req.get(u)
    soup = BS(p.text, 'html.parser')
    soupElements = soup.find_all(name='div',attrs={'class' : 'row'})
    #print(soupElements)
    for s in soupElements:
        company = s.find('span', attrs={'class': 'company'}).getText().strip()
        #print(company)
        title = s.find('a', attrs={'data-tn-element':'jobTitle'})['title']
        #print(title)
        indeed = "http://www.indeed.com"
        link = f"{indeed}{s.find('a').get('href')}"
        #print(link)
        address = s.find('span', attrs={'class': 'location'}).getText()
        #print(address)
        post_date = s.find('span', attrs={'class': 'date'}).getText()
        #print(post_date)
        summary = s.find('div', attrs={'class': 'summary'}).getText().strip()
        #print(summary)
        link_company = s.find('span', attrs={'class': 'company'}).find('a')
        #print(link_company)
        if link_company != None:
            link_company = (f"{indeed}{link_company['href']}")
        else:
            link_company = None
        salary = s.find('span', attrs={'class': 'salary no-wrap'})
        if salary != None:
            salary=salary.text.strip()
        else:
            salary = None


        data = data.append({'Company Name':company,
        'Job Title':title,
        'Link to Job':link,
        'Salary':salary,
        'Job Posted Date':post_date,
        'Job Location':address,
        'Description':summary,
        'Company Link':link_company,
        'Overall_rating': None,
        'wl_bal_rating': None,
        'benefit_rating': None,
        'jsecurity_rating': None,
        'mgmt_rating': None,
        'Culture_rating': None
        }, ignore_index=True)

##print(data.describe())

#df = data

for i in range(0,len(data)):
    comp_target = data.iloc[i]['Company Name']
    #print(comp_target)
    comp_link = data.iloc[i]['Company Link']
    if comp_link != None:
        print(comp_link)
        t2 = req.get(comp_link)
        #print(t2)
        s2 = BS(t2.text, 'html.parser')
        #print(s2)
        rating = s2.find_all(name='td',attrs={'class' : 'cmp-RatingCategory-rating'})
        Work_LifeBalance = float((rating[0].text))
        Compensation_Benefits = float(rating[1].text)
        JobSecurity_Advancement = float(rating[2].text)
        Management = float(rating[3].text)
        Culture = float(rating[4].text)
        Overall_Rating = round(np.mean((Work_LifeBalance,Compensation_Benefits,JobSecurity_Advancement,Management,Culture)),2)
        print(Overall_Rating)
