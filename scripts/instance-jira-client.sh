#!/usr/bin/env bash

bash scripts/setup-venv.sh

python -c "
import JiraManager
from settings import (
    DISCORD_API_TOKEN,
    JIRA_API_TOKEN,
    JIRA_PROJECT_URL,
    JIRA_USER_EMAIL,
    commandPrefixes,
    getAvailableCommands,
)

jiraAPI = JiraManager.JiraAPIClient(JIRA_PROJECT_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN)

import code
code.interact(local=locals())
"