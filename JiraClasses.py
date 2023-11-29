from datetime import datetime
import json

import discord

from utils import getDatetimeFromIsoFormatWithZ, getDuration


class Issue:
    def __init__(self, issue_data):
        self.id = issue_data.get("id")
        self.self = issue_data.get("self")
        self.key = issue_data.get("key")

        fields = issue_data.get("fields")
        self.status = fields.get("status").get("name")
        self.type = fields.get("issuetype").get("name")
        self.created_at = fields.get("created")
        self.updated_at = fields.get("updated")
        
    def isHistory(self):
        return self.type == 'História' 


class Sprint:
    def __init__(self, sprint_data):
        self.id = sprint_data.get("id")
        self.self = sprint_data.get("self")
        self.state = sprint_data.get("state")
        self.name = sprint_data.get("name")
        self.createdDate = sprint_data.get("createdDate")
        self.originBoardId = sprint_data.get("originBoardId")
        self.goal = sprint_data.get("goal")

        sprintStartDate = sprint_data.get("startDate")
        sprintEndDate = sprint_data.get("endDate")
        self.startDate = (
            getDatetimeFromIsoFormatWithZ(sprint_data.get("startDate"))
            if sprintStartDate
            else None
        )
        self.endDate = (
            getDatetimeFromIsoFormatWithZ(sprint_data.get("endDate"))
            if sprintEndDate
            else None
        )

    def getSprintDuration(self):
        return getDuration(self.startDate, self.endDate, "days")

    def getDaysPassed(self):
        return getDuration(datetime.now(), self.startDate, "days")

    def getDaysRemaining(self):
        return getDuration(datetime.now(), self.endDate, "days")


class Board:
    embed: discord.Embed = None

    def __init__(self, project_data):
        self.self = project_data.get("self")
        self.id = project_data.get("id")
        self.name = project_data.get("name")
        location = project_data.get("location")
        self.key = location.get("projectKey")
        self.fullName = location.get("displayName")
        self.image = location.get("avatarURI")
