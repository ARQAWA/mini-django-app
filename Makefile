define check_sha
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/$(1).old_sha
	poetry export --without-hashes -f requirements.txt -o $(1) $(2)
	([ -f $(1) ] && (shasum $(1) | awk '{ print $$1 }') || echo "") > /tmp/.$(1).new_sha
	if diff -q /tmp/$(1).old_sha /tmp/.$(1).new_sha > /dev/null; then \
		echo "- $(1) has not changed"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
	else \
		echo "+ $(1) has changed"; \
		rm /tmp/$(1).old_sha /tmp/.$(1).new_sha; \
	fi
endef

poetry-lock:
	@poetry lock --no-update

poetry-sync:
	@poetry install --sync --no-root --with dev

poetry-export-reqs:
	@$(call check_sha,requirements.txt,)
	@$(call check_sha,requirements-dev.txt,--with dev)

sync: poetry-lock poetry-sync poetry-export-reqs

ruff-format:
	@ruff format --preview

ruff-check:
	@ruff check --preview --fix --unsafe-fixes

mypy:
	@mypy .

linters: ruff-format ruff-check mypy

vult:
	@vulture app

django-cache:
	@python manage.py createcachetable

django-migrate:
	@python manage.py migrate

#django-collectstatic:
	@#python manage.py collectstatic --noinput

django-init: django-cache django-migrate #django-collectstatic

django-create-su:
	@python3 manage.py createsuperuser

django-uvicorn-run:
	@uvicorn "app.core.asgi:application" \
		--host "0.0.0.0" \
		--loop uvloop \
		--http httptools \
		--lifespan off \
		--interface asgi3

run-django: django-init django-uvicorn-run

run-tg-bot:
	@python3 -m app.tg_bot.main

run-hamster:
	@python3 -m app.hamster.main

deploy:
	@echo "Deploying to production"
	@docker compose down && docker compose up --build -d && docker compose logs --tail=3 -f
