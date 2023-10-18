ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

perms:
	sudo chown -hR ${USER}:${USER} .

setup_venv:
	bash scripts/setup-venv.sh

build:
	docker build -t jira-discord-bot . 

up:
	docker run -d --name jira-discord-bot jira-discord-bot

enter:
	docker-compose exec $(ARG) bash
