# Run this manually to start the Python process on the production server.
cd /srv/emergency.bustbyte.no;
. ./env/bin/activate
export PYTHONPATH=/srv/emergency.bustbyte.no/src;
kill -9 $(pidof python3);
nohup python3 src/webserver/server.py 2>&1 &
