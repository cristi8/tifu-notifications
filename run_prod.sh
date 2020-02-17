#!/bin/bash


docker pull cristi8/tifu-notifications-frontend
docker pull cristi8/tifu-notifications-backend

docker stop tifu-fe && docker rm tifu-fe
docker stop tifu-be && docker rm tifu-be

docker run -d --name=tifu-fe --restart=always --net=host cristi8/tifu-notifications-frontend

docker run -d --name=tifu-be --restart=always --net=host \
		-e GOOGLE_APPLICATION_CREDENTIALS=/creds \
        -e TIFU_NOTIFY_SECRET=/notify-secret \
		-v /etc/cristi8/tifu-notifications-service-account-key.json:/creds:ro \
		-v /etc/cristi8/tifu-notify-secret.txt:/notify-secret:ro \
		cristi8/tifu-notifications-backend
