#!/bin/bash

echo "==============================="
echo "Creating Virtual Environment"
python3 -m venv aggregation_ws
echo "Activating Virtual Environment"
source aggregation_ws/bin/activate
echo "Install required dependencies"
pip install -r requirements.txt
echo "==============================="
echo "Starting server: http://127.0.0.1:8080"
uvicorn --host 127.0.0.1 --port 8080 main:flow_aggregation_app --log-config config/logfile.ini


