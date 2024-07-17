docker:
	@rm -f build/Dockerfile
	@cp build/Dockerfile.temp build/Dockerfile
	@docker build -t fast_api_demo -f build/Dockerfile .