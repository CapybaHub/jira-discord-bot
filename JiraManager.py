from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
import requests
import json

from JiraClasses import IssuesList, Sprint


class JiraAPIClient:
    """
    Integration with JIRA WebService.

    https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#about
    """

    user = None
    api_token = None
    project_url = None

    def __init__(self, JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN):
        self.user = JIRA_USER_EMAIL
        self.api_token = JIRA_API_TOKEN
        self.project_url = JIRA_PROJECT_URL

    def _requestToAgile(self, method, suffix, **kwargs):
        response = requests.request(
            method,
            urljoin(f"{self.project_url}/rest/agile/1.0/", suffix),
            auth=HTTPBasicAuth(self.user, self.api_token),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            **kwargs,
        )
        self._handle_api_error(response)
        return response

    def _request(self, method, suffix, **kwargs):
        response = requests.request(
            method,
            urljoin(f"{self.project_url}/rest/api/3/", suffix),
            auth=HTTPBasicAuth(self.user, self.api_token),
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

    def get_projects(self, params=None):
        """Listar todos os projetos com paginação."""
        response = self._request(
            "GET",
            f"project/search",
            params=params,
        )
        return response.json()

    def get_sprint_list(self, boardId):
        """Listar todas sprints."""
        response = self._requestToAgile(
            "GET",
            f"board/{boardId}/sprint",
        )
        return response.json()

    def get_project_list(self, boardId):
        """Listar todos projetos."""
        response = self._requestToAgile(
            "GET",
            f"board/{boardId}/project",
        )
        return response.json()

    def get_board_list(self):
        """Listar todos projetos."""
        response = self._requestToAgile(
            "GET",
            f"board",
        )
        return response.json()

    def get_sprint_data(self, sprint_id):
        """Obter dados de uma sprint."""
        response = self._requestToAgile(
            "GET",
            f"sprint/{sprint_id}",
        )
        sprint = Sprint(response.json())
        return sprint

    def get_sprint_burndown(self, sprint_id):
        """Obter o relatório de burndown de uma sprint."""
        response = self._requestToAgile(
            "GET",
            f"sprint/{sprint_id}/burndownData",
        )
        return response.json()

    def get_tasks_in_sprint(self, sprint_id):
        """Listar todas as tasks de uma sprint."""
        response = self._requestToAgile(
            "GET",
            f"sprint/{sprint_id}/issue",
        )

        data = response.json()

        # Create an Issue instance
        issues = IssuesList(
            startAt=data["startAt"],
            maxResults=data["maxResults"],
            total=data["total"],
            issues=data["issues"],
        )

        return issues
