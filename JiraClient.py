from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
import requests
from typing import List

from JiraClasses import Board, Issue, Sprint
from settings import JIRA_API_TOKEN, JIRA_PROJECT_URL, JIRA_USER_EMAIL


class JiraAPIClient:
    """
    Integration with JIRA WebService.

    https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/
    """

    user_email = None
    api_token = None
    project_url = None

    def __init__(self, JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN):
        self.user_email = JIRA_USER_EMAIL
        self.api_token = JIRA_API_TOKEN
        self.project_url = JIRA_PROJECT_URL

    def _request(self, method, suffix, **kwargs):
        response = requests.request(
            method,
            urljoin(f"{self.project_url}/rest/agile/1.0/", suffix),
            auth=HTTPBasicAuth(self.user_email, self.api_token),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            **kwargs,
        )
        self._handle_api_error(response)
        return response

    def _handle_api_error(self, response):
        is_json = True
        try:
            response.json()
        except ValueError:
            is_json = False

        if not is_json or not response.ok:
            raise Exception(response)

    def get_all_boards(self):
        """Listar todos quadros."""
        response = self._request(
            "GET",
            f"board",
        )

        boardsList = [Board(board) for board in response.json()["values"]]
        return boardsList

    def get_sprints_from_board(self, boardId):
        """Listar todas sprints."""
        response = self._request(
            "GET",
            f"board/{boardId}/sprint",
        )
        jsonResponse = response.json()

        sprintsList = [Sprint(sprint) for sprint in jsonResponse["values"]]
        return sprintsList

    def get_sprint_data_by_id(self, sprint_id):
        """Obter dados de uma sprint."""
        response = self._request(
            "GET",
            f"sprint/{sprint_id}",
        )
        sprint = Sprint(response.json())
        return sprint

    def get_tasks_in_sprint(self, sprint_id):
        """Listar todas as tasks de uma sprint."""
        response = self._request(
            "GET",
            f"sprint/{sprint_id}/issue",
        )

        data = response.json()

        issuesJSONList = list(data.get("issues"))

        issues: List[Issue] = []

        for issue in issuesJSONList:
            issues.append(Issue(issue))

        return issues

    def get_current_sprint(self, board_id):
        all_sprints = self.get_sprints_from_board(board_id)
        currentSprint = None
        for sprint in all_sprints:
            if sprint.state == "active":
                currentSprint = sprint
                break

        if currentSprint:
            return currentSprint
        else:
            return None
