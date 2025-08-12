# ATL Pubnix Tests

Test suites and testing utilities for all system components.

## Test Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `e2e/` - End-to-end tests for complete user workflows
- `security/` - Security and penetration testing
- `performance/` - Load and performance testing
- `fixtures/` - Test data and mock configurations

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/e2e/
```