import requests

class JiraAPIManager:
    def __init__(self, url, email, token):
        self.url = url + "/rest/api/3"
        self.userAuth = email + ":" + token
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def getIssue(self, issueIdOrKey):
        print('issue', issueIdOrKey)
        url = self.url + "/issue/" + issueIdOrKey
        response = await requests.request(
            "GET", url, headers=self.headers, auth=(self.userAuth)
        )
        return response.json()