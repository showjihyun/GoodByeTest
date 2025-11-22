import subprocess
import os
import re

class Analyzer:
    def __init__(self):
        pass

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return None, str(e), -1

    def run_lint(self, file_path):
        """
        Determines the linter based on file extension and runs it.
        """
        if file_path.endswith('.py'):
            return self.run_pylint(file_path)
        elif file_path.endswith('.js') or file_path.endswith('.ts'):
            return self.run_eslint(file_path)
        elif file_path.endswith('.java'):
            return self.run_checkstyle(file_path)
        return None

    def run_pylint(self, file_path):
        # Example: pylint --output-format=json
        print(f"Running Pylint on {file_path}...")
        # Mock return for now
        return {"tool": "pylint", "file": file_path, "status": "passed", "errors": []}

    def run_eslint(self, file_path):
        print(f"Running ESLint on {file_path}...")
        return {"tool": "eslint", "file": file_path, "status": "passed", "errors": []}

import subprocess
import os
import re

class Analyzer:
    def __init__(self):
        pass

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return None, str(e), -1

    def run_lint(self, file_path):
        """
        Determines the linter based on file extension and runs it.
        """
        if file_path.endswith('.py'):
            return self.run_pylint(file_path)
        elif file_path.endswith('.js') or file_path.endswith('.ts'):
            return self.run_eslint(file_path)
        elif file_path.endswith('.java'):
            return self.run_checkstyle(file_path)
        return None

    def run_pylint(self, file_path):
        # Example: pylint --output-format=json
        print(f"Running Pylint on {file_path}...")
        # Mock return for now
        return {"tool": "pylint", "file": file_path, "status": "passed", "errors": []}

    def run_eslint(self, file_path):
        print(f"Running ESLint on {file_path}...")
        return {"tool": "eslint", "file": file_path, "status": "passed", "errors": []}

    def run_checkstyle(self, file_path):
        print(f"Running Checkstyle on {file_path}...")
        return {"tool": "checkstyle", "file": file_path, "status": "passed", "errors": []}

    def run_compliance_check(self, file_path, standard="korea_public"):
        """
        Checks for compliance violations based on the specified standard.
        """
        violations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            status = "passed"
            
            # 1. Uncontrolled Logging (CWE-117)
            if "System.out.print" in content or "console.log" in content or "print(" in content:
                violations.append("Violation: Use of standard output for logging (CWE-117). Use a Logger.")
                status = "failed"

            # 2. Weak Encryption (MD5, SHA1)
            if "MD5" in content or "SHA1" in content:
                violations.append("Violation: Use of weak encryption algorithm (MD5/SHA1). Use SHA-256 or higher.")
                status = "failed"

            # 3. Hardcoded IP Addresses
            import re
            ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
            if re.search(ip_pattern, content):
                violations.append("Violation: Hardcoded IP address detected.")
                status = "failed"

            return {"tool": "compliance", "file": file_path, "status": status, "errors": violations}
            
        except Exception as e:
            return {"tool": "compliance", "file": file_path, "status": "error", "errors": [str(e)]}

    def run_secret_scan(self, file_path):
        """
        Scans for secrets using detect-secrets.
        """
        print(f"Scanning {file_path} for secrets...")
        # Mock implementation for demo purposes as detect-secrets might need complex setup
        # In real world: use detect_secrets.SecretsCollection
        
        violations = []
        status = "passed"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Simple heuristic for demo
            if "sk-" in content or "ghp_" in content or "password =" in content:
                 violations.append("Potential Secret detected (API Key or Password).")
                 status = "failed"
                 
            return {"tool": "secret-scan", "file": file_path, "status": status, "errors": violations}
        except Exception as e:
             return {"tool": "secret-scan", "file": file_path, "status": "error", "errors": [str(e)]}
