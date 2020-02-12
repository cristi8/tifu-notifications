
build:
	docker build -t cristi8/tifu-notifications-frontend .

test: build
	docker run -it --net=host --rm cristi8/tifu-notifications-frontend

push: build
	docker push cristi8/tifu-notifications-frontend
