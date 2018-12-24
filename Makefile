# Makefile sandbox-celery-rabbitmq

# These targets are not files

.PHONY: all help

all: help requirements check_rabbitmq clean celery celery.beat celery.purge celery.kill celery.two celery.ten pep8 rabbitmq.config test test.dev test.failfirst test.collect test.skip.covered coverage coverage.html coveralls docker.login docker.build.dev docker.build_ docker.tag docker.build docker.push docker.build.push docker.pull docker.run.bash docker.run

help:
	@echo 'Makefile *** alpha *** Makefile'

check.test_path:
	@if test "$(TEST_PATH)" = "" ; then echo "TEST_PATH is undefined. The default is tests."; fi

check.docker_registry:
	@if test "$(DOCKER_REGISTRY)" = "" ; then echo "DOCKER_REGISTRY is undefined."; exit 1; fi

requirements:
	@pip install -r requirements.txt

check_rabbitmq:
	@python check_rabbitmq_connection_2.py

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

pep8:
	@pycodestyle --filename="*.py" .

celery:
	@celery -A tasks worker --loglevel=INFO -c 1 -Q default

celery.two:
	@celery -A tasks worker --loglevel=INFO -c 2 -Q default

celery.ten:
	@celery -A tasks worker --loglevel=INFO -c 10 -Q default

celery.beat:
	@celery -A tasks beat

celery.purge:
	"from celery.task.control import discard_all; discard_all()" | python

celery.kill:
	@kill `ps -ef | grep "celery" | awk '{print $$2}'`

rabbitmq.config:
	@rabbitmqctl add_user sandbox_user sandbox_password
	@rabbitmqctl add_vhost sandbox_host
	@rabbitmqctl set_permissions -p sandbox_host sandbox_user ".*" ".*" ".*"

### TESTS

test: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report term-missing --basetemp=tests/media --disable-pytest-warnings

test.dev: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-fail-under 70 --cov-report term-missing --basetemp=tests/media --disable-pytest-warnings

test.failfirst: check.test_path
	@py.test -s -x $(TEST_PATH) --basetemp=tests/media --disable-pytest-warnings

test.collect: check.test_path
	@py.test -s $(TEST_PATH) --basetemp=tests/media --collect-only --disable-pytest-warnings

test.skip.covered: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report term:skip-covered --doctest-modules --basetemp=tests/media --disable-pytest-warnings

coverage: check.test_path test

coverage.html: check.test_path
	@py.test -s $(TEST_PATH) --cov --cov-report html --doctest-modules --basetemp=tests/media --disable-pytest-warnings

coveralls: coverage
	@coveralls

### DOCKER

DOCKER_NAME := intelivix/loafer
DOCKER_TAG := $$(if [ "${TRAVIS_TAG}" == "" ]; then echo `git log -1 --pretty=%h`; else echo "${TRAVIS_TAG}"; fi)
DOCKER_IMG_TAG := ${DOCKER_NAME}:${DOCKER_TAG}
DOCKER_LATEST := ${DOCKER_NAME}:latest

docker.login:
	$$(aws ecr get-login --no-include-email --region us-east-1)

docker.build.dev:
	@docker build -f Dockerfile --no-cache -t ${DOCKER_IMG_TAG} .

docker.build_: check.docker_registry
	@echo "Build started on `date`"
	@docker build -f Dockerfile -t ${DOCKER_IMG_TAG} .
	@echo "Build completed on `date`"

docker.tag: check.docker_registry
	@docker tag ${DOCKER_IMG_TAG} ${DOCKER_REGISTRY}/${DOCKER_LATEST}
	@docker tag ${DOCKER_IMG_TAG} ${DOCKER_REGISTRY}/${DOCKER_IMG_TAG}

docker.build: docker.build_ docker.tag

docker.push: check.docker_registry
	@echo "Pushing images started on `date`"
	@docker push ${DOCKER_REGISTRY}/${DOCKER_LATEST}
	@docker push ${DOCKER_REGISTRY}/${DOCKER_IMG_TAG}
	@echo "Pushing images completed on `date`"

docker.build.push: docker.build docker.push

docker.pull: check.docker_registry
	@docker pull ${DOCKER_REGISTRY}/${DOCKER_LATEST}

docker.run.bash:
	@docker run -it --env-file .env worker-loafer /bin/sh

docker.run:
	@docker run -it \
		--env-file .env \
		--log-driver=awslogs \
	     	--log-opt awslogs-region=us-east-1 \
	     	--log-opt awslogs-group=loafer-test \
	     	--log-opt awslogs-stream=worker \
	     	--log-opt awslogs-create-group=true \
	     	--log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}' \
		worker-loafer
