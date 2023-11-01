import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

JIRA_PROJECT_URL = str(os.getenv("JIRA_PROJECT_URL"))
JIRA_USER_EMAIL = str(os.getenv("JIRA_USER_EMAIL"))
JIRA_API_TOKEN = str(os.getenv("JIRA_API_TOKEN"))
