from DiscordMessagesHandler import DiscordMessagesHandler
from settings import availableCommands

def getBOTCommands(MessageHandler: DiscordMessagesHandler):
    commandFunctions = {
        "commands":  MessageHandler.listAvailableCommands,
        "oi":MessageHandler.sayHello,
        "issue": MessageHandler.getIssueInfo,
        "boards": MessageHandler.listBoards,
        "sprints": MessageHandler.listSprints,
        "current-sprint": MessageHandler.getCurrentSprintInfo,
        "sprint-report":  MessageHandler.getSprintReport,
        }
        
    commands_with_functions = {}
    
    for command in commandFunctions:
        commands_with_functions[command] = availableCommands[command]
        commands_with_functions[command]["function"] = commandFunctions[command]

    commands_with_aliases = {}

    for command in commands_with_functions:
        commands_with_aliases[command] = commands_with_functions[command]

        if "aliases" in commands_with_functions[command]:
            for alias in commands_with_functions[command]["aliases"]:
                commands_with_aliases[alias] = commands_with_functions[command]

    return commands_with_aliases