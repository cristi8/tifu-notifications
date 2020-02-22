# tifu-notifications
Send push notifications to players when using software https://www.dtfb.de/index.php/tifu-die-software

## How to use
There are two components:
 - A python program that should be run in the background at the same time with TiFu software.
 - A server program that handles registration and sends notifications. This is currently deployed at https://foos.cristi8.net/


To use the software, you should:
 - Copy the `tifu_notifications` subdirectory into the TiFu software installation directory.
 - Install Python 3
 - Install dependencies listed in `requirements.txt` by using `pip`
 - Set the secret value in the file `secret.txt`. This can be communicated by Cristian Balas to event organizers, to allow access to sending notifications using `https://foos.cristi8.net/` backend.
 - Run the `run.py` script and keep it running in the background to notify about new matches.



## How it works
 - TiFu software writes tournament progress and match information into `backup` subdirectory.
 - The python script monitors this directory for new information.
 - When a new match is started, the match information is sent to the backend.
 - The backend has a database of registered people (kept in Firebase Firestore)
 - When the backend receives the new match information, it sends push notifications to participants (using Firebase Cloud Messaging)
