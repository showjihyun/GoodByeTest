
import os
import sys
import argparse

from gitlab_client import GitLabClient
from analyzer import Analyzer
from db_checker import DBChecker
from test_runner import TestRunner
from llm_reviewer import LLMReviewer
from notifier import SlackNotifier
from fixer import CodeFixer
from reporter import Reporter
import json

def main():
    print("Initializing GitLab Code Review Agent...")
    
    # 1. Parse Arguments & Environment Variables
    parser = argparse.ArgumentParser(description='GitLab Code Review Agent')
    parser.add_argument('--project-id', help='GitLab Project ID', default=os.environ.get('CI_PROJECT_ID'))
    parser.add_argument('--mr-iid', help='Merge Request IID', default=os.environ.get('CI_MERGE_REQUEST_IID'))
    parser.add_argument('--gitlab-token', help='GitLab Private Token', default=os.environ.get('GITLAB_TOKEN'))
    parser.add_argument('--db-conn', help='DB Connection String', default=os.environ.get('DB_CONNECTION_STRING'))
    
    # LLM Args
    parser.add_argument('--llm-provider', help='LLM Provider (openai, claude, gemini, ollama)', default=os.environ.get('LLM_PROVIDER', 'openai'))
    parser.add_argument('--llm-model', help='LLM Model Name', default=os.environ.get('LLM_MODEL'))
    parser.add_argument('--llm-key', help='API Key for LLM', default=os.environ.get('LLM_API_KEY'))
    parser.add_argument('--ollama-url', help='Ollama Base URL', default=os.environ.get('OLLAMA_URL', 'http://localhost:11434'))
    
    # Compliance Args
    parser.add_argument('--compliance', help='Compliance Standard (e.g., korea_public)', default=None)
    
    # Advanced Args
    parser.add_argument('--slack-webhook', help='Slack Webhook URL', default=os.environ.get('SLACK_WEBHOOK_URL'))
    parser.add_argument('--auto-fix', help='Enable Auto-fix', action='store_true')

    # Test Args
    parser.add_argument('--skip-tests', help='Skip all tests', action='store_true')
    parser.add_argument('--only-unit', help='Run only unit tests', action='store_true')
    parser.add_argument('--only-e2e', help='Run only E2E tests', action='store_true')

    parser.add_argument('--local-files', help='List of local files to scan (bypasses GitLab)', nargs='+')

    args = parser.parse_args()

    # Initialize Client
    gl_client = None
    if args.gitlab_token and not args.local_files:
        if not args.project_id or not args.mr_iid:
             print("Error: Missing Project ID or MR IID for GitLab mode.")
             return
        gl_client = GitLabClient(private_token=args.gitlab_token, project_id=args.project_id)
    
    # Initialize Tools
    analyzer = Analyzer()
    db_checker = DBChecker(connection_string=args.db_conn)
    test_runner = TestRunner()
    notifier = SlackNotifier(webhook_url=args.slack_webhook)
    fixer = CodeFixer()
    
    # Initialize LLM Reviewer
    llm_kwargs = {
        "api_key": args.llm_key,
        "model": args.llm_model,
        "base_url": args.ollama_url
    }
    llm_reviewer = LLMReviewer(provider=args.llm_provider, **llm_kwargs)
    
    db_checker.connect()

    # 2. Fetch Changes
    changed_files = []
    if args.local_files:
        print(f"Running in Local Mode. Scanning files: {args.local_files}")
        changed_files = args.local_files
    elif gl_client:
        print(f"Fetching changes for MR {args.mr_iid}...")
        changes = gl_client.get_mr_changes(args.mr_iid)
        for change in changes['changes']:
            changed_files.append(change['new_path'])
    else:
        # Mock changes for simulation
        print("Running in Simulation Mode (Mock Data)")
        changed_files = ['src/main.py', 'src/UserEntity.java']

    print(f"Target files: {changed_files}")

    # Auto-Fix Logic (Must run sequentially before analysis if enabled)
    if args.auto_fix and changed_files:
        print("--- Stage 0: Auto-Fix (Sequential) ---")
        # Simple pre-check to see what needs fixing
        for file in changed_files:
             # In a real scenario, we might run a quick lint check here first
             if fixer.fix_file(file):
                print(f"Fixed {file}.")

    # Parallel Execution
    print("--- Starting Parallel Execution ---")
    import concurrent.futures
    
    lint_results = []
    db_results = []
    test_result = {"status": "skipped", "details": "Tests skipped"}
    ai_comments = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Define Tasks
        future_static = executor.submit(run_static_analysis_task, analyzer, changed_files, args.compliance)
        future_db = executor.submit(run_db_checks_task, db_checker, changed_files)
        
        future_tests = None
        if not args.skip_tests:
             stages = ['unit', 'integration', 'e2e']
             if args.only_unit: stages = ['unit']
             elif args.only_e2e: stages = ['e2e']
             future_tests = executor.submit(test_runner.run_tests, stages)
        
        # Wait for results
        lint_results = future_static.result()
        db_results = future_db.result()
        if future_tests:
            test_result = future_tests.result()

    print("--- Parallel Execution Completed ---")
    print(f"Test Execution: {test_result['status']}")

    # 5. Run AI Review (Sequential for now as it depends on file content stability)
    print("--- Stage 3: AI Review ---")
    for file in changed_files:
        content = llm_reviewer.get_code_content(file)
        if content:
            review = llm_reviewer.review_code(file, content, compliance_mode=args.compliance)
            ai_comments.append(f"**{file}**: {review}")
            print(f"AI Review for {file}: {review}")

    # 6. Generate Report (JSON) for Dashboard
    
    report_data = {
        "project_id": args.project_id,
        "mr_iid": args.mr_iid,
        "static_analysis": lint_results,
        "dynamic_analysis": db_results,
        "test_execution": test_result,
        "ai_reviews": ai_comments
    }
    
    # Save JSON (Legacy)
    with open("report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    print("Report saved to report.json")

    # Generate HTML & PDF History
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.join(base_dir, '..', 'reports', 'history')
    reporter = Reporter(template_dir=os.path.join(base_dir, 'templates'), output_dir=report_dir)
    html_path, pdf_path = reporter.generate_report(report_data)
    print(f"HTML Report generated: {html_path}")
    print(f"PDF Report generated: {pdf_path}")

    # 7. Report to GitLab
    if gl_client:
        print("Posting summary to GitLab...")
        summary = "## Code Review Agent Report\n\n"
        summary += "### Static Analysis\n" + "\n".join([str(r) for r in lint_results]) + "\n\n"
        summary += "### Dynamic Analysis\n" + "\n".join([str(r) for r in db_results]) + "\n"
        summary += f"Tests: {test_result['status']}\n\n"
        summary += "### AI Review\n" + "\n".join(ai_comments)
        summary += f"\n\n[View Full Report]({os.path.abspath(html_path)})"
        
        gl_client.post_comment(args.mr_iid, summary)
    else:
        print("Skipping GitLab reporting (Simulation Mode)")
        
    # 8. Send Notification
    status = "success" if test_result['status'] == 'passed' else "error"
    msg = f"Code Review Completed for MR !{args.mr_iid}\nStatus: {status.upper()}\nReport: {os.path.abspath(pdf_path)}"
    notifier.send_notification(msg, status=status)

    print("Review Complete.")

def run_static_analysis_task(analyzer, files, compliance_standard):
    print("--- Task: Static Analysis ---")
    results = []
    for file in files:
        # Lint
        res = analyzer.run_lint(file)
        if res: results.append(res)
        
        # Compliance
        if compliance_standard:
            res = analyzer.run_compliance_check(file, standard=compliance_standard)
            if res: results.append(res)
            
        # Secret Scan
        res = analyzer.run_secret_scan(file)
        if res: results.append(res)
            
    return results

def run_db_checks_task(db_checker, files):
    print("--- Task: DB Checks ---")
    results = []
    for file in files:
        res = db_checker.check_file(file)
        if res: results.append(res)
    return results

if __name__ == "__main__":
    main()
