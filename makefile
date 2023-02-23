DEBUG_FILE = debug.yml
PRODUCTION_FILE = production.yml

up:
	docker-compose -f ${PRODUCTION_FILE} up 

build:
	sudo docker-compose -f ${PRODUCTION_FILE} build

debug_up:
	sudo docker-compose -f ${DEBUG_FILE} up 

debug_build:
	sudo docker-compose -f ${DEBUG_FILE} build