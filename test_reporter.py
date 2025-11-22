
import os
import sys

try:
    print("Importing Reporter...")
    from src.reporter import Reporter
    print("Reporter imported.")

    base_dir = os.path.dirname(os.path.abspath('src/main.py'))
    report_dir = os.path.join(base_dir, '..', 'reports', 'history')
    print(f"Report Dir: {report_dir}")

    reporter = Reporter(template_dir=os.path.join(base_dir, 'templates'), output_dir=report_dir)
    
    data = {
        "project_id": "test",
        "mr_iid": "1",
        "test_execution": {"status": "passed", "details": "test"},
        "static_analysis": [],
        "dynamic_analysis": [],
        "ai_reviews": []
    }
    
    print("Generating report...")
    html, pdf = reporter.generate_report(data)
    print(f"Generated: {html}, {pdf}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
