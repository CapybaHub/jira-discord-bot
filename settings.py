JIRA_PROJECT_URL = "https://jiradiscord.atlassian.net/"
JIRA_USER_EMAIL = "bruno.c0310@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0QdYUjJrH1Rbv-8JpqnJO1K7NBoY9MNBSw2A9h8fCLlWLFcumBMRfLjWCs4-2PxCX3cKmVHscNRUkaLABZb5pjO2boLxsge_cW6v2SzZHNMSNKPS-xZIqkpL0Qafjp9w5R4c0A6oFUOLnp-MZBnsDVB9D8CxgcwKemdqvuY9ZkDs=982157D9"
DISCORD_API_TOKEN = (
    "MTExOTM0OTIzMDk3MzIyNzAzOA.GPDLoh._0fROetStp3nUhd1_ssl4zpTaDJ_3HBmK7B8D8"
)

commandPrefixes = ["!"]
def getAvailableCommands(MessageHandler):
  return {
    "oi": {
        "description": "Saudação",
        "params": [],
        "example": "!oi",
        "function": MessageHandler.sayHello,
    },
    "issue": {
        "description": "Busca uma issue no Jira",
        "params": ["issueIdOrKey"],
        "example": "!issue PROJ-123",
        "function": MessageHandler.getIssueInfo,
    },
}