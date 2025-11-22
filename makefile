# Makefile for the "Multi-Agent Market Research" project
# You can override the script name by passing SCRIPT=filename.py to make

PYTHON ?= python3
SCRIPT ?= market_research_agents.py

.PHONY: help run

help:
	@echo "Available commands:"
	@echo "  make run                 - run the default script ($(SCRIPT))"
	@echo "  make run SCRIPT=other.py - run a different Python script"

run:
	$(PYTHON) $(SCRIPT)