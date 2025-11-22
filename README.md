# GitLab Code Review Agent 🚀

> **An Intelligent, Automated Code Review Assistant for Your CI/CD Pipeline.**

The GitLab Code Review Agent is a comprehensive tool designed to automate the code review process. It combines static analysis, security scanning, test execution, and LLM-powered AI reviews to ensure high code quality and security before merging.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**Features**](docs/features.md) | Detailed breakdown of supported languages and analysis capabilities. |
| [**Architecture**](docs/architecture.md) | System design, components, and data flow diagrams. |
| [**Usage Guide**](docs/usage_guide.md) | Instructions for installation, configuration, and execution (Local & Docker). |
| [**Roadmap**](docs/roadmap.md) | Future plans and commercial SaaS transition strategy. |

---

## ✨ Key Features

-   **🤖 AI-Powered Reviews**: Integrates with OpenAI, Claude, Gemini, or Ollama to provide intelligent code feedback.
-   **🛡️ Security First**: Built-in secret scanning and compliance checks (e.g., Korea Public Sector standards).
-   **⚡ High Performance**: Parallel execution of static analysis, DB checks, and tests.
-   **📊 Rich Reporting**: Generates detailed HTML & PDF reports with history tracking.
-   **🌍 Polyglot**: Native support for Java, Python, React, and Node.js.

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/gitlab-review-agent.git
cd gitlab-review-agent
```

### 2. Run with Docker
```bash
docker build -t gitlab-review-agent .
docker run -v $(pwd):/app gitlab-review-agent python src/main.py --local-files src/main.py
```

### 3. View Reports
Check the `reports/history/` directory for the generated HTML and PDF reports.

---

## 🤝 Contributing
Contributions are welcome! Please read our [Architecture Guide](docs/architecture.md) to understand the system design before making changes.

## 📄 License
This project is licensed under the MIT License.
