import requests
import urllib.request
import requests
import urllib
from urllib.request import urlopen
import urllib3
from bs4 import BeautifulSoup
import re

# for line in urllib.request.urlopen('https://raw.githubusercontent.com/finxter/FinxterTutorials/main/nlights.txt'):
#    print(line.decode("utf-8"))
obedy_accurate = []                 #Create an empty list to store all the food items in the future

def removetags(jidlo):              #Removes all the HTML tags
    CLEANR = re.compile("<.*?>")
    jidloclear = re.sub(CLEANR, '', jidlo)
    return jidloclear
    

url = "https://www.strava.cz/strava5/Jidelnicky?zarizeni=0253"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
obedy_list = soup.find_all("div", {"class": "dialog"})          #Finds all divisions containing the food and food title
for maybejidlo in obedy_list:
    if "Oběd1" or "Pol&#233;vka" in maybejidlo:
        pass
    else:
        obedy_list.remove(maybejidlo)

for obed_kandidat in obedy_list:
    obed_kandidat = obed_kandidat.find_all("div", {"class": "nazev sloupec"})
    obedy_accurate = obedy_accurate + [obed_kandidat]

for jidlo in obedy_accurate: 
        print(removetags(str(jidlo)))
    
