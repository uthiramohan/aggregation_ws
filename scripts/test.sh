#!/bin/bash

pytest
pytest --cov-report term-missing --cov=app tests/