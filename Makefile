define check_sha
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/$(1).old_sha
	poetry export --without-hashes -f requirements.txt -o $(1) $(2)
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/.$(1).new_sha
	if diff -q /tmp/$(1).old_sha /tmp/.$(1).new_sha > /dev/null; then \
		echo "$(1) has not changed"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
	else \
		echo "Error: $(1) has changed!"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
		exit 1; \
	fi
endef

poetry-lock:
	@poetry lock --no-update

poetry-sync:
	@poetry install --sync --no-root --with dev

poetry-export-reqs:
	@$(call check_sha,requirements.txt,)

sync: poetry-lock poetry-sync poetry-export-reqs

ruff-format:
	@ruff format --preview

ruff-check:
	@ruff check --preview --fix --unsafe-fixes

mypy:
	@mypy app

linters: ruff-format ruff-check mypy

vult:
	@vulture app

include .env

MIGRATIONS_CH_DIR=./migrations_clickhouse
ch-migrate-make:
	@read -p "Enter migration name: " name_; \
	migrate create -ext sql -dir $(MIGRATIONS_CH_DIR) -seq -digits 6 $$name_

ch-migrate-up:
	@migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_CH_DIR) up

ch-migrate-down:
	@migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_CH_DIR) down

ch-migrate-force:
	@read -p "Enter version to force: " vers_; \
	migrate -database $(CLICKHOUSE_MIGRATION_DSN) -path $(MIGRATIONS_CH_DIR) force $$vers_

MIGRATIONS_PG_DIR=./migrations_postgres
pg-migrate-make:
	@read -p "Enter migration name: " name_; \
	migrate create -ext sql -dir $(MIGRATIONS_PG_DIR) -seq -digits 6 $$name_

pg-migrate-up:
	@migrate -database $(POSTGRES_MIGRATION_DSN) -path "$(MIGRATIONS_PG_DIR)" up

pg-migrate-down:
	@migrate -database $(POSTGRES_MIGRATION_DSN) -path "$(MIGRATIONS_PG_DIR)" down

pg-migrate-force:
	@read -p "Enter version to force: " vers_; \
	migrate -database $(POSTGRES_MIGRATION_DSN) -path "$(MIGRATIONS_PG_DIR)" force $$vers_
