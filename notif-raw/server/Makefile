
## To generate keys:
# openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem
# openssl ec -in ./vapid_private.pem -outform DER|tail -c +8|head -c 32|base64|tr -d '=' |tr '/+' '_-' >> private_key.txt
# openssl ec -in ./vapid_private.pem -pubout -outform DER|tail -c 65|base64|tr -d '=' |tr '/+' '_-' >> public_key.txt
## ...and remove newlines from the .txt files

## To generate Flask secret key:
# python3 -c 'import os, base64; print(base64.b64encode(os.urandom(16)).decode())' > flask_secret_key.txt

FLASK_SECRET_KEY := $(shell cat ../keys/flask_secret_key.txt)
VAPID_PRIVATE_KEY := $(shell cat ../keys/private_key.txt)
VAPID_PUBLIC_KEY := $(shell cat ../keys/public_key.txt)


build:
	docker build -t cristi8/tifu-notifications-server .

test: build
	docker run -it --net=host --rm \
	-e FLASK_SECRET_KEY=${FLASK_SECRET_KEY} \
	-e VAPID_PRIVATE_KEY=${VAPID_PRIVATE_KEY} \
	-e VAPID_PUBLIC_KEY=${VAPID_PUBLIC_KEY} \
	cristi8/tifu-notifications-server

