from llm_providers import LLMFactory

class LLMReviewer:
    def __init__(self, provider="openai", **kwargs):
        self.provider_name = provider
        try:
            self.provider = LLMFactory.get_provider(provider, **kwargs)
        except Exception as e:
            print(f"Failed to initialize LLM Provider {provider}: {e}")
            self.provider = None

    def review_code(self, file_path, code_content, compliance_mode=None):
        """
        Sends code to LLM for review.
        """
        print(f"AI ({self.provider_name}) Reviewing {file_path}...")
        
        compliance_instruction = ""
        if compliance_mode == "korea_public":
            compliance_instruction = """
            CRITICAL: You must review this code against 'South Korea NIS Software Development Security Guide'.
            1. Check for Personal Information Leakage.
            2. Check for SQL Injection and OS Command Injection.
            3. Check for Weak Encryption (MD5, SHA1 are BANNED).
            4. Check for Uncontrolled Logging (System.out.println is BANNED).
            """

        prompt = f"""
        You are a senior code reviewer. Review the following code for bugs, security issues, and style improvements.
        Be concise and constructive.
        {compliance_instruction}
        
        File: {file_path}
        
        Code:
        {code_content}
        """
        
        if self.provider:
            return self.provider.generate_review(prompt)
        else:
            return "AI Review (Mock): Provider not initialized."

    def get_code_content(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
