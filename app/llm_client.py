from __future__ import annotations
import json, os, urllib.request

class LLMClient:
    """Small OpenAI-compatible REST client. No local model is required."""
    def __init__(self, api_key=None, endpoint=None, model=None):
        self.api_key = api_key or os.getenv('TOWERIQ_API_KEY')
        self.endpoint = endpoint or os.getenv('TOWERIQ_LLM_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
        self.model = model or os.getenv('TOWERIQ_LLM_MODEL', 'gpt-4.1-mini')

    @property
    def configured(self):
        return bool(self.api_key)

    def answer(self, system_prompt: str, user_prompt: str) -> str:
        if not self.configured:
            raise RuntimeError('No LLM API key configured. The app can still run in evidence-only mode.')
        payload = json.dumps({
            'model': self.model,
            'temperature': 0.1,
            'messages': [
                {'role':'system','content':system_prompt},
                {'role':'user','content':user_prompt}
            ]
        }).encode()
        req = urllib.request.Request(self.endpoint, data=payload, method='POST', headers={
            'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        return data['choices'][0]['message']['content']
