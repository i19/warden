#!/bin/sh
kill -9 $(ps -ef|grep api-server|gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
#python api-server.py &
nohup python api.py > /dev/null 2>&1 &