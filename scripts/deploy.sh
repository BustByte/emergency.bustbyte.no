# Deploy to the production server. This presumes
# that ./scripts/start-webserver.sh is running.
ssh michael@emergency.bustbyte.no <<EOF
    cd /srv/emergency.bustbyte.no
    source env/bin/activate
    git fetch origin
    git reset --hard origin/master
    make install
    ./scripts/start-webserver.sh
EOF
