import json
import requests
from pprint import pprint

username: str = "Misus91066"
password: str = "94dFZccN"
web_app_url: str = "https://bakalari.gymta.cz/"

class bakalariScraper:
    web_app_url: str
    access_token: str
    refresh_token: str
    timetable: dict
    noticeboard: dict

    def __init__(self, web_app_url: str, username: str, password: str) -> None:
        self.web_app_url = web_app_url
        self.firstAuth(username, password)
        self.getTimetable()
        self.getNoticeboard()
        #pprint(self.noticeboard)


    def firstAuth(self, username: str, password: str) -> None:
        auth_request_headers: dict[str, str] = { "Content-Type": "application/x-www-form-urlencoded" }
        auth_request_body: dict[str, str] = {
                                "client_id" : "ANDR",
                                "grant_type" : "password",
                                "username" : username,
                                "password" : password,
                            }
        resp: requests.Response = requests.post(url=f'{self.web_app_url}api/login', data=auth_request_body, headers=auth_request_headers)
        self.access_token = resp.json()["access_token"]
        self.refresh_token = resp.json()["refresh_token"]

    def getNoticeboard(self) -> None:
        request_headers: dict[str, str] = {
                    "Content-Type" : "application/x-www-form-urlencoded",
                    "Authorization" : f"Bearer {self.access_token}",
                }

        self.noticeboard = requests.post(url=f'{self.web_app_url}api/3/komens/messages/noticeboard', headers=request_headers).json()

    def getTimetable(self) -> None:
        request_headers: dict[str, str] = {
                            "Content-Type" : "application/x-www-form-urlencoded",
                            "Authorization" : f"Bearer {self.access_token}",
                          }
        self.timetable = requests.get(url=f'{self.web_app_url}api/3/timetable/actual', headers=request_headers).json()

    def roomIdToRoom(self, id: str) -> str:
        rooms = self.timetable["Rooms"]
        for room in rooms:
            if room["Id"] == id:
                return room["Abbrev"]
        return ""

    def teacherIdToTeacher(self, id: str) -> str:
        teachers = self.timetable["Teachers"]
        for teacher in teachers:
            if teacher["Id"] == id:
                return teacher["Name"]
        return ""

    def timeIdToTime(self, id: str) -> str:
        hours = self.timetable["Hours"]
        for hour in hours:
            if hour["Id"] == id:
                BeginTime = hour["BeginTime"]
                EndTime = hour["EndTime"]
                fmt_str = f"{BeginTime} - {EndTime}"
                return fmt_str
        return ""

    def subjectIdToSubject(self, id: str) -> str:
        subjects = self.timetable["Subjects"]
        for subject in subjects:
            if subject["Id"] == id:
                return subject["Name"]
        return ""


    def getDayDate(self, i: int) -> str:
        if i > 4:
            return ""
        else:
            day = self.timetable["Days"][i]
            return day["Date"]

    def getLessonSubject(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            return self.subjectIdToSubject(lesson["SubjectId"])
    
    def getLessonRoom(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            return self.roomIdToRoom(lesson["RoomId"])

    def getLessonTeacher(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            return self.teacherIdToTeacher(lesson["TeacherId"])
            

    def getLessonTheme(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            return lesson["Theme"]

    def getLessonChange(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            if lesson["Change"] == None:
                return ""
            else:
                return lesson["Change"]["Description"]

    def getLessonTime(self, day: int, i: int) -> str:
        if day > 4:
            return ""
        else:
            lesson = self.timetable["Days"][day]["Atoms"][i]
            return self.timeIdToTime(lesson["HourId"])

    def getTimetableForDay(self, day: int) -> str:
        if day > 4 or day < 0:
            return "Invalid day"
        if self.timetable["Days"][day]["DayType"] == "Celebration":
            return f"""{self.getDayDate(day)}
Celebration"""

        else:
            return_str = f"""{self.getDayDate(day)}
=============================="""
            for lesson_id in range(len(self.timetable["Days"][day]["Atoms"])):
                return_str += f"""
{self.getLessonTime(day, lesson_id)}
{self.getLessonSubject(day, lesson_id)}
{self.getLessonTheme(day, lesson_id)}
{self.getLessonTeacher(day, lesson_id)}
{self.getLessonRoom(day, lesson_id)}
{self.getLessonChange(day, lesson_id)}
====================================="""
            return return_str

Scraper = bakalariScraper(web_app_url, username, password)

# HOLY FUCK I AM A FUCKING GENIUS MAN HOLY SHIT I HAVE ASCENDED TO THE NEXT PYTHON LEVEL
