#!/usr/bin/env python
# coding: utf-8

# # SIMPLE FACEBOOK & IG PAGE PARSER (VERY RUDIMENTARY)

# In[24]:


# importing dependencies
from bs4 import BeautifulSoup as soup #for parsing the page
import requests #to make a url request
import re #for extracting numbers in text
import pandas as pd #for dealing with excel files
import time
from datetime import datetime
import random as rand
import pathlib


# In[3]:


def ScrapeFBLikesAndFollowers(url) :
    #fetch url
    #make request
    response = requests.get(url)

    #parse page using BeautifulSoup
    parse_page = soup(response.content, 'lxml')

    #find initial column containing community metrics (i.e. likes, follows, check-ins)
    community_metrics_0 = parse_page.find('div', attrs={'id' : 'PagesProfileHomeSecondaryColumnPagelet'})

    #go down the tree and find box containing likes & follows
    community_metrics = community_metrics_0.find('div', attrs={'class' : '_4-u2 _6590 _3xaf _4-u8'})

    #take only the number part of the like/follow count text
    likes = re.findall(r'\d+', community_metrics.contents[1].find('div', attrs={'class' : '_4bl9'}).text)
    follows = re.findall(r'\d+', community_metrics.contents[2].find('div', attrs={'class' : '_4bl9'}).text)

    #list-ify likes and follows count
    likesnfollows = (int("".join(likes)), int("".join(follows)))

    return likesnfollows


# In[4]:


def ScrapeIGLikesAndFollowers(url) :
    #clear the code as text holder
    code_as_text = ''

    #fetch the IG page and set it as text
    code_as_text = requests.get(url).text

    #find these two items denoting the number of followers and posts
    posts = "".join(re.findall(r'\d+', code_as_text[code_as_text.find('timeline_media":{"count":')+len('timeline_media":{"count":'):code_as_text.find(',"page_info"', code_as_text.find('timeline_media":{"count":')+len('timeline_media":{"count":'))]))
    followers = "".join(re.findall(r'\d+',code_as_text[code_as_text.find('"edge_followed_by":{"count":')+len('"edge_followed_by":{"count":'):code_as_text.find('},"followed_by_viewer"')]))

    #collect it to a tuple
    collect = (followers, posts)

    #capture for cases where some items cannot be found
    followersandposts =  tuple(map(lambda x: "NA" if len(x) > 20 else int(x) , collect))

    return collect


# In[5]:


def Scrape(SM, url) :
    rVal = tuple()
    if SM == "fb" :
        rVal = ScrapeFBLikesAndFollowers(url)
    if SM == "ig" :
        rVal = ScrapeIGLikesAndFollowers(url)
    return rVal


# In[7]:


#initial interface

print("A Very Simple Facebook and IG Scraper")
print("Made for : Sevenrooms")
print("Made by : En Mayordomo")
print("Made by : En Mayordomo")
#fetches the name of the file to be worked on

while True:
    try :
        xls_name = input("*What is the name of the file you're working on? (MUST BE IN THE SAME FOLDER AS THIS PROGRAM AND AN .XLSX FILE)")
        fullxlsname = xls_name + ".xlsx"
        xlfile = pd.read_excel(fullxlsname)
    except FileNotFoundError :
        print("*No file with that name. Are you sure it's correctly typed OR is in the same folder as this code?")
    else :
        break

#fetches the lower and upper bounds

looper = True
while looper :
    getlower = int(input("*What row should I start?")) 

    getupper = int(input("*What row should I end?"))

    lower = getlower - 2
    upper = getupper - 1
    if getlower >= getupper :
        print("*Your end row must be greater than your start row. Let's try again")
    else :
        print("*Thank you!")
        time.sleep(1)
        print("*This looks good")
        looper = False 
        

dfrange = xlfile.loc[lower:upper, :]


# In[ ]:





# In[11]:


print("Scraping addresses...")
dic_to_return = {}

smtypes = ['Instagram URL', 'Facebook URL']

SM = {'Instagram URL' : 'ig',
      'Facebook URL' : 'fb'   
}

for index in dfrange.index :
    print("Now at row {}, {}".format(str(index + 2), dfrange.loc[index, 'Venue']), end = '\r')
    templist = []
    for smtype in smtypes :
        try :
            if not pd.isna(dfrange.loc[index, smtype]) :
                templist.append(Scrape(SM[smtype], dfrange.loc[index, smtype]))
            else :
                templist.append(("NA", "NA"))
            time.sleep(rand.randrange(10, 20))
        except AttributeError :
            templist.append(("NA", "NA"))
            continue
    dic_to_return.update({dfrange.loc[index, 'Venue'] : templist})
print("Done!")


# In[12]:


results_df = pd.DataFrame.from_dict(dic_to_return).transpose()
results_df.rename(columns = {0: 'Instagram', 1:'Facebook'}, inplace=True)
finalcolnames = {'Instagram0': 'Instagram Followers', 
                 'Instagram1' : 'Instagram Posts', 
                 'Facebook0' : 'Facebook Likes', 
                 'Facebook1' : 'Facebook Followers'}
for colname in list(results_df.columns) :
    for i in range(0, 2) :
        results_df[finalcolnames[colname + str(i)]] = ['' if item[i] == 'NA' else item[i] for item in list(results_df.loc[:, colname])]


# In[36]:


dffinal = results_df.loc[:, ['Instagram Followers', 'Instagram Posts', 'Facebook Likes', 'Facebook Followers']]


# In[38]:


t = datetime.now().strftime("%Y%m%d%H%M%S")
name = t + "- scrape.csv"
print("Exporting to a csv file...")
dffinal.to_csv(str(pathlib.Path().absolute())+name)
print("Done! Check the output file.")

