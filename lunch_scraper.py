import re
from typing import List
import requests
from bs4 import BeautifulSoup, Tag

# OGM CLASS NO WAY -> happy risa
class Lunch:
    date: str
    soup: str
    lunch: str

    def __init__(self, date, soup, lunch) -> None:
        self.date = date
        self.soup = soup
        self.lunch = lunch

# another class???? -> happier risa

class lunchScraper:
    url: str
    soup: BeautifulSoup
    lunches: List[Lunch]
    strip_html_tags_regex = re.compile("<.*?>")
    get_div_content_regex = re.compile(r'<div[^>]*\bclass="den"[^>]*>(.*?)<\/div>')

    def __init__(self, url) -> None:
        self.url = url
        self.soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.lunches = []
        orders = self.soup.find_all("div", {"class": "objednavka"})

        for order in orders:
            self.lunches.append(self.parseLunch(order))



    def removeHtmlTags(self, html: Tag) -> str:
        return re.sub(self.strip_html_tags_regex, '', str(html))

    def parseLunch(self, html: Tag) -> Lunch:
        return Lunch(
                    self.getDay(html),
                    self.getSoup(html),
                    self.getLunch(html)
                    )


    def getLunch(self, html: Tag) -> str:
        lines = self.removeHtmlTags(html)
        lines = lines.splitlines()
        for i,line in enumerate(lines):
            if "Oběd1" in line:
                if i+1 < len(lines):
                    return lines[i+1]
        return "None"


    def getSoup(self, html: Tag) -> str:
        lines = self.removeHtmlTags(html)
        lines = lines.splitlines()
        for i,line in enumerate(lines):
            if "Polévka" in line:
                if i+1 < len(lines):
                    return lines[i+1]
        return "None"


    def getDay(self, html: Tag) -> str:
        day_src = html.find("div", {"class" : "den"})
        day_src = str(self.get_div_content_regex.findall(str(day_src)))
        day_src = day_src.replace('[', '')
        day_src = day_src.replace(']', '')
        day_src = day_src.replace('\'', '')
        return day_src
