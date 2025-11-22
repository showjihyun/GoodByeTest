# Features

## 1. Multi-Language Support
The agent automatically detects and handles:
-   **Java**: Maven projects (Checkstyle, JUnit).
-   **Python**: Standard projects (Pylint, Pytest).
-   **JavaScript/TypeScript**: Node.js/React projects (ESLint, Jest, Playwright).
-   **Polyglot**: Can analyze mixed repositories in a single run.

## 2. Comprehensive Analysis Pipeline
The review process consists of parallel stages:

### Static Analysis
-   **Linting**: Enforces code style and finds syntax errors.
-   **Compliance**: Checks for specific regulatory requirements (e.g., avoiding `console.log` in production, hardcoded IPs).

### Security Scanning
-   **Secret Detection**: Scans for high-entropy strings, API keys, and passwords using `detect-secrets`.

### Dynamic Analysis
-   **Database Checks**: Validates JPA Entities and Schema consistency (requires DB connection).
-   **Test Execution**: Runs Unit, Integration, and E2E tests and parses results.

## 3. AI Code Review
-   **Context-Aware**: Analyzes the specific changes in the Merge Request.
-   **Multi-Provider**: Supports OpenAI (GPT-4), Anthropic (Claude), Google (Gemini), and Ollama (Local LLaMA).
-   **Actionable Feedback**: Provides suggestions for refactoring, bug fixes, and documentation.

## 4. Reporting & History
-   **Rich Formats**: Generates HTML and PDF reports.
-   **History Tracking**: Archives every review run with timestamps for audit trails.
-   **Integration**: Posts summaries directly to GitLab Merge Requests and sends Slack notifications.
