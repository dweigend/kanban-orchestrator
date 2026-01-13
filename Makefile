.PHONY: dev check backend frontend

# Start both servers (press Ctrl+C to stop)
dev:
	@echo "🚀 Starting servers..."
	@trap 'kill 0' EXIT; \
	cd backend && uv run uvicorn main:app --reload --port 8000 & \
	cd frontend && bun dev & \
	wait

# Run all quality checks
check:
	@echo "🔍 Backend checks..."
	cd backend && uv run ruff check --fix . && uv run ruff format . && uvx ty check
	@echo "🔍 Frontend checks..."
	cd frontend && bunx biome check --write . && bunx svelte-check --threshold warning
	@echo "✅ All checks passed!"

# Individual server commands
backend:
	cd backend && uv run uvicorn main:app --reload --port 8000

frontend:
	cd frontend && bun dev
