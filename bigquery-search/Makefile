deploy:
	gcloud run deploy bigquery-search \
	--source . \
	--region "us-central1" \
	--platform managed

build:
	docker build -t bigquery-search .

run-sh:
	docker run -it --user app bigquery-search /bin/bash

exec:	
	docker run -it -p 8080:8080 bigquery-search

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  deploy: Deploy the application to Google Cloud Run"
	@echo "  help:   Show this help message"
