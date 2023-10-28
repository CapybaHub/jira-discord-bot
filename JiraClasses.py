from datetime import datetime

from utils import getDatetimeFromIsoFormatWithZ, getDuration


class IssuesList:
    def __init__(self, startAt, maxResults, total, issues):
        self.startAt = startAt
        self.maxResults = maxResults
        self.total = total
        self.issues = [IssueDetails(issue) for issue in issues]

    def issues_count(self):
        return len(self.issues)


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
        self.statuscategorychangedate = fields_data.get("statuscategorychangedate")
        self.issuetype = IssueType(fields_data.get("issuetype"))
        self.timespent = fields_data.get("timespent")
        self.sprint = Sprint(fields_data.get("sprint"))
        self.project = Project(fields_data.get("project"))
        self.priority = Priority(fields_data.get("priority"))
        self.status = Status(fields_data.get("status"))
        # Add more fields as needed


class IssueType:
    def __init__(self, issuetype_data):
        self.self = issuetype_data.get("self")
        self.id = issuetype_data.get("id")
        self.description = issuetype_data.get("description")
        self.iconUrl = issuetype_data.get("iconUrl")
        self.name = issuetype_data.get("name")
        self.subtask = issuetype_data.get("subtask")
        self.avatarId = issuetype_data.get("avatarId")
        self.hierarchyLevel = issuetype_data.get("hierarchyLevel")
        # Add more fields as needed


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
        # Add more fields as needed


class Priority:
    def __init__(self, priority_data):
        self.self = priority_data.get("self")
        self.iconUrl = priority_data.get("iconUrl")
        self.name = priority_data.get("name")
        self.id = priority_data.get("id")
        # Add more fields as needed


class Status:
    def __init__(self, status_data):
        self.self = status_data.get("self")
        self.description = status_data.get("description")
        self.iconUrl = status_data.get("iconUrl")
        self.name = status_data.get("name")
        self.id = status_data.get("id")
        self.statusCategory = StatusCategory(status_data.get("statusCategory"))
        # Add more fields as needed


class StatusCategory:
    def __init__(self, status_category_data):
        self.self = status_category_data.get("self")
        self.id = status_category_data.get("id")
        self.key = status_category_data.get("key")
        self.colorName = status_category_data.get("colorName")
        self.name = status_category_data.get("name")
        # Add more fields as needed
