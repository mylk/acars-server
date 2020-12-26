deps_sys:
ifeq (, $(shell which acarsdec 2> /dev/null))
	$(error Please install acarsdec, first.)
endif
ifneq (0, $(shell cat /sys/module/usbcore/parameters/usbfs_memory_mb))
	echo 0 | sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb
endif

deps:
	pip install -r requirements.txt

deps_dev:
	pip install -r requirements_dev.txt

deps_image_downloader:
	pip install -r requirements_image_downloader.txt

client:
	PYTHONPATH=. python acarsserver/cli/client.py

client_fake: clean
	PYTHONPATH=. python acarsserver/cli/client_fake.py

image_download:
	PYTHONPATH=. python acarsserver/cli/image_download.py

listener:
	PYTHONPATH=. python acarsserver/cli/listener.py

web:
	python run.py

db_migrate:
	yoyo apply

test: clean
	chmod 0777 acarsserver/log ; \
	docker-compose run --rm test ; \
	docker-compose kill rabbitmq

clean:
	find . -name *.pyc -delete
	find . -name __pycache__ -type d -delete
