import os
from abc import ABC, abstractmethod
from openai import OpenAI
import anthropic
import google.generativeai as genai
import requests

class LLMProvider(ABC):
    @abstractmethod
    def generate_review(self, prompt: str) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_review(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful code review assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {e}"

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key, model="claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate_review(self, prompt: str) -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Anthropic Error: {e}"

class GeminiProvider(LLMProvider):
    def __init__(self, api_key, model="gemini-1.5-pro-latest"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_review(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"

class OllamaProvider(LLMProvider):
    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        self.base_url = base_url
        self.model = model

    def generate_review(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            else:
                return f"Ollama Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Ollama Connection Error: {e}"

class LLMFactory:
    @staticmethod
    def get_provider(provider_name, **kwargs):
        if provider_name == "openai":
            return OpenAIProvider(api_key=kwargs.get("api_key"), model=kwargs.get("model", "gpt-3.5-turbo"))
        elif provider_name == "claude":
            return AnthropicProvider(api_key=kwargs.get("api_key"), model=kwargs.get("model", "claude-3-opus-20240229"))
        elif provider_name == "gemini":
            return GeminiProvider(api_key=kwargs.get("api_key"), model=kwargs.get("model", "gemini-1.5-pro-latest"))
        elif provider_name == "ollama":
            return OllamaProvider(base_url=kwargs.get("base_url", "http://localhost:11434"), model=kwargs.get("model", "llama3"))
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
