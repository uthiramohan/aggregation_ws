#!/bin/bash

uvicorn_pid=$(ps aux | grep 'uvicorn' | grep -v grep | awk {'print $2'} )
if [[ -n $uvicorn_pid ]]; then
  echo "Killing uvicorn pid: $uvicorn_pid"
  kill $uvicorn_pid
fi
