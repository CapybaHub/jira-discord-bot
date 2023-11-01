from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
import requests

from JiraClasses import IssueDetails, Sprint

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

    def get_sprint_list(self, boardId):
        """Listar todas sprints."""
        response = self._request(
            "GET",
            f"board/{boardId}/sprint",
        )
        return response.json()

    def get_board_list(self):
        """Listar todos quadros."""
        response = self._request(
            "GET",
            f"board",
        )
        return response.json()

    def get_sprint_data(self, sprint_id):
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

        issues = [IssueDetails(issue) for issue in issues]

        return issues
