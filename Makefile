# ATL Pubnix Development Makefile

.PHONY: help dev-up dev-down dev-logs test test-unit test-integration clean build

help: ## Show this help message
	@echo "ATL Pubnix Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev-up: ## Start development environment
	docker-compose -f docker/development/docker-compose.yml up -d
	@echo ""
	@echo "Development environment started!"
	@echo "Web interface: http://localhost:8080"
	@echo "SSH access: ssh -p 2222 testuser1@localhost (password: testpass)"
	@echo "Web dev server: http://localhost:3000"

dev-down: ## Stop development environment
	docker-compose -f docker/development/docker-compose.yml down

dev-logs: ## Show development environment logs
	docker-compose -f docker/development/docker-compose.yml logs -f

dev-shell: ## Get shell access to development container
	docker-compose -f docker/development/docker-compose.yml exec pubnix-dev bash

test: ## Run all tests
	docker-compose -f docker/testing/docker-compose.yml up --abort-on-container-exit
	docker-compose -f docker/testing/docker-compose.yml down

test-unit: ## Run unit tests only
	cd backend && python -m pytest tests/unit/ -v

test-integration: ## Run integration tests only
	cd backend && python -m pytest tests/integration/ -v

lint: ## Run code linting
	cd backend && flake8 .
	cd web && npm run lint

format: ## Format code
	cd backend && black . && isort .
	cd web && npm run format

clean: ## Clean up development environment
	docker-compose -f docker/development/docker-compose.yml down -v
	docker-compose -f docker/testing/docker-compose.yml down -v
	docker system prune -f

build: ## Build all Docker images
	docker-compose -f docker/development/docker-compose.yml build
	docker-compose -f docker/testing/docker-compose.yml build

setup-dev: ## Set up development environment (first time)
	@echo "Setting up ATL Pubnix development environment..."
	@echo "Installing backend dependencies..."
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt
	@echo "Installing web dependencies..."
	cd web && npm install
	@echo "Building Docker images..."
	make build
	@echo "Starting development environment..."
	make dev-up
	@echo ""
	@echo "Setup complete! Run 'make help' for available commands."

ssh-test: ## Test SSH connection to development environment
	@echo "Testing SSH connection (password: testpass):"
	ssh -o StrictHostKeyChecking=no -p 2222 testuser1@localhost "echo 'SSH connection successful!'; whoami; pwd; ls -la"