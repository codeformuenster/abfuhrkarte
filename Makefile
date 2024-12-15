OPENDATA_URL=https://opendata.stadt-muenster.de/sites/default/files/awm_abfuhrkalender_2024.zip

CONTAINER_ENGINE ?= $(if $(shell command -v podman), podman, docker)
CONTAINER_RUN_ARGS = --rm -v $(PWD)/data:/app/data
CONTAINER_RUN_ARGS += $(if $(filter ${CONTAINER_ENGINE}, podman), --userns=keep-id)

data/abfuhrdaten.csv:
	wget -qO- $(OPENDATA_URL) | zcat | iconv -f ISO-8859-1 -t UTF-8 -o data/abfuhrdaten.csv

.PHONY: build-container
build-container:
	$(CONTAINER_ENGINE) build -t abfuhrkarte .

.PHONY: clean
clean:
	rm data/*.csv data/*.json

data/calendar.json: data/abfuhrdaten.csv
	$(CONTAINER_ENGINE) run ${CONTAINER_RUN_ARGS} abfuhrkarte load_calendar

data/geometries.json:
	$(CONTAINER_ENGINE) run ${CONTAINER_RUN_ARGS} abfuhrkarte build_geometries

dist/index.html:
	$(CONTAINER_ENGINE) run ${CONTAINER_RUN_ARGS} -v $(PWD)/dist:/app/dist abfuhrkarte generate_html

.PHONY: all
all: build-container data/abfuhrdaten.csv data/calendar.json data/geometries.json dist/index.html
