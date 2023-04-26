import re
import requests
from bs4 import BeautifulSoup, Tag

# the magic url
site_url = "https://www.strava.cz/strava5/Jidelnicky?zarizeni=0253"

# the lunch class we use to easily parse stuff (we dont want žsón)
class Lunch:
    date: str
    soup: str
    lunch: str

    def __init__(self, date, soup, lunch) -> None:
        self.date = date
        self.soup = soup
        self.lunch = lunch


# function to remove the html tags from text
strip_html_tags_regex = re.compile("<.*?>")
def removeHtmlTags(html: Tag) -> str:
    return re.sub(strip_html_tags_regex, '', str(html))

# function that returns the content of a div -> used to get the day
get_div_content_regex = re.compile(r'<div[^>]*\bclass="den"[^>]*>(.*?)<\/div>')
def getDay(html: Tag) -> str:
    day_src = html.find("div", {"class" : "den"})
    day_src = str(get_div_content_regex.findall(str(day_src)))
    day_src = day_src.replace('[', '')
    day_src = day_src.replace(']', '')
    day_src = day_src.replace('\'', '')
    return day_src

def getSoup(html: Tag) -> str:
    lines = removeHtmlTags(html)
    lines = lines.splitlines()
    for i,line in enumerate(lines):
        if "Polévka" in line:
            if i+1 < len(lines):
                return lines[i+1]
    return "None"


def getLunch(html: Tag) -> str:
    lines = removeHtmlTags(html)
    lines = lines.splitlines()
    for i,line in enumerate(lines):
        if "Oběd1" in line:
            if i+1 < len(lines):
                return lines[i+1]
    return "None"

def parseLunch(html: Tag) -> Lunch:
    return Lunch(
                getDay(html),
                getSoup(html),
                getLunch(html)
                )


# the page source code
site_response = requests.get(site_url)
soup = BeautifulSoup(site_response.content, 'html.parser')
lunch_orders = soup.find_all("div", {"class": "objednavka"})

lunch = parseLunch(lunch_orders[0])
print(lunch.date)
print(lunch.soup)
print(lunch.lunch)
print("=================================")
lunch = parseLunch(lunch_orders[1])
print(lunch.date)
print(lunch.soup)
print(lunch.lunch)
print("=================================")
lunch = parseLunch(lunch_orders[2])
print(lunch.date)
print(lunch.soup)
print(lunch.lunch)
print("=================================")
