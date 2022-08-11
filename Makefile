run:
	python3 loggenerator.py

docker-build:
	docker build -t oleewere/loggenerator:latest .

docker-run:
	docker run --rm oleewere/loggenerator:latest