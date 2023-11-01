ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

perms:
	sudo chown -hR ${USER}:${USER} .

setup_venv:
	bash scripts/setup-venv.sh

build:
	docker build -t jira-discord-bot . 

up:
	docker compose up 

down:
	docker compose down

enter:
	docker-compose exec $(ARG) bash

test-jira:
	bash scripts/instance-jira-client.sh
