# Chune

Chune is a webapp that allows anyone to add songs to your spotify queue. This enables you to plug 
in to your speakers when hosting a party and let people request songs without having to get your
attention or physically access your spotify device.

Chune is written in Python3 using Flask and Spotipy.   ... AND NOW DOCKER!

## Docker instructions

To run with docker:
- Clone the docker branch of the repo.
- Modify `creds-template.txt` with your spotify creds as described below and save it as `creds.txt`.
- Use `docker build -t chune-app .` within the repo folder to build the image. This might take a while.
- Once the image is built, use `docker run -id -p 35280:8000 chune-app` with the service exposed on port 35280.
- Find the local IP of the machine running docker with `ifconfig` or `ip addr`. Usually your'e looking for `wlan0` or `eth0`, YMMV.
- You can now access chune on any device on your local network at `<machine ip>:35280` or with `localhost:35280` from the host machine itself.

## WARNING

Chune is not designed to be secure, use at your own risk. As far as I can tell, the only danger is 
attackers queueing songs on your spotify - not the end of the world. I am however not a security
expert and therefore give no guarantees of safety or privacy.

## Development State
This project is currently a quick and dirty solution to address my needs, if there is any interest here I will rewrite it in a more proper fashion (actually use Flask properly, work out how to make the app stateful without using random files, add a credentials/login UI.).

## Other Files
To use your spotify account, you need to make an account on the spotify for developers page and add an app to generate a user ID and user secret. These should be placed in a file called 'creds.txt' and placed next to 'app.py'.
The spotipy creds manager should create a file '.cache' in the project directory to store cached auth tokens, allowing you to authenticate once and then use the same token again automatically.


