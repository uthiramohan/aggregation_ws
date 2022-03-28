#!/bin/bash
echo "Purging!!!!!!!"
echo "=============================================================="
echo "Shutting down server"
sh scripts/shutdown.sh
echo "=============================================================="
echo "Purging the databases"
if [[ -f "flows.db" ]]; then

  rm flows.db
fi
if [[ -f "test.db" ]]; then
  rm test.db
fi
if [[ -f "tests/test.db" ]]; then
  rm tests/test.db
fi