# ATL Pubnix Development Makefile

.PHONY: help dev-up dev-down dev-logs test test-unit test-integration clean build

help: ## Show this help message
	@echo "ATL Pubnix Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev-up: ## Start development environment
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml up -d; \
		echo ""; \
		echo "Development environment started!"; \
		echo "Web interface: http://localhost:8080"; \
		echo "SSH access: ssh -p 2222 testuser1@localhost (password: testpass)"; \
		echo "Web dev server: http://localhost:3000"; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi

dev-down: ## Stop development environment
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml down; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi

dev-logs: ## Show development environment logs
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml logs -f; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi

dev-shell: ## Get shell access to development container
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml exec pubnix-dev bash; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi

test: ## Run all tests (dockerized)
	@if [ -f docker/testing/docker-compose.yml ]; then \
		docker-compose -f docker/testing/docker-compose.yml up --abort-on-container-exit; \
		docker-compose -f docker/testing/docker-compose.yml down; \
	else \
		echo "[skip] docker/testing/docker-compose.yml not found"; \
	fi

test-unit: ## Run unit tests only
	cd backend && uv run pytest tests/ -v

test-integration: ## Run integration tests only
	@if [ -d backend/tests/integration ]; then \
		cd backend && uv run pytest tests/integration/ -v; \
	else \
		echo "[skip] no backend/tests/integration directory"; \
	fi

lint: ## Run code linting
	cd backend && uv run ruff check . --fix --exit-zero
	@if [ -f web/package.json ]; then \
		if command -v npm >/dev/null 2>&1; then \
			cd web && npm run lint || echo "[warn] web lint failed (eslint may be missing)"; \
		else \
			echo "[skip] npm not installed"; \
		fi; \
	else \
		echo "[skip] web/package.json not found"; \
	fi

format: ## Format code
	cd backend && uv run ruff format .
	@if [ -f web/package.json ]; then \
		cd web && npm run format; \
	else \
		echo "[skip] web/package.json not found"; \
	fi

clean: ## Clean up development environment
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml down -v; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi
	@if [ -f docker/testing/docker-compose.yml ]; then \
		docker-compose -f docker/testing/docker-compose.yml down -v; \
	else \
		echo "[skip] docker/testing/docker-compose.yml not found"; \
	fi
	@if command -v docker >/dev/null 2>&1; then \
		docker system prune -f; \
	else \
		echo "[skip] docker not installed"; \
	fi

build: ## Build all Docker images
	@if [ -f docker/development/docker-compose.yml ]; then \
		docker-compose -f docker/development/docker-compose.yml build; \
	else \
		echo "[skip] docker/development/docker-compose.yml not found"; \
	fi
	@if [ -f docker/testing/docker-compose.yml ]; then \
		docker-compose -f docker/testing/docker-compose.yml build; \
	else \
		echo "[skip] docker/testing/docker-compose.yml not found"; \
	fi

setup-dev: ## Set up development environment (first time)
	@echo "Setting up ATL Pubnix development environment..."
	@echo "Installing backend dependencies..."
	cd backend && uv sync --dev
	@echo "Installing web dependencies..."
	@if [ -f web/package.json ]; then \
		cd web && npm install; \
	else \
		echo "[skip] web/package.json not found"; \
	fi
	@echo "Building Docker images..."
	$(MAKE) build
	@echo "Starting development environment..."
	$(MAKE) dev-up
	@echo ""
	@echo "Setup complete! Run 'make help' for available commands."

ssh-test: ## Test SSH connection to development environment
	@echo "Testing SSH connection (password: testpass):"
	@if [ "$$ENABLE_SSH_TEST" = "1" ]; then \
		ssh -o StrictHostKeyChecking=no -p 2222 testuser1@localhost "echo 'SSH connection successful!'; whoami; pwd; ls -la"; \
	else \
		echo "[skip] set ENABLE_SSH_TEST=1 to run this test"; \
	fi