build_fastapi:
	@rm -f build/Dockerfile
	@cp build/Dockerfile.temp build/Dockerfile
	@docker build -t fastapi_service -f build/Dockerfile .

build_fluentd:
	@rm -f build/fluentd/Dockerfile
	@cp build/fluentd/Dockerfile.temp build/fluentd/Dockerfile
	@docker build -t fluentd_service -f build/fluentd/Dockerfile .

init_db:
	@python3 script/init-schema.py
	@python3 script/import-data.py

start:
	@docker-compose -f build/docker-compose.yml up -d

stop:
	@docker-compose -f build/docker-compose.yml stop

check:
	@pip3 install pytest
	@pip3 install cryptography
	@docker-compose -f test/docker-compose.yml up -d
	@sleep 5
	@python3 script/init-schema.py
	@python3 script/import-data.py
	@pytest
	@docker-compose -f test/docker-compose.yml down