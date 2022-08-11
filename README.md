# loggenerator

[![Docker Pulls](https://img.shields.io/docker/pulls/oleewere/loggenerator.svg)](https://hub.docker.com/r/oleewere/loggenerator/)
[![](https://images.microbadger.com/badges/image/oleewere/loggenerator.svg)](https://microbadger.com/images/oleewere/loggenerator "")
![license](http://img.shields.io/badge/license-Apache%20v2-blue.svg)

Simple log generator tool with configurable volume and format. Goal is to use this for testing docker log parsing (with stack trace) by different log shipper tools.

## Options

Options can be provided by flags or environment variables:

- `SLEEP_INTERVAL_SEC` env variable or `-s / --sleep-interval` as command argument: Sleep interval between log generation events in seconds. (default: `10`)
- `REPEAT_MESSAGES_BETWEEN_SLEEPS` env variable or `-t / --times` as command argument: Repeat messages number between sleeps. (default: `1`)
- `JSON_FORMAT` env variable or `-j / --json-format` as command argument: Boolean flag to enable json formatted logging. (default: `false`)
- `DOCKER_FORMAT` env variable or `-d / --docker-format` as command argument: Boolean flag to enable docker formatted logging. (default: `false`)
- `BROKEN_JSON` env variable or `-b / --use-broken-json` as command argument: Boolean flag to enable json message splitting. Useful to test joining lines. (default: `false`)

## Usage

Simply run `loggenerator.py` script with python:

```bash
python3 loggenerator.py -j -s 5 -t 2
```

Or run by docker:

```bash
docker pull oleewere/loggenerator:v0.1.0 
docker run --rm -e JSON_FORMAT=true  -e SLEEP_INTERVAL_SEC=5 -e REPEAT_MESSAGES_BETWEEN_SLEEPS=2 oleewere/loggenerator:v0.1.0 
```

