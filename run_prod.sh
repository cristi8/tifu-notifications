#!/bin/bash

docker stop tifu-fe && docker rm tifu-fe
docker stop tifu-be && docker rm tifu-be


docker pull cristi8/tifu-notifications-frontend
docker pull cristi8/tifu-notifications-backend

docker run -d --name=tifu-fe --restart=always --net=host cristi8/tifu-notifications-frontend

docker run -d --name=tifu-be --restart=always --net=host \
		-e GOOGLE_APPLICATION_CREDENTIALS=/creds \
		-v /etc/cristi8/tifu-notifications-service-account-key.json:/creds:ro \
		cristi8/tifu-notifications-backend
