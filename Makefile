build-dev:
	docker build -t tern-rest-api:dev .


serve-dev: build-dev
	docker run --rm --name tern-rest-api -e ENVIRONMENT=DEVELOPMENT --privileged -v /var/run/docker.sock:/var/run/docker.sock -v $(PWD):/opt/tern-rest-api -p 5001:80 tern-rest-api:dev
