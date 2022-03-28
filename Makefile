.PHONY: start_server
start_server:
	chmod +x scripts/start_server.sh
	./scripts/start_server.sh
.PHONY: stop_server
stop_server:
	chmod +x scripts/stop_server.sh
	./scripts/stop_server.sh
test:
	chmod +x scripts/test.sh
	./scripts/test.sh
shutdown:
	chmod +x scripts/shutdown.sh
	./scripts/shutdown.sh
submit_flow_data:
	chmod +x scripts/post_request.sh
	./scripts/post_request.sh
get_flow_data:
	chmod +x scripts/get_request.sh
	./scripts/get_request.sh
purge_all:
	chmod +x scripts/purge_all.sh
	./scripts/purge_all.sh
