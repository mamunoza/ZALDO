.PHONY: dev backend frontend migrate seed test

ENV_FILE ?= .env

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

dev:
	docker compose up --build

migrate:
	alembic -c db/alembic.ini upgrade head

seed:
	python scripts/seed_backend.py

test:
	pytest backend/tests
