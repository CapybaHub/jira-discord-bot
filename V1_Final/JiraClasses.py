from datetime import datetime

from utils import getDatetimeFromIsoFormatWithZ, getDuration

class IssueDetails:
    def __init__(self, issue_data):
        self.id = issue_data.get("id")
        self.self = issue_data.get("self")
        self.key = issue_data.get("key")
        self.fields = Fields(issue_data.get("fields"))
        self.isDone = self.fields.status.name == "Concluído"

    def getCurrentStatus(self):
        return self.fields.status.name


class Fields:
    def __init__(self, fields_data):
        self.sprint = Sprint(fields_data.get("sprint"))
        self.project = Project(fields_data.get("project"))

class Sprint:
    def __init__(self, sprint_data):
        self.id = sprint_data.get("id")
        self.self = sprint_data.get("self")
        self.state = sprint_data.get("state")
        self.name = sprint_data.get("name")
        self.startDate = getDatetimeFromIsoFormatWithZ(sprint_data.get("startDate"))
        self.endDate = getDatetimeFromIsoFormatWithZ(sprint_data.get("endDate"))
        self.createdDate = sprint_data.get("createdDate")
        self.originBoardId = sprint_data.get("originBoardId")
        self.goal = sprint_data.get("goal")

    def getSprintDuration(self):
        return getDuration(self.startDate, self.endDate, "days")

    def getDaysPassed(self):
        return getDuration(self.startDate, datetime.now(), "days")

    def getDaysRemaining(self):
        return getDuration(datetime.now(), self.endDate, "days")


class Project:
    def __init__(self, project_data):
        self.self = project_data.get("self")
        self.id = project_data.get("id")
        self.key = project_data.get("key")
        self.name = project_data.get("name")
        self.projectTypeKey = project_data.get("projectTypeKey")
        self.simplified = project_data.get("simplified")
        self.avatarUrls = project_data.get("avatarUrls")