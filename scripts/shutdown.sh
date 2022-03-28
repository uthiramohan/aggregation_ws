#!/bin/bash
echo "Shutting Down!!"
echo "Killing the server"
sh ./scripts/stop_server.sh
echo "Deleting the Virtual Environment workspace"
rm -r aggregation_ws server.log
