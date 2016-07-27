# QuickChatz
A sign-up free chat application written using Django, Twisted and WebSockets. Ability to create chats, by generating a chat ID and join chats using the chat ID

## How to start the chat and web servers
- Install Twisted and Django
- Make migratioons (In WebServer directory): `python manage.py makemigrations`, then `python manage.py migrate`
- Run WebServer (In WebServer directory): `python manage.py runserver`
- Run ChatServer (In ChatServer directory): `twistd -n -y WSServer.py`
- Go to 'http://127.0.0.1:8000/'

## How to use site
- Click 'Create Chat' to create a chat, this will redirect you to the 'Join Chat' page but with a newly generated chat ID in the input field
- Share your chat ID
- People will join by clicking 'Join Chat' and entering the chat ID in the input field

## TODO
- Check if the chat ID exists in the database before joining client to chat ID in the chat server not just the web server

