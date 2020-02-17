
build:
	docker build -t cristi8/tifu-notifications-backend .

test: build
	docker run -it --net=host --rm \
		-e GOOGLE_APPLICATION_CREDENTIALS=/creds \
		-e TIFU_NOTIFY_SECRET=/notify-secret \
		-v /etc/cristi8/tifu-notifications-service-account-key.json:/creds:ro \
		-v /etc/cristi8/tifu-notify-secret.txt:/notify-secret:ro \
		cristi8/tifu-notifications-backend

push: build
	docker push cristi8/tifu-notifications-backend
