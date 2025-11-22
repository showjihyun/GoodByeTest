# Usage Guide

## Prerequisites
-   **Docker**: For containerized execution (Recommended).
-   **Python 3.10+**: For local execution.
-   **GitLab Token**: If integrating with GitLab CI.
-   **LLM API Key**: OpenAI, Anthropic, or Google API key (optional, for AI reviews).

## Installation

### Option A: Docker (Recommended)
1.  **Build the Image**:
    ```bash
    docker build -t gitlab-review-agent .
    ```

### Option B: Local Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install Analysis Tools**:
    -   Ensure `mvn`, `npm`, `pylint`, `eslint`, `checkstyle` are in your PATH if you plan to run them locally.

## Running the Agent

### 1. Local Simulation Mode
Run the agent against local files without connecting to GitLab.
```bash
python src/main.py --local-files src/main.py app.js --compliance korea_public
```

### 2. GitLab CI Integration
Add the following to your `.gitlab-ci.yml`:

```yaml
code_review:
  stage: test
  image: gitlab-review-agent:latest
  script:
    - python src/main.py
  variables:
    GITLAB_TOKEN: $GITLAB_TOKEN
    OPENAI_API_KEY: $OPENAI_API_KEY
  only:
    - merge_requests
```

## Configuration Options

| Argument | Env Variable | Description |
|----------|--------------|-------------|
| `--project-id` | `CI_PROJECT_ID` | GitLab Project ID |
| `--mr-iid` | `CI_MERGE_REQUEST_IID` | Merge Request IID |
| `--llm-provider` | `LLM_PROVIDER` | AI Provider (openai, claude, gemini, ollama) |
| `--compliance` | - | Compliance Standard (e.g., `korea_public`) |
| `--convention` | - | Coding Convention (`google`, `airbnb`, `pep8`, `sun`) |
| `--skip-tests` | - | Skip test execution stage |
| `--local-files` | - | List of files to scan locally |

## Output
-   **Console**: Real-time logs of analysis progress.
-   **Reports**:
    -   `reports/history/report_YYYYMMDD_HHMMSS.html`: Detailed web report.
    -   `reports/history/report_YYYYMMDD_HHMMSS.pdf`: PDF document.
-   **GitLab**: Comment posted on the Merge Request with a summary.
