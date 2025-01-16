import requests
from typing import List

class Generator:
    def __init__(self, model: str = "phi4", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str, context: List[str]) -> str:
        formatted_prompt = self._format_prompt(prompt, context)
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": formatted_prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Generation failed: {response.text}")

    def _format_prompt(self, query: str, context: List[str]) -> str:
        context_str = "\n".join(context)
        return f"""Instruct: Using only the context provided below, answer the following question. If the answer cannot be found in the context, say "I cannot answer this based on the provided context."

Context:
{context_str}

Question: {query}

Answer: Let me help you with that."""
