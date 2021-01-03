.PHONY: run-db, run

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

run-db:
	test -n "$(WIMWB_DB_PASSWORD)" && \
	docker run --name=whatismybrowser-db \
	--mount type=bind,src=$(current_dir)/data/,dst=/docker-entrypoint-initdb.d/ \
	-e MYSQL_ROOT_PASSWORD=${WIMWB_DB_PASSWORD} -e MYSQL_DATABASE="uas" \
	-p 3306:3306 -d mysql:latest

run:
	uvicorn wimwb.web:app --reload
