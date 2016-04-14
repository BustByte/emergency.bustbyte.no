# Emergency (Project in TDT4215) [![Build Status](https://travis-ci.org/BustByte/emergency.bustbyte.no.svg?branch=master)](https://travis-ci.org/BustByte/emergency.bustbyte.no)
Group members:
- Sigurd Grøneng
- Michael McMillan
- Eirik Fosse

## Install
```
make install
```
- You should run the system in a virtual environment for it to work properly.
- Our database of tweets is not included. Twitter only allows fetching 3200 tweets back in time on a user timeline, so we retrieved the rest of the tweets from a third party. We have however included a twitter download script where you can download the latest 3200 tweets for a list of users.
- Before the system can work properly, you must add config details to `config.py`.

## Start
```
make serve
```
Then open `localhost:9090` in your browser.

