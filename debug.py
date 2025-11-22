
import os
import sys

print(f"CWD: {os.getcwd()}")
base_dir = os.path.dirname(os.path.abspath('src/main.py'))
print(f"Base Dir: {base_dir}")
report_dir = os.path.join(base_dir, '..', 'reports', 'history')
print(f"Report Dir: {os.path.abspath(report_dir)}")
