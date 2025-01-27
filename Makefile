# TODO look at Felis's makefile

# Variables for images and Dockerfiles
DOCKER_IMAGE_NAME_PQSERVER := pqserver
DOCKERFILE_PQSERVER := Dockerfile.pqserver

DOCKER_IMAGE_NAME_HINFO := hinfo
DOCKERFILE_HINFO := Dockerfile.hinfo

DOCKER_COMPOSE := docker-compose

# Default target: Help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all       - Build both pqserver and hinfo with Docker Compose"
	@echo "  pqserver  - Build the pqserver Docker image"
	@echo "  hinfo     - Build the hinfo Docker image"
	@echo "  clean     - Remove built images"
	@echo "  up        - Start the pqserver service with Docker Compose"
	@echo "  down      - Stop all Docker Compose services"

# Default target: Build all images
.PHONY: all
all: pqserver hinfo

# Build targets
.PHONY: pqserver
pqserver:
	$(DOCKER_COMPOSE) build pqserver

.PHONY: hinfo
hinfo:
	$(DOCKER_COMPOSE) build hinfo

# Clean target
.PHONY: clean
clean:
	docker image rm -f pqserver hinfo || true

# Docker Compose up for pqserver
.PHONY: up
up:
	$(DOCKER_COMPOSE) up pqserver

# Docker Compose down
.PHONY: down
down:
	$(DOCKER_COMPOSE) down
.PHONY: db-shell
db-shell:
    docker-compose -f $(DOCKER_COMPOSE) exec local-db psql -U postgres

.PHONY: schema
schema:
	felis create --engine-url postgresql+psycopg2://username:password@localhost/database schema.yaml