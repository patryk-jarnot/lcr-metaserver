CONTAINER_NAME=lcr-metaserver
CONTAINER_ID=$(shell docker ps | grep ${CONTAINER_NAME} | grep -oE "^\w+")

build:
	DOCKER_BUILDKIT=1 docker build -t ${CONTAINER_NAME} .

run:
	docker run -v $(shell pwd)/data:/${CONTAINER_NAME}/data \
		 --expose 8000 -p 8000:8000 \
		 --expose 5002 -p 5002:5002 \
	  ${CONTAINER_NAME}

start:
	docker run -v $(shell pwd)/data:/${CONTAINER_NAME}/data \
		 --expose 8000 -p 8000:8000 \
		 --expose 5002 -p 5002:5002 \
	  ${CONTAINER_NAME} tail -f /dev/null

stop:
	docker stop ${CONTAINER_ID}

attach:
	docker exec -it ${CONTAINER_ID} /bin/bash

# You can use it in case of unexpected failures. IT CLEANS DOCKER CACHE!!!
clean:
	docker stop $(shell docker ps -a -q)
	docker system prune -a

